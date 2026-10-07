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
