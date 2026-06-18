# LLM Evals and Guardrails Platform

Lightweight LLMOps platform for prompt-injection detection, structured-output validation, citation coverage checks, and regression-style evaluation.

## Problem

Production AI systems need tests for reliability, safety, and structured behavior, not only prompts.

## Demo

```bash
streamlit run projects/llm-evals-guardrails-platform/app.py
```

## Features

- Prompt injection detector
- JSON/structured-output validator
- Citation coverage score
- Eval case schema
- Dashboard and FastAPI `/evaluate` endpoint
- Local sample eval cases

## Tech Stack

Python, Streamlit, FastAPI, Pydantic-style schemas, pytest.

## Architecture

```mermaid
flowchart LR
  A["Eval case"] --> B["Guardrail checks"]
  B --> C["Metric scoring"]
  C --> D["Findings"]
  D --> E["Dashboard/API"]
```

## Limitations

- Rules are transparent baselines.
- Does not replace human review or full red-team evaluation.

## How I Would Improve This In Production

- Add model-graded evals, prompt version registry, SQLite persistence, and CI regression gates.

## What This Proves To Employers

LLMOps, guardrails, prompt-injection awareness, structured-output validation, and responsible AI engineering.

