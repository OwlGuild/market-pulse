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
frequency and renders a markdown table. Counts are derived at runtime, never hardcoded, and a
skill is counted once per record so duplicated bullets cannot inflate a share.

```bash
PYTHONPATH=src python -m market_pulse.cli report --input examples/records.json
# | Skill | Count | Share |
# |---|---|---|
# | python | 2 | 67% |
# | postgresql | 1 | 33% |
# | django | 1 | 33% |
# | typescript | 1 | 33% |
# | react | 1 | 33% |
# | sql | 1 | 33% |
```

Rows with equal counts appear in input order, so the same corpus always renders the same
table regardless of interpreter hash randomisation.

Stages that are not implemented exit with a clear message instead of pretending to succeed,
and malformed input (invalid JSON, a directory, a non-array payload) fails with a one-line
error rather than a traceback.

## Quickstart

```bash
git clone https://github.com/OwlGuild/market-pulse.git
cd market-pulse
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

Running the CLI needs `PYTHONPATH=src` (or `pytest.ini` does it for the tests):

```bash
PYTHONPATH=src python -m market_pulse.cli report --input examples/records.json
# Windows PowerShell: $env:PYTHONPATH="src"; python -m market_pulse.cli report --input examples/records.json
```

## Testing

```bash
pytest -q
# 30 passed
```

The suite covers frequency counting, share derivation against real totals, duplicate and
whitespace safety, markdown rendering, every CLI error path (missing file, directory input,
non-UTF-8 input, UTF-8 BOM input, unreadable file, invalid JSON, non-array payload, invalid
skills shape, unwritable output), the raw-file overwrite guard, deterministic tie ordering,
and every stub stage. CI runs it on every push, plus a Docker image build.

## Docker

The image ships the pipeline only (tests and examples are excluded by `.dockerignore`) and
defaults to the CLI help:

```bash
docker build -t market-pulse .
docker run --rm market-pulse
# Windows PowerShell: docker run --rm market-pulse
```

To run the report against a local data file, mount it over `/data`:

```bash
docker run --rm -v "$PWD/examples:/data" market-pulse report --input /data/records.json
# Windows PowerShell: docker run --rm -v "${PWD}\examples:/data" market-pulse report --input /data/records.json
```

## Roadmap

- `extract` with rate limiting and raw-response archiving
- `transform` normalisation and validation rules
- `load` into PostgreSQL with history retention
- Skill demand by seniority and contract type
- Stacks that appear together, week over week

## Design notes

- **Counts are derived, never hardcoded.** Every figure in the report is computed at runtime
  and guarded by tests with different corpus sizes.
- **Idempotent stages (planned).** Re-running `transform` on the same raw input will yield the
  same rows — a Roadmap item, not yet implemented.
- **Parsing is validated (planned).** Conflicting required/nice-to-have entries will be
  reported, not silently dropped.

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
