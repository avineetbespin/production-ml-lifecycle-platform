from sklearn.metrics import accuracy_score, f1_score


class BenchmarkResult:
    def __init__(self, accuracy: float, f1: float):
        self.accuracy = accuracy
        self.f1 = f1

    def exceeds(self, other: "BenchmarkResult", threshold: float) -> bool:
        return (self.accuracy - other.accuracy) >= threshold or (self.f1 - other.f1) >= threshold


def evaluate_model(model, X, y) -> BenchmarkResult:
    preds = model.predict(X)
    return BenchmarkResult(
        accuracy=accuracy_score(y, preds),
        f1=f1_score(y, preds, average="binary"),
    )


def compare_models(candidate, champion, X, y, threshold: float) -> dict:
    candidate_metrics = evaluate_model(candidate, X, y)
    champion_metrics = evaluate_model(champion, X, y)
    return {
        "candidate": candidate_metrics,
        "champion": champion_metrics,
        "pass_threshold": candidate_metrics.exceeds(champion_metrics, threshold),
    }
