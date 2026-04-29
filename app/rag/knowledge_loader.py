from __future__ import annotations

import json
from pathlib import Path

from app.models import KnowledgeDocument


def load_knowledge_documents(path: Path) -> list[KnowledgeDocument]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [KnowledgeDocument(**item) for item in payload]
