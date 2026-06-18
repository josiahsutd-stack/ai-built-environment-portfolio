from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.extend([str(PROJECT_ROOT / "src"), str(REPO_ROOT)])

import streamlit as st

from fine_tuning_lora_lab import generate_instruction_dataset, mock_lora_train, validate_dataset

st.set_page_config(page_title="Fine-Tuning LoRA Lab", page_icon="AI", layout="wide")
st.title("Fine-Tuning and LoRA Lab")
rows = generate_instruction_dataset()
st.subheader("Dataset validation")
st.json(validate_dataset(rows))
st.subheader("Mock training report")
st.json(mock_lora_train(rows))
