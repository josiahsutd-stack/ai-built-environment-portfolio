# ruff: noqa: E402, I001
from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path
from time import perf_counter
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.extend([str(PROJECT_ROOT / "src"), str(REPO_ROOT)])

from aec_code_compliance_rag import (
    build_assistant_from_paths,
    downloaded_public_paths,
)  # noqa: E402
from aec_code_compliance_rag.observability import QueryLogger  # noqa: E402


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    k: int = Field(default=4, ge=1, le=10)
    retrieval_mode: str = "hybrid"
    source_filters: dict[str, Any] | None = None


class RetrieveRequest(BaseModel):
    question: str = Field(min_length=1)
    k: int = Field(default=4, ge=1, le=20)
    retrieval_mode: str = "hybrid"
    source_filters: dict[str, Any] | None = None


def _synthetic_docs() -> list[Path]:
    return sorted(
        [
            *(PROJECT_ROOT / "sample_data").glob("*.md"),
            *(PROJECT_ROOT / "sample_data").glob("*.pdf"),
        ]
    )


def _public_docs() -> list[Path]:
    return downloaded_public_paths(PROJECT_ROOT / "public_sources" / "downloaded")


def _corpus_config() -> tuple[str, list[Path], Path | None]:
    corpus = os.getenv("AEC_RAG_CORPUS", "synthetic")
    if corpus == "public":
        docs = _public_docs()
        if not docs:
            raise RuntimeError(
                "Public corpus missing. Run scripts/download_public_sources.py first."
            )
        return corpus, docs, PROJECT_ROOT / "public_sources" / "downloaded" / "source_manifest.json"
    return "synthetic", _synthetic_docs(), None


@lru_cache(maxsize=8)
def _assistant(retrieval_mode: str):
    _corpus, docs, manifest_path = _corpus_config()
    return build_assistant_from_paths(
        docs, manifest_path=manifest_path, retrieval_mode=retrieval_mode
    )


app = FastAPI(title="AEC Code Compliance RAG API", version="0.1.0")
logger = QueryLogger(PROJECT_ROOT / "demo_outputs" / "query_log.sqlite")


@app.get("/health")
def health() -> dict[str, object]:
    corpus, docs, _manifest_path = _corpus_config()
    return {"status": "ok", "corpus": corpus, "document_count": len(docs)}


@app.get("/sources")
def sources(retrieval_mode: str = "hybrid") -> list[dict[str, str]]:
    return _assistant(retrieval_mode).source_catalog()


@app.post("/query")
def query(request: QueryRequest) -> dict[str, object]:
    corpus, _docs, _manifest_path = _corpus_config()
    started = perf_counter()
    try:
        response = _assistant(request.retrieval_mode).answer(
            request.question,
            k=request.k,
            source_filters=request.source_filters,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    latency_ms = int((perf_counter() - started) * 1000)
    log_id = logger.log_query(
        corpus=corpus,
        retrieval_mode=request.retrieval_mode,
        question=request.question,
        response=response,
        latency_ms=latency_ms,
        source_filters=request.source_filters,
    )
    response["api"] = {"latency_ms": latency_ms, "query_log_id": log_id}
    return response


@app.post("/retrieve")
def retrieve(request: RetrieveRequest) -> dict[str, object]:
    try:
        results = _assistant(request.retrieval_mode).retrieve(
            request.question,
            k=request.k,
            source_filters=request.source_filters,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "count": len(results),
        "results": [
            {
                "source": result.source,
                "score": result.score,
                "metadata": result.metadata,
                "excerpt": result.text[:600],
            }
            for result in results
        ],
    }


@app.get("/logs/recent")
def recent_logs(limit: int = 20) -> list[dict[str, Any]]:
    return logger.recent(limit=limit)
