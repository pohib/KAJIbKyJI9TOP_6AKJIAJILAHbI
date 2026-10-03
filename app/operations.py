from __future__ import annotations

import math
import operator
from collections.abc import Callable

OPERATIONS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "sin": lambda a, _b: math.sin(a),
    "cos": lambda a, _b: math.cos(a),
}

AVAILABLE_OPERATIONS: list[str] = list(OPERATIONS.keys())


def apply_operation(symbol: str, a: float, b: float) -> float:
    return OPERATIONS[symbol](a, b)


_SELF_TEST_SAMPLES: dict[str, tuple[float, float, float]] = {
    "+": (2.0, 3.0, 5.0),
    "-": (5.0, 3.0, 2.0),
    "*": (2.0, 3.0, 6.0),
    "/": (6.0, 3.0, 2.0),
    "sin": (0.0, 0.0, 0.0),
    "cos": (0.0, 0.0, 1.0),
}


def self_test() -> str:
    missing = set(OPERATIONS) - set(_SELF_TEST_SAMPLES)

    if missing:
        raise RuntimeError(f"Нет self-test-примеров для операций: {missing}")

    if not OPERATIONS:
        raise RuntimeError("Реестр операций пуст")

    for symbol, func in OPERATIONS.items():
        if not callable(func):
            raise RuntimeError(f"Операция '{symbol}' не вызываема")

    for symbol, (a, b, expected) in _SELF_TEST_SAMPLES.items():
        if symbol not in OPERATIONS:
            raise RuntimeError(f"Отсутствует операция '{symbol}'")
        got = OPERATIONS[symbol](a, b)
        if not math.isclose(got, expected, abs_tol=1e-9):
            raise RuntimeError(
                f"Тест не пройден для '{symbol}': "
                f"{a} {symbol} {b} = {got}, ожидалось {expected}"
            )
    return "ok"
