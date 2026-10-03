from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.operations import AVAILABLE_OPERATIONS


@pytest.mark.parametrize(
    "a, b, op, expected",
    [
        (10, 5, "+", 15),
        (10, 5, "-", 5),
        (10, 5, "*", 50),
        (10, 5, "/", 2),
    ],
    ids=["add", "sub", "mul", "div"],
)
def test_basic_operations(client: TestClient, a, b, op, expected):
    r = client.post("/calculate", json={"a": a, "b": b, "operation": op})
    assert r.status_code == 200, r.text
    assert r.json()["result"] == pytest.approx(expected)


def test_division_true_not_floor(client: TestClient):
    r = client.post("/calculate", json={"a": 10, "b": 3, "operation": "/"})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(10 / 3)
    assert r.json()["result"] != 3


def test_negative_operands(client: TestClient):
    cases = [
        (-2, 3, "*", -6),
        (-2, -3, "*", 6),
        (-5, 3, "+", -2),
        (5, -3, "+", 2),
    ]
    for a, b, op, expected in cases:
        r = client.post("/calculate", json={"a": a, "b": b, "operation": op})
        assert r.status_code == 200
        assert r.json()["result"] == pytest.approx(expected), (a, b, op)


def test_float_precision_truncate(client: TestClient):
    r = client.post("/calculate", json={"a": 0.1, "b": 0.2, "operation": "+"})
    assert r.status_code == 200
    assert r.json()["result"] == pytest.approx(0.3)


def test_overflow_crash(client: TestClient):
    r = client.post("/calculate", json={"a": 1e308, "b": 1e308, "operation": "*"})
    assert r.status_code == 200
    assert r.json()["result"] is None


def test_zero_plus_zero(client: TestClient):
    r = client.post("/calculate", json={"a": 0, "b": 0, "operation": "+"})
    assert r.status_code == 200
    assert r.json()["result"] == 0


@pytest.mark.parametrize("a", [0, 1, -1, 1e10])
def test_division_by_zero_rejected(client: TestClient, a):
    r = client.post("/calculate", json={"a": a, "b": 0, "operation": "/"})
    assert r.status_code == 400
    assert "нол" in r.json()["detail"].lower()


def test_zero_divided_by_zero(client: TestClient):
    r = client.post("/calculate", json={"a": 0, "b": 0, "operation": "/"})
    assert r.status_code == 400


@pytest.mark.parametrize("bad_op", ["%", "**", "//", "plus", "", " ", None, 1])
def test_unknown_operation(client: TestClient, bad_op):
    r = client.post("/calculate", json={"a": 1, "b": 2, "operation": bad_op})
    assert r.status_code == 422, r.text


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"a": 1},
        {"a": "abc", "b": 2, "operation": "+"},
        {"a": 1, "b": None, "operation": "+"},
        {"a": 1, "b": 2},
    ],
)
def test_payload_rejected(client: TestClient, payload):
    r = client.post("/calculate", json=payload)
    assert r.status_code == 422


def test_string_numbers_converted_to_float(client: TestClient):
    r = client.post("/calculate", json={"a": "10", "b": "5", "operation": "+"})
    assert r.status_code == 200
    assert r.json()["result"] == 15


def test_response_contains_all_operations(client: TestClient):
    r = client.post("/calculate", json={"a": 1, "b": 2, "operation": "+"})
    assert r.status_code == 200
    body = r.json()
    assert body["available_operations"] == AVAILABLE_OPERATIONS
    assert body["a"] == 1
    assert body["b"] == 2
    assert body["operation"] == "+"
