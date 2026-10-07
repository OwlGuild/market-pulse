"""Load stage: upsert normalised rows into PostgreSQL."""
from typing import Any


def upsert(rows: list[dict[str, Any]]) -> int:
    raise NotImplementedError("upsert() is implemented in week 1")
