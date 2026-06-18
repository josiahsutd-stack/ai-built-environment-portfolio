from __future__ import annotations

import pandas as pd


def detect_drift(
    reference: pd.DataFrame, current: pd.DataFrame, threshold: float = 0.2
) -> dict[str, object]:
    drifted: list[str] = []
    scores: dict[str, float] = {}
    for column in reference.select_dtypes("number").columns:
        if column not in current:
            continue
        ref_mean = float(reference[column].mean())
        cur_mean = float(current[column].mean())
        score = abs(cur_mean - ref_mean) / max(1.0, abs(ref_mean))
        scores[column] = round(score, 3)
        if score > threshold:
            drifted.append(column)
    return {"drifted_features": drifted, "scores": scores, "drift_detected": bool(drifted)}
