from __future__ import annotations

from pathlib import Path

from shared.ai import SearchResult, TfidfVectorStore, get_llm_provider
from shared.ai.providers import LLMProvider

from .chunking import DocumentChunk, load_markdown_chunks


class RAGAssistant:
    def __init__(self, chunks: list[DocumentChunk], provider: LLMProvider | None = None) -> None:
        self.chunks = chunks
        self.provider = provider or get_llm_provider()
        self.store = TfidfVectorStore()
        self.store.add_texts(
            [chunk.text for chunk in chunks],
            sources=[chunk.source for chunk in chunks],
            metadata=[chunk.metadata() for chunk in chunks],
        )

    def retrieve(self, question: str, *, k: int = 4, min_score: float = 0.01) -> list[SearchResult]:
        return self.store.search(question, k=k, min_score=min_score)

    def format_citation(self, result: SearchResult, index: int) -> dict[str, object]:
        page = result.metadata.get("page") or None
        citation_id = f"C{index}"
        return {
            "citation_id": citation_id,
            "source": result.source,
            "section": result.metadata.get("section", ""),
            "heading": result.metadata.get("heading", ""),
            "clause_id": result.metadata.get("clause_id", ""),
            "page": page,
            "chunk_id": result.metadata.get("chunk_id", ""),
            "score": round(result.score, 3),
            "excerpt": result.text[:360],
            "reference": self._citation_reference(result, citation_id),
        }

    def _citation_reference(self, result: SearchResult, citation_id: str) -> str:
        page = result.metadata.get("page")
        page_label = f", page {page}" if page else ""
        return (
            f"[{citation_id}] {result.source}"
            f" > {result.metadata.get('heading', result.metadata.get('section', ''))}"
            f" ({result.metadata.get('clause_id', 'no-clause-id')}{page_label})"
        )

    def answer(self, question: str, *, k: int = 4) -> dict[str, object]:
        if not question.strip():
            return {
                "answer": "Please provide a code, guidance, or design-standard question.",
                "sources": [],
            }
        results = self.retrieve(question, k=k)
        if not results:
            return {
                "answer": "I could not find grounded evidence in the demo documents.",
                "sources": [],
                "retrieval": {"k": k, "result_count": 0},
            }
        context = "\n\n".join(
            (
                f"[C{idx + 1}] {result.source} / "
                f"{result.metadata.get('heading')} / "
                f"{result.metadata.get('clause_id')}: {result.text}"
            )
            for idx, result in enumerate(results)
        )
        prompt = (
            "Answer this AEC code-compliance question using only the context. "
            "If evidence is incomplete, say what is missing.\n\n"
            f"Question: {question}\n\nContext:\n{context}"
        )
        citations = [self.format_citation(result, idx + 1) for idx, result in enumerate(results)]
        if getattr(self.provider, "name", "") == "mock-local-llm":
            answer = self._local_grounded_answer(citations)
        else:
            answer = self.provider.generate(
                prompt,
                system=(
                    "You are a cautious AEC design-standards assistant. "
                    "Use only the provided context and cite chunk IDs like [C1]."
                ),
            )
        return {
            "answer": answer,
            "sources": citations,
            "retrieval": {
                "k": k,
                "result_count": len(results),
                "top_score": citations[0]["score"] if citations else 0,
            },
        }

    def _local_grounded_answer(self, citations: list[dict[str, object]]) -> str:
        top_score = float(citations[0]["score"]) if citations else 0.0
        selected_citations = [
            citation
            for citation in citations
            if float(citation["score"]) >= max(0.08, top_score * 0.5)
        ]
        if not selected_citations:
            selected_citations = citations[:1]
        bullets = []
        for citation in selected_citations[:3]:
            excerpt = str(citation["excerpt"]).replace("\n", " ")
            bullets.append(
                "- {excerpt} [{citation_id}]".format(
                    excerpt=excerpt,
                    citation_id=citation["citation_id"],
                )
            )
        return (
            "Based on the synthetic demo guidance retrieved locally, review these items:\n"
            + "\n".join(bullets)
            + "\n\nThis is decision-support text only; a qualified reviewer would still "
            "check the governing jurisdiction, current code version, and project-specific constraints."
        )


def build_assistant_from_paths(paths: list[str | Path]) -> RAGAssistant:
    chunks: list[DocumentChunk] = []
    for path in paths:
        chunks.extend(load_markdown_chunks(path))
    return RAGAssistant(chunks)
