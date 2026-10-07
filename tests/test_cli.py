import json

from market_pulse.cli import run


def test_report_writes_markdown(tmp_path):
    records = [{"skills": ["Python", "SQL"]}, {"skills": ["python"]}]
    src = tmp_path / "records.json"
    src.write_text(json.dumps(records), encoding="utf-8")
    out = tmp_path / "report.md"

    assert run(["report", "--input", str(src), "--output", str(out)]) == 0

    text = out.read_text(encoding="utf-8")
    assert "| python | 2 | 100% |" in text
    assert "| sql | 1 | 50% |" in text


def test_report_fails_on_missing_input(tmp_path):
    assert run(["report", "--input", str(tmp_path / "nope.json")]) == 1


def test_pending_stage_exits_with_two(capsys):
    assert run(["extract"]) == 2
    assert "not implemented" in capsys.readouterr().err
