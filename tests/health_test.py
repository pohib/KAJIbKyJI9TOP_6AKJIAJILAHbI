from __future__ import annotations

from fastapi.testclient import TestClient

from app import operations
from app.operations import AVAILABLE_OPERATIONS, apply_operation, self_test


def test_root_reports_actual_operations(client: TestClient):
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "CalcAPI"
    assert body["available_operations"] == AVAILABLE_OPERATIONS


def test_health_ok(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["checks"]["operations_registry"] == "ok"
    assert body["checks"]["calculator_self_test"] == "ok"
    assert body["version"]


def test_health_returns_503_when_registry_broken(client: TestClient, monkeypatch):
    monkeypatch.setattr(operations, "OPERATIONS", {}, raising=True)
    r = client.get("/health")
    assert r.status_code == 503
    body = r.json()["detail"]
    assert body["status"] == "degraded"
    assert "operations_registry" in body["message"]


def test_health_returns_503_when_self_test_fails(client: TestClient, monkeypatch):
    broken = dict(operations.OPERATIONS)
    broken["+"] = lambda a, b: a - b
    monkeypatch.setattr(operations, "OPERATIONS", broken, raising=True)
    r = client.get("/health")
    assert r.status_code == 503
    body = r.json()["detail"]
    assert body["status"] == "degraded"
    assert "calculator_self_test" in body["message"]

def test_apply_operation():
    assert apply_operation("+", 2, 3) == 5
    assert apply_operation("*", 4, 5) == 20


def test_self_test_passes_on_default_registry():
    assert self_test() == "ok"
