from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.extend([str(PROJECT_ROOT / "src"), str(REPO_ROOT)])

import streamlit as st

from mlops_model_serving_monitoring import detect_drift, generate_churn_data, train_churn_model

st.set_page_config(page_title="MLOps Model Serving", page_icon="AI", layout="wide")
st.title("MLOps Model Serving and Monitoring Platform")
data = generate_churn_data()
model, metrics = train_churn_model(data)
current = data.copy()
current["usage_score"] = current["usage_score"] * 0.6
st.subheader("Model metrics")
st.json(metrics)
st.subheader("Drift report")
st.json(detect_drift(data, current))
