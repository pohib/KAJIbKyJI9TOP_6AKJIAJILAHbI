from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.operations import AVAILABLE_OPERATIONS, apply_operation
from app.schemas import CalcRequest, CalcResponse

router = APIRouter(tags=["calc"])


@router.post(
    "/calculate",
    response_model=CalcResponse,
    responses={400: {"description": "Некорректная операция"}},
)
def calculate(data: CalcRequest) -> CalcResponse:
    if data.operation == "/" and data.b == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Деление на ноль ьратишка",
        )

    result = apply_operation(data.operation, data.a, data.b)

    return CalcResponse(
        a=data.a,
        b=data.b,
        operation=data.operation,
        result=result,
        available_operations=AVAILABLE_OPERATIONS,
    )
