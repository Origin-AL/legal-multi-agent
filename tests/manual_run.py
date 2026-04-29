from app.config import settings
from app.llm.factory import build_llm_provider
from app.models import AnalysisRequest, CaseMaterial
from app.rag.knowledge_loader import load_knowledge_documents
from app.rag.retriever import LegalKnowledgeRetriever
from app.repositories.analysis_repository import AnalysisRepository
from app.services.orchestrator import LegalOrchestrator


def main() -> None:
    orchestrator = LegalOrchestrator(
        llm_provider=build_llm_provider(),
        retriever=LegalKnowledgeRetriever(load_knowledge_documents(settings.knowledge_base_path)),
        repository=AnalysisRepository(settings.database_path),
    )
    response = orchestrator.run(
        AnalysisRequest(
            user_query="\u8bf7\u5e2e\u6211\u5ba1\u67e5\u5408\u540c\u4e2d\u7684\u89e3\u9664\u6761\u6b3e\u548c\u8fdd\u7ea6\u8d23\u4efb\u98ce\u9669",
            materials=[
                CaseMaterial(
                    title="\u670d\u52a1\u5408\u540c",
                    content=(
                        "\u7532\u65b9\u59d4\u6258\u4e59\u65b9\u63d0\u4f9b\u8f6f\u4ef6\u5f00\u53d1\u670d\u52a1\u3002"
                        "\u82e5\u4e59\u65b9\u903e\u671f15\u65e5\u672a\u5b8c\u6210\u4ea4\u4ed8\uff0c\u7532\u65b9\u6709\u6743\u89e3\u9664\u5408\u540c\u3002"
                        "\u8fdd\u7ea6\u91d1\u6309\u5408\u540c\u603b\u4ef7\u768430%\u8ba1\u7b97\u3002"
                    ),
                )
            ],
        )
    )
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
