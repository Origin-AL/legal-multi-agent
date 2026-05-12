from __future__ import annotations

import re

import jieba

from app.models import Citation, KnowledgeDocument

LAYER_WEIGHTS = {"statute": 1.0, "interpretation": 0.85, "case": 0.7}
MIN_SCORE_THRESHOLD = 0.15

_STOP_WORDS = frozenset(
    "的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 "
    "自己 这 他 她 它 们 那 些 什么 怎么 如何 可以 能 吗 呢 吧 啊 呀 嘛 哦 "
    "the a an is are was were be been being have has had do does did will would "
    "shall should may might can could of to in for on with at by from as into".split()
)


class LegalKnowledgeRetriever:
    def __init__(self, documents: list[KnowledgeDocument]) -> None:
        self.documents = documents
        self._doc_tokens: list[tuple[KnowledgeDocument, set[str]]] = [
            (doc, self._tokenize(" ".join([doc.title, doc.excerpt, doc.body, " ".join(doc.tags)])))
            for doc in documents
        ]

    def search(self, query: str, *, top_k: int | None = None) -> list[Citation]:
        query_tokens = self._tokenize(query)
        query_lower = query.lower()

        if top_k is None:
            top_k = min(max(3, len(query_tokens) // 3), 8)

        scored: list[tuple[float, KnowledgeDocument]] = []

        for document, haystack in self._doc_tokens:
            overlap = len(query_tokens & haystack)
            base_score = overlap / max(len(query_tokens), 1)
            if base_score <= 0:
                continue

            cat_boost = 1.0
            if document.law_category and document.law_category in query_lower:
                cat_boost = 1.3
            for tag in document.tags:
                if tag in query_lower:
                    cat_boost = max(cat_boost, 1.15)

            layer_weight = LAYER_WEIGHTS.get(document.layer_type, 1.0)
            final_score = base_score * cat_boost * layer_weight
            scored.append((final_score, document))

        scored.sort(key=lambda item: item[0], reverse=True)
        filtered = [(s, d) for s, d in scored if s >= MIN_SCORE_THRESHOLD]

        if not filtered:
            return []

        top_matches = filtered[:top_k]
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
        words = jieba.lcut(normalized)
        tokens: set[str] = set()
        for w in words:
            w = w.strip()
            if not w or w in _STOP_WORDS:
                continue
            if re.fullmatch(r"[a-z0-9_]+", w):
                tokens.add(w)
            elif "一" <= w[-1] <= "鿿" and len(w) >= 2:
                tokens.add(w)
        return tokens
