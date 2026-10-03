from __future__ import annotations

import math
from typing import Literal

from pydantic import BaseModel, Field, field_validator

OperationType = Literal["+", "-", "*", "/"]


class CalcRequest(BaseModel):
    a: float = Field(..., description="Первый операнд", examples=[10])
    b: float = Field(..., description="Второй операнд", examples=[5])
    operation: OperationType = Field(..., description="Операция", examples=["+"])

    model_config = {
        "json_schema_extra": {
            "example": {"a": 10, "b": 5, "operation": "+"}
        }
    }


class CalcResponse(BaseModel):
    a: float
    b: float
    operation: str
    result: float | None
    available_operations: list[str]

    @field_validator("result", mode="before")
    @classmethod
    def normalize_nonfinite(cls, v):
        if isinstance(v, float) and not math.isfinite(v):
            return None
        return v


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    message: str
    version: str
    checks: dict[str, str]
