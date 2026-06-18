# Architecture

This project is a local, synthetic-data RAG assistant for AEC guidance. It is designed to be inspectable by recruiters and technical reviewers, not to provide real compliance advice.

## System Flow

```mermaid
flowchart LR
  A["Synthetic markdown guidance"] --> B["Section-aware chunker"]
  B --> C["Chunk metadata contract"]
  C --> D["Local TF-IDF retrieval store"]
  Q["Reviewer question"] --> D
  D --> E["Top-k chunks with scores"]
  E --> F["Grounded answer builder"]
  E --> G["Citation formatter"]
  F --> H["Answer"]
  G --> H
  D --> I["Retrieval evaluator"]
  I --> J["demo_outputs"]
```

## Module Boundaries

| Area | File | Responsibility |
| --- | --- | --- |
| Chunking | `src/aec_code_compliance_rag/chunking.py` | Splits markdown by headings, preserves page markers, and emits chunk metadata. |
| Assistant | `src/aec_code_compliance_rag/assistant.py` | Builds the retrieval store, handles questions, formats citations, and returns no-result responses. |
| Evaluation | `src/aec_code_compliance_rag/evaluation.py` | Loads evaluation cases and computes retrieval metrics. |
| Evaluation CLI | `evaluate_retrieval.py` | Runs the evaluator and writes reviewer artifacts in `demo_outputs/`. |
| Demo UI | `app.py` | Streamlit interface for local question answering and citation inspection. |

## Data Contract

Every retrieved chunk carries this metadata:

| Field | Meaning |
| --- | --- |
| `source` | Original demo document filename. |
| `section` | Markdown section title used for retrieval grouping. |
| `heading` | Human-readable heading shown in citations. |
| `clause_id` | Deterministic synthetic clause identifier derived from the heading. |
| `page` | Optional demo page marker from markdown comments. |
| `chunk_id` | Stable chunk identifier for tests, evals, and citations. |
| `start_word` / `end_word` | Word offsets within the section body. |

The current corpus is markdown, so page values come from comments such as `<!-- page: 2 -->`. A production extension would replace this with PDF parser output and versioned source metadata.

## Retrieval Design

The retriever uses `shared.ai.TfidfVectorStore` to keep the project runnable without paid APIs, local model downloads, or external infrastructure. This is intentionally transparent: reviewers can inspect the exact chunk text, score, metadata, and citation.

In a production path, the same assistant boundary could support:

- BM25 plus embedding hybrid retrieval.
- Cross-encoder or LLM reranking.
- Jurisdiction, discipline, document type, and code-year filters.
- Versioned indexes for superseded and current clauses.

## Citation Design

Citations are structured dictionaries, not just rendered strings. Each citation includes:

- `citation_id`, for answer references such as `[C1]`.
- `source`, `heading`, `clause_id`, `page`, and `chunk_id`.
- `score`, so reviewers can see retrieval confidence.
- `excerpt`, so the answer evidence is visible.
- `reference`, a readable citation label.

This makes citations easy to display in Streamlit, test in pytest, and export in demo outputs.

## No-Result Handling

The assistant returns a no-evidence answer when:

- The question is empty.
- Retrieval finds no chunks above the score threshold.

For compliance-oriented workflows, this behavior is more important than always generating a fluent answer.

## Production Extension Points

The current project is intentionally local and synthetic. A serious applied extension would add:

- PDF ingestion with page extraction and clause parsing.
- Source document versioning and jurisdiction metadata.
- Embedding retrieval, BM25, reranking, and filterable search.
- Answer-faithfulness evaluation against retrieved chunks.
- Human approval workflow for compliance-sensitive responses.
- Monitoring for no-result rate, citation coverage, low-score answers, and stale documents.
