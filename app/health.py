from __future__ import annotations
from typing import Callable
from app.operations import self_test as operations_self_test


def _check_operations_registry() -> str:
    from app.operations import OPERATIONS
    if not OPERATIONS:
        raise RuntimeError("Реестр операций пуст")
    return "ok"

def _check_calculator_self_test() -> str:
    return operations_self_test()

HEALTH_CHECKS: dict[str, Callable[[], str]] = {
    "operations_registry": _check_operations_registry,
    "calculator_self_test": _check_calculator_self_test,
}