from __future__ import annotations

from fastapi.testclient import TestClient


def test_errors_tracebacks(client: TestClient):
    r = client.post("/calculate", json={"a": 1, "b": 0, "operation": "/"})
    assert r.status_code == 400
    detail = r.json()["detail"]
    assert "Traceback" not in detail
    assert "File " not in detail
    assert "line " not in detail


def test_openapi_internal_paths(client: TestClient):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    text = r.text
    assert "/home/" not in text
    assert "C:\\" not in text
