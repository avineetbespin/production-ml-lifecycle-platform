from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["liveness"])
def health():
    return {"status": "healthy"}


@router.get("/ready", tags=["readiness"])
def ready():
    return {"status": "ready"}
