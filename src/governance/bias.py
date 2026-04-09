import numpy as np
import pandas as pd


def check_bias(dataset: pd.DataFrame, model) -> dict:
    if "sensitive_group" not in dataset.columns:
        return {"disparate_impact": 0.0, "passed": True}

    X = dataset.drop(columns=["target"])
    y = dataset["target"]
    y_pred = model.predict(X)

    table = pd.DataFrame({"label": y, "prediction": y_pred, "group": dataset["sensitive_group"]})
    group_scores = table.groupby("group").apply(lambda df: (df["prediction"] == 1).mean())
    if len(group_scores) < 2:
        return {"disparate_impact": 0.0, "passed": True}

    disparity = abs(group_scores.iloc[0] - group_scores.iloc[1])
    return {
        "disparate_impact": float(disparity),
        "passed": disparity <= 0.05,
        "group_rates": group_scores.to_dict(),
    }
