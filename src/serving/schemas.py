from typing import List

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: List[float] = Field(..., description="Feature vector for the model")


class PredictResponse(BaseModel):
    prediction: int
    probabilities: List[float]
    model_version: str


class HealthResponse(BaseModel):
    status: str
