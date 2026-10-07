from market_pulse.report import skill_frequency, to_markdown


def test_skill_frequency_counts_each_skill():
    records = [
        {"skills": ["Python", "SQL"]},
        {"skills": ["python", "Git"]},
    ]
    counter = skill_frequency(records)
    assert counter["python"] == 2
    assert counter["sql"] == 1
    assert counter["git"] == 1


def test_report_derives_share_from_total():
    records = [{"skills": ["Python"]}, {"skills": ["Git"]}]
    counter = skill_frequency(records)
    md = to_markdown(counter, total=2)
    assert "| python | 1 | 50% |" in md


def test_share_is_derived_for_larger_corpora():
    records = [
        {"skills": ["Python"]},
        {"skills": ["Go"]},
        {"skills": ["Rust"]},
        {"skills": ["Java"]},
    ]
    counter = skill_frequency(records)
    md = to_markdown(counter, total=len(records))
    assert "| python | 1 | 25% |" in md
    assert "| go | 1 | 25% |" in md


def test_frequency_is_case_whitespace_and_duplicate_safe():
    records = [
        {"skills": [" Python ", "python", "PYTHON"]},
        {"skills": ["  SQL  "]},
        {"skills": []},
        {"skills": None},
    ]
    counter = skill_frequency(records)
    assert counter["python"] == 1
    assert counter["sql"] == 1
    # Two skills across four records: shares stay inside 100%.
    md = to_markdown(counter, total=4)
    assert "| python | 1 | 25% |" in md
    assert "| sql | 1 | 25% |" in md


def test_empty_corpus_renders_header_only():
    md = to_markdown(skill_frequency([]), total=0)
    assert md.splitlines() == ["| Skill | Count | Share |", "|---|---|---|"]
