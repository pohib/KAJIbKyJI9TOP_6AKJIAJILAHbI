from __future__ import annotations

import importlib

import app.config


def test_version_from_env(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "9.9.9-test")
    importlib.reload(app.config)
    assert app.config.APP_VERSION == "9.9.9-test"
    monkeypatch.delenv("APP_VERSION", raising=False)
    importlib.reload(app.config)
