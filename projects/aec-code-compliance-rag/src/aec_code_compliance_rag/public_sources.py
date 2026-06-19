from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._parts: list[str] = []
        self._current_href: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in {"h1", "h2", "h3"}:
            self._parts.append("\n\n## ")
        elif tag in {"p", "li", "tr", "div", "section", "article"}:
            self._parts.append("\n")
        elif tag == "a":
            href = dict(attrs).get("href")
            self._current_href = href

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "a":
            self._current_href = None

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = " ".join(data.split())
        if not text:
            return
        if self._current_href and self._current_href.startswith(("http://", "https://")):
            text = f"{text} ({self._current_href})"
        self._parts.append(text)
        self._parts.append(" ")

    def text(self) -> str:
        raw_text = "".join(self._parts)
        raw_text = re.sub(r"[ \t]+", " ", raw_text)
        raw_text = re.sub(r"\n{3,}", "\n\n", raw_text)
        return raw_text.strip()


@dataclass(frozen=True)
class DownloadedSource:
    source: str
    path: Path
    bytes_written: int
    content_type: str
    url: str


def public_sources_root(project_root: str | Path | None = None) -> Path:
    if project_root is not None:
        return Path(project_root) / "public_sources"
    return Path(__file__).resolve().parents[2] / "public_sources"


def load_public_source_definitions(
    source_file: str | Path | None = None,
) -> dict[str, Any]:
    target = Path(source_file) if source_file else public_sources_root() / "sources.json"
    return json.loads(target.read_text(encoding="utf-8"))


def public_download_dir(source_file: str | Path | None = None) -> Path:
    source_path = Path(source_file) if source_file else public_sources_root() / "sources.json"
    payload = load_public_source_definitions(source_path)
    return source_path.parent / str(payload.get("download_dir", "downloaded"))


def downloaded_public_paths(download_dir: str | Path | None = None) -> list[Path]:
    target = Path(download_dir) if download_dir else public_download_dir()
    if not target.exists():
        return []
    return sorted([*target.glob("*.pdf"), *target.glob("*.md")])


def download_public_sources(
    source_file: str | Path | None = None,
    *,
    force: bool = False,
    timeout_seconds: int = 90,
) -> dict[str, Any]:
    source_path = Path(source_file) if source_file else public_sources_root() / "sources.json"
    payload = load_public_source_definitions(source_path)
    download_dir = source_path.parent / str(payload.get("download_dir", "downloaded"))
    download_dir.mkdir(parents=True, exist_ok=True)

    downloaded_at = datetime.now(UTC).isoformat()
    records: list[DownloadedSource] = []
    manifest_rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for row in payload.get("sources", []):
        source_name = str(row["source"])
        destination = download_dir / source_name
        try:
            record = _download_one(
                row,
                destination=destination,
                force=force,
                downloaded_at=downloaded_at,
                timeout_seconds=timeout_seconds,
            )
            records.append(record)
            manifest_rows.append(
                {
                    **{
                        key: value
                        for key, value in row.items()
                        if key
                        in {
                            "source",
                            "title",
                            "publisher",
                            "source_url",
                            "source_type",
                            "jurisdiction",
                            "code_year",
                            "document_version",
                            "superseded",
                            "allowed_use",
                            "rights",
                            "source_note",
                        }
                    },
                    "downloaded_at": downloaded_at,
                    "source": source_name,
                }
            )
        except Exception as exc:  # pragma: no cover - network failures vary
            failures.append({"source": source_name, "error": str(exc)})

    manifest_payload = {
        "note": "Generated from public_sources/sources.json. Downloaded files are local-only and not committed.",
        "generated_at": downloaded_at,
        "sources": manifest_rows,
    }
    (download_dir / "source_manifest.json").write_text(
        json.dumps(manifest_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    report = {
        "generated_at": downloaded_at,
        "download_dir": str(download_dir),
        "downloaded_count": len(records),
        "failure_count": len(failures),
        "downloaded": [
            {
                "source": record.source,
                "path": str(record.path),
                "bytes_written": record.bytes_written,
                "content_type": record.content_type,
                "url": record.url,
            }
            for record in records
        ],
        "failures": failures,
    }
    (source_path.parent / "download_report.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    return report


def _download_one(
    row: dict[str, Any],
    *,
    destination: Path,
    force: bool,
    downloaded_at: str,
    timeout_seconds: int,
) -> DownloadedSource:
    source_url = str(row["source_url"])
    if destination.exists() and not force:
        return DownloadedSource(
            source=destination.name,
            path=destination,
            bytes_written=destination.stat().st_size,
            content_type="existing",
            url=source_url,
        )

    request = urllib.request.Request(
        source_url,
        headers={"User-Agent": "ai-portfolio-local-review/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        content_type = response.headers.get("content-type", "")
        body = response.read()
        final_url = response.geturl()

    if destination.suffix.lower() == ".md":
        text = _html_to_markdown(body.decode("utf-8", errors="replace"), row, downloaded_at)
        destination.write_text(text, encoding="utf-8")
    else:
        destination.write_bytes(body)
    return DownloadedSource(
        source=destination.name,
        path=destination,
        bytes_written=destination.stat().st_size,
        content_type=content_type,
        url=final_url,
    )


def _html_to_markdown(html: str, row: dict[str, Any], downloaded_at: str) -> str:
    parser = _VisibleTextParser()
    parser.feed(html)
    title = str(row.get("title", row["source"]))
    metadata_lines = [
        f"title: {title}",
        f"document_id: {row.get('document_id', Path(str(row['source'])).stem)}",
        f"jurisdiction: {row.get('jurisdiction', 'singapore')}",
        f"code_year: {row.get('code_year', '')}",
        f"document_version: {row.get('document_version', '')}",
        f"superseded: {str(row.get('superseded', False)).lower()}",
        f"source_type: {row.get('source_type', 'html')}",
        f"allowed_use: {row.get('allowed_use', '')}",
        f"publisher: {row.get('publisher', '')}",
        f"source_url: {row.get('source_url', '')}",
        f"rights: {row.get('rights', '')}",
        f"downloaded_at: {downloaded_at}",
        f"source_note: {row.get('source_note', '')}",
    ]
    return (
        "\n".join(metadata_lines)
        + "\n\n"
        + f"# {title}\n\n"
        + "Official public page converted to text for local retrieval review. "
        + "Verify against the source URL before relying on the content.\n\n"
        + parser.text()
        + "\n"
    )
