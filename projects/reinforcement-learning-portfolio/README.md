# Reinforcement Learning Portfolio

RL project with warehouse inventory control and dynamic pricing simulators, baseline policies, reward design, and policy evaluation.

## Problem

Sequential decisions such as reordering or price changes require simulation, rewards, baselines, and evaluation before optimization claims are meaningful.

## Demo

```bash
streamlit run projects/reinforcement-learning-portfolio/app.py
```

## Features

- Inventory-control environment
- Dynamic-pricing environment
- Random and heuristic baselines
- Reward curves via local evaluation metrics
- Reproducible seeds
- Short local training/evaluation path

## Tech Stack

Python, NumPy-style environment design, Streamlit, pytest.

## Architecture

```mermaid
flowchart LR
  A["Environment state"] --> B["Policy"]
  B --> C["Action"]
  C --> D["Reward + next state"]
  D --> E["Evaluation metrics"]
```

## Limitations

- Lightweight custom environments rather than heavy RL libraries.
- No production pricing or inventory claims.

## How I Would Improve This In Production

- Add Gymnasium wrappers, DQN/PPO integrations, experiment tracking, and richer simulations.

## What This Proves To Employers

RL fundamentals, reward shaping, sequential decision-making, simulation, and applied optimization thinking.

