# MLOps Model Serving and Monitoring Platform

Synthetic churn-risk MLOps demo with model training, prediction schema, FastAPI serving, inference-style validation, drift detection, and Streamlit monitoring.

## Problem

ML systems need serving, schema checks, logging, drift detection, and model lifecycle thinking beyond notebooks.

## Demo

```bash
streamlit run projects/mlops-model-serving-monitoring/app.py
```

## Features

- Synthetic churn dataset
- scikit-learn training pipeline
- FastAPI `/predict` and `/metrics`
- Drift detection
- Model version metadata
- Dockerfile

## Tech Stack

Python, pandas, scikit-learn, FastAPI, Streamlit, Docker, pytest.

## Architecture

```mermaid
flowchart LR
  A["Synthetic data"] --> B["Training pipeline"]
  B --> C["Model registry metadata"]
  C --> D["Prediction API"]
  D --> E["Monitoring + drift detection"]
```

## Limitations

- Synthetic customer data only.
- Not a real financial or customer-retention decision system.

## How I Would Improve This In Production

- Add SQLite inference logging, model registry artifacts, MLflow-compatible metadata, and alerting.

## What This Proves To Employers

MLOps, model serving, monitoring, drift detection, API engineering, and production ML thinking.

