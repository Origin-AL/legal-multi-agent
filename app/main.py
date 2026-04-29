from fastapi import FastAPI, HTTPException

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


@app.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: str) -> AnalysisResponse:
    response = orchestrator.get_analysis(analysis_id)
    if response is None:
        raise HTTPException(status_code=404, detail="analysis not found")
    return response
