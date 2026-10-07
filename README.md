# market-pulse

Data pipeline that collects, cleans and analyses job-market postings so that what we build and
what we apply for is based on evidence rather than guesses.

[![CI](https://github.com/OwlGuild/market-pulse/actions/workflows/ci.yml/badge.svg)](https://github.com/OwlGuild/market-pulse/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Pipeline](https://img.shields.io/badge/stage-ETL-orange.svg)](#roadmap)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## Why this exists

Hiring advice online is mostly anecdote. This repository turns the question "which skills do
these postings actually ask for?" into a query. Every number in our planning came from data,
not from intuition.

## Pipeline

```
extract   fetch raw postings, store the untouched response
  ↓
transform normalise titles, locations and requirements into one schema
  ↓
load      upsert into PostgreSQL, keep history so trends are measurable
  ↓
report    aggregate frequencies, generate the market report   ← implemented
```

Raw responses are kept as-is. When a parsing rule is wrong, the fix is reprocessing — the
original is never overwritten.

## What works today

The **report** stage is implemented and tested: it takes normalised records, counts skill
frequency and renders a markdown table. Counts are derived at runtime, never hardcoded.

```bash
export PYTHONPATH=src
python -m market_pulse.cli report --input output/records.json
# | Skill  | Count | Share |
# |--------|-------|-------|
# | python | 2     | 100%  |
```

Stages that are not implemented exit with a clear message instead of pretending to succeed.

## Quickstart

```bash
git clone https://github.com/OwlGuild/market-pulse.git
cd market-pulse
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt pytest
export PYTHONPATH=src
pytest -q
# 5 passed
```

## Testing

```bash
pytest -q
# 5 passed
```

The suite covers frequency counting, share derivation against the real total, markdown
rendering and CLI behaviour (success, missing input, unimplemented stage). CI runs it on every
push.

## Roadmap

- `extract` with rate limiting and raw-response archiving
- `transform` normalisation and validation rules
- `load` into PostgreSQL with history retention
- Skill demand by seniority and contract type
- Stacks that appear together, week over week

## Design notes

- **Idempotent stages.** Re-running `transform` on the same raw input yields the same rows.
- **Parsing is validated.** Conflicting required/nice-to-have entries are reported, not
  silently dropped.
- **Counts are derived, never hardcoded.** Every figure in the report is computed at runtime.

## Ownership

Both maintainers of [OwlGuild](https://github.com/OwlGuild) commit here.

| Area | Maintainer |
|---|---|
| Extraction and rate limiting | [@MarziehAkrami](https://github.com/MarziehAkrami) |
| Normalisation and validation | [@MarziehAkrami](https://github.com/MarziehAkrami) |
| Schema and PostgreSQL load | [@MarziehAkrami](https://github.com/MarziehAkrami) |
| Reporting and visualisation | [@AhmadGolbooee](https://github.com/AhmadGolbooee) |
| CI, Docker, docs | shared |

## License

[MIT](LICENSE).
