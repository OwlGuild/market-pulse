import json

from market_pulse.extract import RAW_DIR, save_raw
from market_pulse.transform import normalise, validate


def test_save_raw_writes_untouched_payload(tmp_path, monkeypatch):
    monkeypatch.setattr("market_pulse.extract.RAW_DIR", tmp_path)
    payload = {"title": "Backend Developer", "skills": ["Python"]}
    path = save_raw(3, payload)
    assert path == tmp_path / "page_003.json"
    assert json.loads(path.read_text(encoding="utf-8")) == payload


def test_validate_reports_missing_title():
    records = [{"title": "QA Engineer"}, {"skills": ["Python"]}]
    errors = validate(records)
    assert errors == ["record 1: missing title"]


def test_validate_accepts_complete_records():
    assert validate([{"title": "Data Engineer"}]) == []


def test_unimplemented_stage_raises_clearly():
    try:
        normalise({"title": "x"})
    except NotImplementedError as exc:
        assert "not implemented yet" in str(exc)
    else:
        raise AssertionError("normalise() must stay unimplemented until the roadmap item lands")


def test_raw_dir_lives_outside_the_package():
    assert RAW_DIR.name == "raw"
    assert "output" in RAW_DIR.parts
    assert "market_pulse" not in RAW_DIR.parts
