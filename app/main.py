from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal


app = FastAPI(
    title="Calc API",
    description="""
    апишка калькулятор баклажаны
    Доступные операции:
    + — сложение
    - — вычитание
    * — умножение
    / — деление
    """,
    version="1.0"
)


class CalcRequest(BaseModel):
    a: float
    b: float
    operation: Literal["+", "-", "*", "/"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "a": 10,
                "b": 5,
                "operation": "+"
            }
        }
    }


class CalcResponse(BaseModel):
    a: float
    b: float
    operation: str
    result: float
    available_operations: list[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "a": 10,
                "b": 5,
                "operation": "+",
                "result": 15,
                "available_operations": [
                    "+",
                    "-",
                    "*",
                    "/"
                ]
            }
        }
    }


@app.get("/")
def root():
    try:
        return {
            "name": "CalcAPI",
            "status": "работает",
            "message": "API работает",
            "available_operations": ["+", "-", "*", "/"]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Не удалось получить статус API"
        )


@app.get("/health")
def health():
    try:
        return {
            "status": "ok",
            "message": "Сервис работает корректно"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Сервис недоступен"
        )


@app.post("/calculate", response_model=CalcResponse)
def calculate(data: CalcRequest):
    try:
        if data.operation == "+":
            result = data.a + data.b

        elif data.operation == "-":
            result = data.a - data.b

        elif data.operation == "*":
            result = data.a * data.b

        elif data.operation == "/":
            if data.b == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Деление на ноль ьратишка"
                )

            result = data.a / data.b

        else:
            raise HTTPException(
                status_code=400,
                detail="Неизвестная операция"
            )

        return CalcResponse(
            a=data.a,
            b=data.b,
            operation=data.operation,
            result=result,
            available_operations=["+", "-", "*", "/"]
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Ошибка при выполнении вычисления"
        )
