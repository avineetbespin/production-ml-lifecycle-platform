from fastapi.testclient import TestClient

from src.serving.app import app


client = TestClient(app)


def test_predict_rejects_broken_schema():
    response = client.post("/predict", json={"data": [1, 2, 3]})
    assert response.status_code == 422
    assert "features" in response.text


def test_predict_rejects_invalid_types():
    response = client.post("/predict", json={"features": ["a", "b", "c"]})
    assert response.status_code == 422


def test_readiness_health_endpoints():
    health = client.get("/health")
    ready = client.get("/ready")
    assert health.status_code == 200 and health.json()["status"] == "healthy"
    assert ready.status_code == 200 and ready.json()["status"] == "ready"
