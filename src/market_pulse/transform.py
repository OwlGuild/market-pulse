"""Transform stage: normalise raw payloads into a single schema."""
from typing import Any


def normalise(record: dict[str, Any]) -> dict[str, Any]:
    raise NotImplementedError("normalise() is not implemented yet (see Roadmap)")


def validate(records: list[dict[str, Any]]) -> list[str]:
    errors = []
    for i, r in enumerate(records):
        if not r.get("title"):
            errors.append(f"record {i}: missing title")
    return errors
