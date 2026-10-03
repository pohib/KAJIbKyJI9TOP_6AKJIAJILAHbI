from __future__ import annotations

import math
from typing import Literal

from pydantic import BaseModel, Field, field_validator

OperationType = Literal["+", "-", "*", "/", "sin", "cos"]


class CalcRequest(BaseModel):
    operation: OperationType = Field(
        ...,
        description=(
            "Операция. "
            "Бинарные (+ - * /) требуют оба операнда 'a' и 'b'. "
            "Унарные (sin, cos) используют только 'a', поле 'b' игнорируется."
        ),
        examples=["+", "sin"],
    )
    a: float = Field(
        ...,
        description=(
            "Первый операнд. "
            "Для бинарных операций — левый операнд. "
            "Для унарных (sin) — единственный аргумент."
        ),
        examples=[10],
    )
    b: float = Field(
        ...,
        description=(
            "Второй операнд. "
            "Обязателен для бинарных операций (+ - * /). "
            "Для унарных операций (sin) можно передать любое значение — "
            "оно будет проигнорировано."
        ),
        examples=[5],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"operation": "+", "a": 10, "b": 5},
                {"operation": "sin", "a": 0, "b": 0},
                {"operation": "cos", "a": 0, "b": 0},
            ]
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
