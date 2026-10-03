from __future__ import annotations

from fastapi import FastAPI

from app.config import APP_DESCRIPTION, APP_NAME, APP_VERSION
from app.operations import AVAILABLE_OPERATIONS
from app.routers import calc, health

app = FastAPI(
    title=APP_NAME,
    description=f"{APP_DESCRIPTION}.\n\nДоступные операции: {', '.join(AVAILABLE_OPERATIONS)}",
    version=APP_VERSION,
)

app.include_router(health.router)
app.include_router(calc.router)
