from __future__ import annotations

from pathlib import Path

from .chunking import DocumentChunk, chunk_pdf_pages


def _normalize_extracted_text(text: str) -> str:
    replacements = {
        "\u00e2\u20ac\u0153": '"',
        "\u00e2\u20ac\u009d": '"',
        "\u00e2\u20ac\u02dc": "'",
        "\u00e2\u20ac\u2122": "'",
        "\u00e2\u20ac\u201c": "-",
        "\u00e2\u20ac\u201d": "-",
        "\u00c2 ": " ",
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2013": "-",
        "\u2014": "-",
    }
    normalized = text
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def _read_pdf_pages(path: Path) -> list[tuple[int, str]]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - exercised only in missing-dep envs
        raise RuntimeError(
            "PDF ingestion requires pypdf. Install project requirements with "
            "`python -m pip install -r requirements.txt`."
        ) from exc

    reader = PdfReader(str(path))
    pages: list[tuple[int, str]] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = _normalize_extracted_text(page.extract_text() or "")
        if text.strip():
            pages.append((page_number, text))
    return pages


def load_pdf_chunks(
    path: str | Path,
    *,
    max_words: int = 110,
    metadata_overrides: dict[str, object] | None = None,
) -> list[DocumentChunk]:
    target = Path(path)
    return chunk_pdf_pages(
        _read_pdf_pages(target),
        source=target.name,
        max_words=max_words,
        metadata_overrides=metadata_overrides,
    )
