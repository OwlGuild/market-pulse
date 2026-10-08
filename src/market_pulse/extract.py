"""Extract stage: fetch raw postings and store the untouched response."""
import json
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "output" / "raw"


def extract(page: int) -> dict:
    raise NotImplementedError("extract() is not implemented yet (see Roadmap)")


def save_raw(page: int, payload: dict) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"page_{page:03d}.json"
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path
