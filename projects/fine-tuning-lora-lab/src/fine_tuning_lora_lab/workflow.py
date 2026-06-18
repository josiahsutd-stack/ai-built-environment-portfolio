from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LoRAConfig:
    base_model: str = "small-local-or-remote-model-placeholder"
    rank: int = 8
    alpha: int = 16
    task: str = "support_ticket_classification"


def generate_instruction_dataset() -> list[dict[str, str]]:
    labels = ["billing", "technical", "account", "sales"]
    return [
        {
            "instruction": "Classify this support ticket.",
            "input": f"Customer message about {label} issue number {idx}.",
            "output": label,
        }
        for idx in range(32)
        for label in [labels[idx % len(labels)]]
    ]


def validate_dataset(rows: list[dict[str, str]]) -> dict[str, object]:
    required = {"instruction", "input", "output"}
    invalid = [
        idx for idx, row in enumerate(rows) if not required.issubset(row) or not row["output"]
    ]
    labels = sorted({row.get("output", "") for row in rows if row.get("output")})
    return {
        "valid": not invalid and bool(rows),
        "invalid_rows": invalid,
        "labels": labels,
        "row_count": len(rows),
    }


def split_dataset(
    rows: list[dict[str, str]], train_ratio: float = 0.75
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    split = int(len(rows) * train_ratio)
    return rows[:split], rows[split:]


def mock_lora_train(
    rows: list[dict[str, str]], config: LoRAConfig | None = None
) -> dict[str, object]:
    validation = validate_dataset(rows)
    if not validation["valid"]:
        raise ValueError("Dataset failed validation.")
    config = config or LoRAConfig()
    train, val = split_dataset(rows)
    return {
        "mode": "mock_training_no_gpu_required",
        "base_model": config.base_model,
        "rank": config.rank,
        "train_rows": len(train),
        "validation_rows": len(val),
        "eval_accuracy_placeholder": 0.78,
    }
