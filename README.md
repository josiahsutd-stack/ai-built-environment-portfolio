# Applied and General AI Engineering Portfolio

AI engineer focused on applied AI systems, LLM agents, multimodal AI, machine learning, and automation - with a unique background in architecture and the built environment.

This portfolio combines domain-specific AI for the built environment with general AI engineering projects across VLMs, agents, reinforcement learning, deep learning, MLOps, recommender systems, time-series ML, and fine-tuning workflows.

## Recommended Review Path For Recruiters

If you are reviewing my portfolio, I recommend starting with the AEC Code Compliance RAG Assistant. It is the primary flagship because it best combines my AI engineering skills with my built-environment background.

- [AEC Code Compliance RAG Assistant](projects/aec-code-compliance-rag/README.md) - source-grounded AEC RAG with chunk metadata, retrieval evaluation, citation quality, demo outputs, architecture docs, tests, and explicit limitations.

Strong supporting systems:

- [Agentic Research Operations Assistant](projects/agentic-research-ops-assistant/README.md) - planner/executor agent, tool registry, local RAG, citations, approval checkpoints, SQLite trace persistence, and trace evaluation.
- [MLOps Model Serving and Monitoring Platform](projects/mlops-model-serving-monitoring/README.md) - training, model artifacts, FastAPI serving, SQLite inference logs, drift history, Docker, and tests.
- [Multimodal VLM Visual QA Assistant](projects/multimodal-vlm-visual-qa/README.md) - VLM product workflow with mock mode plus an optional OpenAI-compatible vision-provider path.

## Why I Structured This Portfolio This Way

I designed this repository for two kinds of hiring review:

- If you are hiring for applied AI or LLM engineering, start with the AEC RAG project, then review the agent, MLOps, and VLM projects as supporting range.
- If you are hiring for built-environment, robotics, or embodied AI work, review the AEC document system first, then BIM QA, construction progress, energy modeling, spatial design, and construction robotics projects.
- I kept every project runnable locally with synthetic data or mock providers so you can inspect the engineering without needing private datasets, paid APIs, or hidden infrastructure.

## Flagship Project

| Project | Why it is featured | Evidence to inspect |
| --- | --- | --- |
| [AEC Code Compliance RAG](projects/aec-code-compliance-rag/README.md) | Best match between applied AI engineering and built-environment domain knowledge. | Chunk metadata, citations, retrieval eval, sample questions, demo outputs, architecture docs, tests, no-result handling, limitations. |

## Secondary Experiments

These projects broaden the portfolio and support the main AEC RAG signal.

| Area | Projects |
| --- | --- |
| Built-environment AI | Construction Progress CV, BIM Issue Detection Agent, Building Energy ML, Spatial Design Recommender, AI + AEC Job Fit Analyzer |
| Construction robotics / embodied AI | Construction Robot Task Planner, Site Robot Safety Monitor, VLA Embodied Agent Simulator |
| General AI/ML systems | Agentic Research Ops, MLOps Serving Monitoring, Multimodal VLM Visual QA, LLM Evals Guardrails, Reinforcement Learning Portfolio, Deep Learning Vision Lab, Recommender Ranking Engine, Time-Series Anomaly Forecasting, Fine-Tuning LoRA Lab |

## AI For The Built Environment

These projects preserve the differentiator: AI plus architecture, AEC, construction, BIM, energy, spatial design, and construction robotics.

- AEC Code Compliance RAG Assistant (primary flagship)
- Construction Progress Computer Vision Tracker
- BIM / Drawing Issue Detection Agent
- AI + AEC Job Fit Analyzer
- Building Energy Prediction ML Pipeline
- Spatial Design Recommendation Engine
- Construction Robot Task Planner
- Site Robot Safety Monitor

## General AI Engineering Projects

- Multimodal VLM Visual QA Assistant
- Agentic Research Operations Assistant
- VLA Embodied Agent Simulator
- Reinforcement Learning Portfolio
- Deep Learning Vision Lab
- LLM Evals and Guardrails Platform
- MLOps Model Serving and Monitoring Platform
- Recommender System Ranking Engine
- Time-Series Anomaly Detection and Forecasting
- Fine-Tuning and LoRA Lab

## Skills Coverage Matrix

See [docs/skills-matrix.md](docs/skills-matrix.md), [docs/role-to-project-map.md](docs/role-to-project-map.md), and [portfolio-site/pages/skills-matrix.html](portfolio-site/pages/skills-matrix.html).

## Quickstart

```bash
python scripts/setup.py
python scripts/verify.py
```

`scripts/setup.py` creates `.venv` using the correct Windows/macOS/Linux path. Use
`python scripts/setup.py --no-venv` to install into the current Python environment instead.

## Run Tests And Quality Checks

```bash
python -m black --check .
python -m ruff check .
python scripts/check_repo_health.py
python scripts/run_smoke_tests.py
python -m pytest
python scripts/check_project_docs.py
python scripts/verify.py
```

The Makefile provides the same common checks where `make` is available:

```bash
make setup
make verify
make health
make smoke
make test
```

## Reviewer Guides

- [How to review this portfolio](docs/how-to-review-this-portfolio.md)
- [Technical review guide](docs/technical-review-guide.md)
- [Repository review metadata](docs/repository-review-metadata.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Repo audit](docs/repo-audit.md)
- [Project roadmap](docs/project-roadmap.md)

## Portfolio Site

Open [portfolio-site/index.html](portfolio-site/index.html), or run:

```bash
python -m http.server 8080 --directory portfolio-site
```

## Docker Example

Build project images from the repository root:

```bash
docker build -f projects/mlops-model-serving-monitoring/Dockerfile -t ai-portfolio-mlops .
docker run --rm -p 8000:8000 ai-portfolio-mlops
```

Use the same `docker build -f projects/<project>/Dockerfile -t <name> .` pattern for projects with Dockerfiles.

## Repository Structure

```text
.
|-- profile-readme.md
|-- portfolio-site/
|-- projects/
|   |-- aec-code-compliance-rag/
|   |-- construction-progress-cv/
|   |-- bim-issue-detection-agent/
|   |-- building-energy-ml-pipeline/
|   |-- construction-robot-task-planner/
|   |-- multimodal-vlm-visual-qa/
|   |-- agentic-research-ops-assistant/
|   |-- vla-embodied-agent-simulator/
|   |-- reinforcement-learning-portfolio/
|   |-- deep-learning-vision-lab/
|   |-- llm-evals-guardrails-platform/
|   |-- mlops-model-serving-monitoring/
|   |-- recommender-system-ranking-engine/
|   |-- time-series-anomaly-forecasting/
|   `-- fine-tuning-lora-lab/
|-- shared/
|-- docs/
|-- scripts/
`-- tests/
```

## Roadmap

See [docs/project-roadmap.md](docs/project-roadmap.md) and [docs/project-priority-roadmap.md](docs/project-priority-roadmap.md).

## Synthetic And Mock Notes

- All data is synthetic/demo data unless explicitly stated otherwise.
- LLM/VLM projects run in mock mode without paid APIs; the VLM project also supports an optional OpenAI-compatible hosted provider when configured.
- VLA and robotics projects are simulations, not real robot deployments.
- Fine-tuning uses a mock training path locally and documents where real GPU training would fit.
- AEC outputs are not legal, code, engineering, or professional compliance advice.
- No production users, clients, employers, or performance claims are fabricated.

## Contact

- GitHub: `https://github.com/josiahsutd-stack`
- LinkedIn: listed in application materials
- Email: listed in application materials
