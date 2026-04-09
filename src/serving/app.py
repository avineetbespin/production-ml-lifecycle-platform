import os
import time

import mlflow
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from src.common.config import settings
from src.serving.health import router as health_router
from src.serving.logging import get_json_logger, log_structured
from src.serving.metrics import REQUEST_COUNT, REQUEST_LATENCY, PREDICTION_COUNT
from src.serving.schemas import PredictRequest, PredictResponse


app = FastAPI(
    title="MLOps Model Serving API",
    description="FastAPI wrapper serving a production-ready ML model with observability and health probes.",
)
app.include_router(health_router)
logger = get_json_logger()

MODEL_URI = os.getenv("MODEL_URI", f"models:/{settings.MODEL_NAME}/{settings.PRODUCTION_STAGE}")
MODEL = None
MODEL_VERSION = None


def load_model():
    global MODEL, MODEL_VERSION
    try:
        MODEL = mlflow.pyfunc.load_model(MODEL_URI)
        MODEL_VERSION = MODEL.metadata.get("run_id", "unknown")
        logger.info(f"Loaded ML model from {MODEL_URI}")
    except Exception as exc:
        MODEL = None
        MODEL_VERSION = "unavailable"
        logger.warning(f"Unable to load model from {MODEL_URI}: {exc}")


@app.on_event("startup")
def startup_event():
    load_model()


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        REQUEST_COUNT.labels(endpoint=request.url.path, status="error").inc()
        log_structured(logger, "request_error", path=request.url.path, error=str(exc))
        raise
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    REQUEST_COUNT.labels(endpoint=request.url.path, status=str(response.status_code)).inc()
    return response


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    features = [payload.features]
    try:
        preds = MODEL.predict(features)
        probs = MODEL.predict_proba(features).tolist()[0]
    except Exception as exc:
        log_structured(logger, "prediction_error", error=str(exc), features=payload.features)
        raise HTTPException(status_code=422, detail="Invalid feature vector for model inference")

    response = PredictResponse(
        prediction=int(preds[0]),
        probabilities=[float(p) for p in probs],
        model_version=MODEL_VERSION,
    )
    PREDICTION_COUNT.labels(outcome=str(response.prediction)).inc()
    log_structured(logger, "prediction_success", prediction=response.prediction, model_version=response.model_version)
    return response


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
