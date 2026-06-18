# Recommender System Ranking Engine

Recommendation engine for AI courses/jobs/projects with popularity baseline, content-based ranking, evaluation metrics, API, and demo.

## Problem

Recommendation products need retrieval, ranking, explanations, and metrics, not just a nearest-neighbor call.

## Demo

```bash
streamlit run projects/recommender-system-ranking-engine/app.py
```

## Features

- Synthetic user-item interactions
- Content-based ranking with TF-IDF
- Popularity baseline
- Precision@k and NDCG@k
- FastAPI `/recommend`
- Recommendation explanations through tags and scores

## Tech Stack

Python, pandas, scikit-learn, FastAPI, Streamlit, pytest.

## Architecture

```mermaid
flowchart LR
  A["Catalog + interactions"] --> B["Retrieval baseline"]
  A --> C["Content ranking"]
  C --> D["Metrics"]
  D --> E["Demo/API"]
```

## Limitations

- Small synthetic dataset.
- Collaborative filtering/two-tower models are future extensions.

## How I Would Improve This In Production

- Add matrix factorization, two-tower retrieval, online feedback, and ranking experiments.

## What This Proves To Employers

Recommender systems, embeddings, ranking metrics, applied ML evaluation, and product thinking.

