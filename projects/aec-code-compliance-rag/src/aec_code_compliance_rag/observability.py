from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class QueryLogger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS query_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    corpus TEXT NOT NULL,
                    retrieval_mode TEXT NOT NULL,
                    question TEXT NOT NULL,
                    status TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    result_count INTEGER NOT NULL,
                    latency_ms INTEGER NOT NULL,
                    source_filters_json TEXT NOT NULL,
                    response_json TEXT NOT NULL
                )
                """)

    def log_query(
        self,
        *,
        corpus: str,
        retrieval_mode: str,
        question: str,
        response: dict[str, Any],
        latency_ms: int,
        source_filters: dict[str, Any] | None = None,
    ) -> int:
        retrieval = response.get("retrieval", {})
        with sqlite3.connect(self.path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO query_log (
                    created_at,
                    corpus,
                    retrieval_mode,
                    question,
                    status,
                    confidence,
                    result_count,
                    latency_ms,
                    source_filters_json,
                    response_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(UTC).isoformat(),
                    corpus,
                    retrieval_mode,
                    question,
                    str(response.get("status", "")),
                    str(response.get("confidence", "")),
                    int(retrieval.get("result_count", 0)),
                    latency_ms,
                    json.dumps(source_filters or {}, sort_keys=True),
                    json.dumps(response, sort_keys=True, default=str),
                ),
            )
            return int(cursor.lastrowid)

    def recent(self, *, limit: int = 20) -> list[dict[str, Any]]:
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, created_at, corpus, retrieval_mode, question, status,
                       confidence, result_count, latency_ms, source_filters_json
                FROM query_log
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
