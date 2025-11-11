"""Simple in-memory vector store for semantic search."""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List, Tuple

_TOKEN_PATTERN = re.compile(r"[\w']+")


def _tokenize(text: str) -> List[str]:
    return _TOKEN_PATTERN.findall(text.lower())


@dataclass
class SearchResult:
    text: str
    score: float


class SimpleVectorStore:
    """Lightweight TF-IDF based vector store with cosine similarity."""

    def __init__(self) -> None:
        self._documents: List[str] = []
        self._token_counts: List[Counter[str]] = []
        self._doc_vectors: List[Tuple[dict[str, float], float]] = []
        self._idf: dict[str, float] = {}

    @property
    def documents(self) -> List[str]:
        return self._documents

    def add_documents(self, docs: Iterable[str]) -> None:
        for doc in docs:
            tokens = _tokenize(doc)
            if not tokens:
                continue
            counts = Counter(tokens)
            self._documents.append(doc)
            self._token_counts.append(counts)
        self._recompute_vectors()

    def _recompute_vectors(self) -> None:
        if not self._token_counts:
            self._idf = {}
            self._doc_vectors = []
            return

        total_docs = len(self._token_counts)
        doc_freq: Counter[str] = Counter()
        for counts in self._token_counts:
            doc_freq.update(counts.keys())

        self._idf = {
            term: math.log((total_docs + 1) / (freq + 1)) + 1.0
            for term, freq in doc_freq.items()
        }

        self._doc_vectors = []
        for counts in self._token_counts:
            length = sum(counts.values()) or 1
            vector = {
                term: (counts[term] / length) * self._idf.get(term, 1.0)
                for term in counts
            }
            norm = math.sqrt(sum(value * value for value in vector.values())) or 1.0
            self._doc_vectors.append((vector, norm))

    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        if not self._doc_vectors:
            return []

        tokens = _tokenize(query)
        if not tokens:
            return []

        q_counts = Counter(tokens)
        length = sum(q_counts.values()) or 1
        q_vec = {
            term: (q_counts[term] / length) * self._idf.get(term, 1.0)
            for term in q_counts
        }
        q_norm = math.sqrt(sum(value * value for value in q_vec.values())) or 1.0

        results: List[SearchResult] = []
        for (doc_vec, doc_norm), doc_text in zip(self._doc_vectors, self._documents):
            dot = sum(q_vec.get(term, 0.0) * doc_vec.get(term, 0.0) for term in q_vec)
            score = dot / (q_norm * doc_norm) if q_norm and doc_norm else 0.0
            if score > 0:
                results.append(SearchResult(text=doc_text, score=score))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]


__all__ = ["SimpleVectorStore", "SearchResult"]
