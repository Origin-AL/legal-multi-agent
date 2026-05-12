import asyncio
import json
import logging
import threading
from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

logger = logging.getLogger(__name__)


class _Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

from app.config import settings
from app.frontend import render_index
from app.llm.factory import build_llm_provider
from app.models import AnalysisRequest, AnalysisResponse
from app.rag.knowledge_loader import load_knowledge_documents
from app.rag.retriever import LegalKnowledgeRetriever
from app.repositories.analysis_repository import AnalysisRepository
from app.services.orchestrator import LegalOrchestrator

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="Prompt-driven legal multi-agent backend with local RAG and SQLite persistence.",
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误，请稍后重试。"},
    )

repository = AnalysisRepository(settings.database_path)
retriever = LegalKnowledgeRetriever(load_knowledge_documents(settings.knowledge_base_path))
orchestrator = LegalOrchestrator(
    llm_provider=build_llm_provider(),
    retriever=retriever,
    repository=repository,
)


@app.get("/", include_in_schema=False)
def index():
    return render_index()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analysis", response_model=AnalysisResponse)
def analyze_case(request: AnalysisRequest) -> AnalysisResponse:
    if not request.user_query.strip():
        raise HTTPException(status_code=400, detail="user_query must not be empty")
    return orchestrator.run(request)


@app.post("/analysis/stream")
async def analyze_case_stream(request: AnalysisRequest):
    if not request.user_query.strip():
        raise HTTPException(status_code=400, detail="user_query must not be empty")

    queue: asyncio.Queue[dict | None] = asyncio.Queue()

    def _produce() -> None:
        try:
            for chunk in orchestrator.run_streaming(request):
                asyncio.run_coroutine_threadsafe(queue.put(chunk), loop)
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    loop = asyncio.get_running_loop()
    threading.Thread(target=_produce, daemon=True).start()

    async def event_generator() -> AsyncGenerator[str, None]:
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            yield f"data: {json.dumps(chunk, ensure_ascii=False, cls=_Encoder)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: str) -> AnalysisResponse:
    response = orchestrator.get_analysis(analysis_id)
    if response is None:
        raise HTTPException(status_code=404, detail="analysis not found")
    return response
