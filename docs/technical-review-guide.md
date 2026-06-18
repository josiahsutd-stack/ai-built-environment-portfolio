# Technical Review Guide

This document is written for recruiters and technical reviewers. It summarizes what the flagship projects demonstrate, what is intentionally mocked or synthetic, and which implementation details are worth inspecting. The intended interpretation is: these are local, testable demos of engineering shape with clear production next steps, not inflated production claims.

## Flagship Projects

### Agentic Research Operations Assistant

- Review signal: planner-executor agent with local document retrieval, tool registry, per-tool traces, citations, memory, approval checkpoints, SQLite trace persistence, and trace evaluation.
- Architecture evidence: task -> plan -> tool registry/permissions -> retrieved evidence -> report -> human approval -> persisted trace -> trace eval.
- Engineering rationale: the agent keeps every step inspectable, permissioned, retryable, and auditable.
- Limitations to note: local documents only; no live web search or production workflow engine.
- Technical question supported: "How are hallucinations controlled?" Evidence in the project includes citations, retrieved context, approval checkpoints, tool traces, persisted runs, and eval findings.
- Production extension: PDF ingestion, web/search connectors, richer memory, role-based tool permissions, and richer eval suites.

### Multimodal VLM Visual QA Assistant

- Review signal: image QA workflow with mock mode, optional OpenAI-compatible hosted provider, structured JSON, confidence, uncertainty, and validation.
- Architecture evidence: image bytes -> validator -> provider abstraction -> hosted or mock response -> schema response -> history/UI.
- Engineering rationale: the workflow separates product behavior from the model dependency.
- Limitations to note: mock mode validates the interface but does not perform real visual reasoning; hosted mode requires a real API key and model access.
- Technical question supported: "How would this be evaluated?" Evidence to look for includes extraction accuracy, uncertainty calibration, visual hallucination cases, and schema validity.
- Production extension: OCR, region grounding, eval image sets, local model backends, and latency testing.

### MLOps Model Serving and Monitoring Platform

- Review signal: synthetic churn model with training, model artifact, FastAPI prediction schema, SQLite inference logging, drift checks, and monitoring dashboard.
- Architecture evidence: synthetic data -> training -> model artifact/metadata -> API -> prediction log -> drift report/history.
- Engineering rationale: the project shows deployment and monitoring shape without external services.
- Limitations to note: synthetic data, local model artifact, and lightweight drift checks.
- Technical question supported: "How is model quality monitored?" Evidence to look for includes inference schema checks, SQLite prediction logs, drift metrics, model metadata, and the planned path to delayed labels.
- Production extension: MLflow-compatible registry, alert thresholds, retraining workflows, and real delayed labels.

### LLM Evals and Guardrails Platform

- Review signal: eval cases for prompt injection, structured output validity, and citation coverage.
- Architecture evidence: eval case -> guardrail checks -> scores -> findings -> dashboard/API.
- Engineering rationale: deterministic baseline evals are easy to run in CI and easy to inspect.
- Limitations to note: transparent rules are not a full red-team program.
- Technical question supported: "How are LLM systems made more reliable?" Evidence in the project includes eval sets, regression checks, structured-output validation, prompt-injection checks, and monitoring surfaces.
- Production extension: prompt versioning, model-graded evals, persisted results, and CI gating.

## Secondary Project Review Signals

- AEC RAG Assistant: chunking, retrieval, citations, incomplete-evidence handling, and TF-IDF limitations versus embedding retrieval.
- LLM Evals Guardrails: prompt-injection checks, structured-output validation, citation checks, and eval-result schema.
- Reinforcement Learning Portfolio: environment design, reward shaping, policy baselines, and the distinction between simulation and optimization claims.
- Deep Learning Vision Lab: synthetic dataset generation, metrics, model-card discipline, and the path from baseline to PyTorch CNN/U-Net.
- Recommender Ranking Engine: popularity versus content-based recommendations, ranking metrics, and product-facing explanations.
- Time-Series Anomaly Forecasting: moving-average baseline, Isolation Forest, alert thresholds, and time-aware evaluation.
- Fine-Tuning LoRA Lab: dataset validation, LoRA configuration, mock training, and compute-aware workflow design.
- VLA Embodied Agent Simulator: language-to-action simulation, state/action traces, and honest hardware limitations.
- BIM Issue Detection Agent: deterministic rule checks before LLM explanation, issue reports, and AEC coordination workflow fit.
- Building Energy ML Pipeline: feature engineering, regression evaluation, model card, and energy-domain limitations.
