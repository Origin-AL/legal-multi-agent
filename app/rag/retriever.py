from __future__ import annotations

import re

from app.models import Citation, KnowledgeDocument


class LegalKnowledgeRetriever:
    def __init__(self, documents: list[KnowledgeDocument]) -> None:
        self.documents = documents

    def search(self, query: str, *, top_k: int = 4) -> list[Citation]:
        query_tokens = self._tokenize(query)
        scored: list[tuple[float, KnowledgeDocument]] = []

        for document in self.documents:
            haystack = self._tokenize(" ".join([document.title, document.excerpt, document.body, " ".join(document.tags)]))
            overlap = len(query_tokens & haystack)
            score = overlap / max(len(query_tokens), 1)
            if score > 0:
                scored.append((score, document))

        scored.sort(key=lambda item: item[0], reverse=True)
        top_matches = scored[:top_k] if scored else [(0.0, document) for document in self.documents[:top_k]]
        return [
            Citation(
                source_type=document.source_type,
                title=document.title,
                excerpt=document.excerpt,
                reference_id=document.reference_id,
                score=round(score, 3),
            )
            for score, document in top_matches
        ]

    def _tokenize(self, text: str) -> set[str]:
        normalized = text.lower()
        words = set(re.findall(r"[a-z0-9_]+", normalized))
        chars = {char for char in normalized if "\u4e00" <= char <= "\u9fff"}
        return words | chars
