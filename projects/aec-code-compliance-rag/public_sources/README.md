# Public Source Corpus

This directory contains metadata for an optional Singapore public-document corpus.

Run:

```bash
python projects/aec-code-compliance-rag/scripts/download_public_sources.py
```

Downloaded PDFs and the generated `source_manifest.json` are written under `downloaded/`, which is ignored by Git. The committed `sources.json` file records source provenance and allowed-use notes.
