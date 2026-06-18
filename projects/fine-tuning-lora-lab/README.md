# Fine-Tuning and LoRA Lab

Compute-aware fine-tuning workflow for support-ticket classification with dataset generation, validation, split logic, LoRA config, mock training, and evaluation report.

## Problem

Fine-tuning projects often fail before training because datasets, validation, compute assumptions, and evaluation are unclear.

## Demo

```bash
streamlit run projects/fine-tuning-lora-lab/app.py
```

## Features

- Instruction dataset generator
- Dataset validation
- Train/validation split
- LoRA config structure
- Mock trainer requiring no GPU
- Clear path for real GPU training

## Tech Stack

Python, dataclasses, Streamlit, pytest, Hugging Face-compatible workflow structure.

## Architecture

```mermaid
flowchart LR
  A["Instruction dataset"] --> B["Validation"]
  B --> C["Split"]
  C --> D["LoRA config"]
  D --> E["Mock training report"]
```

## Limitations

- No real heavy fine-tuning is run locally.
- Mock trainer demonstrates workflow shape, not model adaptation performance.

## How I Would Improve This In Production

- Add tokenizer, PEFT/LoRA trainer, GPU instructions, model registry, and held-out evaluation.

## What This Proves To Employers

Fine-tuning workflow knowledge, dataset preparation, model adaptation planning, evaluation discipline, and responsible compute-aware engineering.

