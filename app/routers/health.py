from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.config import APP_NAME, APP_VERSION
from app.health import HEALTH_CHECKS
from app.operations import AVAILABLE_OPERATIONS
from app.schemas import HealthResponse

router = APIRouter(tags=["health"])

@router.get("/")
def root() -> dict:
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "работает как негор",
        "available_operations": AVAILABLE_OPERATIONS,
    }

@router.get(
    "/health",
    response_model=HealthResponse,
    responses={503: {"description": "Сервис В С Е"}},
)
def health() -> HealthResponse:
    results: dict[str, str] = {}
    failed: list[str] = []

    for name, check in HEALTH_CHECKS.items():
        try:
            results[name] = check()
        except Exception as exc:
            results[name] = f"error: {exc}"
            failed.append(name)

    payload = HealthResponse(
        status="ok" if not failed else "degraded",
        message=(
            "Сервис работает пушечно четенько кефтемешечно"
            if not failed
            else f"Провалены проверки: {', '.join(failed)}"
        ),
        version=APP_VERSION,
        checks=results,
    )

    if failed:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=payload.model_dump(),
        )
    return payload
