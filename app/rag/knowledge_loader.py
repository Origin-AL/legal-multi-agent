from __future__ import annotations

import json
import logging
from pathlib import Path

from app.models import KnowledgeDocument

logger = logging.getLogger(__name__)


def load_knowledge_documents(path: Path) -> list[KnowledgeDocument]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        docs = [KnowledgeDocument(**item) for item in payload]
        logger.info("Loaded %d knowledge documents from %s", len(docs), path)
        return docs
    except FileNotFoundError:
        logger.warning("Knowledge base not found at %s, starting with empty retriever", path)
    except json.JSONDecodeError as exc:
        logger.warning("Knowledge base JSON parse error at %s: %s, starting with empty retriever", path, exc)
    except Exception as exc:
        logger.warning("Failed to load knowledge base from %s: %s, starting with empty retriever", path, exc)
    return []
