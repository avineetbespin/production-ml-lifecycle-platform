from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "mlops_requests_total",
    "Total number of inference requests",
    ["endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "mlops_request_latency_seconds",
    "Latency of inference requests in seconds",
    ["endpoint"],
)
PREDICTION_COUNT = Counter(
    "mlops_prediction_total",
    "Total number of generated predictions",
    ["outcome"],
)
