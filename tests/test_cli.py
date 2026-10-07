import json

from market_pulse.cli import run


def _write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def test_report_writes_markdown(tmp_path):
    records = [{"skills": ["Python", "SQL"]}, {"skills": ["python"]}]
    src = tmp_path / "records.json"
    src.write_text(json.dumps(records), encoding="utf-8")
    out = tmp_path / "report.md"

    assert run(["report", "--input", str(src), "--output", str(out)]) == 0

    text = out.read_text(encoding="utf-8")
    assert "| python | 2 | 100% |" in text
    assert "| sql | 1 | 50% |" in text


def test_report_prints_to_stdout_without_output_flag(tmp_path, capsys):
    src = _write(tmp_path / "records.json", json.dumps([{"skills": ["Python"]}]))
    assert run(["report", "--input", str(src)]) == 0
    assert "| python | 1 | 100% |" in capsys.readouterr().out


def test_report_fails_on_missing_input(tmp_path):
    assert run(["report", "--input", str(tmp_path / "nope.json")]) == 1


def test_report_fails_on_invalid_json(tmp_path, capsys):
    src = _write(tmp_path / "broken.json", "not json at all")
    assert run(["report", "--input", str(src)]) == 1
    assert "invalid JSON" in capsys.readouterr().err


def test_report_fails_on_empty_file(tmp_path, capsys):
    src = _write(tmp_path / "empty.json", "")
    assert run(["report", "--input", str(src)]) == 1
    assert "invalid JSON" in capsys.readouterr().err


def test_report_fails_when_input_is_not_an_array(tmp_path, capsys):
    src = _write(tmp_path / "object.json", json.dumps({"skills": ["Python"]}))
    assert run(["report", "--input", str(src)]) == 1
    assert "JSON array" in capsys.readouterr().err


def test_report_fails_when_elements_are_not_objects(tmp_path, capsys):
    src = _write(tmp_path / "strings.json", json.dumps(["Python", "SQL"]))
    assert run(["report", "--input", str(src)]) == 1
    assert "JSON object" in capsys.readouterr().err


def test_report_fails_when_input_is_a_directory(tmp_path, capsys):
    assert run(["report", "--input", str(tmp_path)]) == 1
    assert "no such file" in capsys.readouterr().err


def test_report_fails_when_output_directory_is_missing(tmp_path, capsys):
    src = _write(tmp_path / "records.json", json.dumps([{"skills": ["Python"]}]))
    out = tmp_path / "missing-dir" / "report.md"
    assert run(["report", "--input", str(src), "--output", str(out)]) == 1
    assert "cannot write" in capsys.readouterr().err


def test_pending_stage_exits_with_two(capsys):
    assert run(["extract"]) == 2
    assert "not implemented" in capsys.readouterr().err
