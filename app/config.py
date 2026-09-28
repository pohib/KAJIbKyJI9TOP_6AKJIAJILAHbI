from __future__ import annotations
import os
from importlib.metadata import PackageNotFoundError, version as pkg_version

APP_NAME = "CalcAPI"
APP_DESCRIPTION = "КАЛЬКУЛЯТОР БАКЛАЖАНЫ"

_FALLBACK_VERSION = "0.0.0"

def _resolve_version() -> str:
    env_version = os.getenv("APP_VERSION")
    if env_version:
        return env_version
    try:
        return pkg_version("calcapi")
    except PackageNotFoundError:
        return _FALLBACK_VERSION

APP_VERSION: str = _resolve_version()