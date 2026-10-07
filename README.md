# market-pulse

Data pipeline that collects, cleans and analyses job-market postings so that what we build and
what we apply for is based on evidence rather than guesses.

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-16-336791.svg)](https://www.postgresql.org/)
[![Pipeline](https://img.shields.io/badge/stage-ETL-orange.svg)](#pipeline)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## Why this exists

Hiring advice online is mostly anecdote. This repository turns the question "which skills do
these postings actually ask for?" into a query. Every number in our planning came from this
pipeline, not from intuition.

## Pipeline

```
extract   fetch raw postings, store the untouched response
  ↓
transform normalise titles, locations and requirements into one schema
  ↓
load      upsert into PostgreSQL, keep history so trends are measurable
  ↓
report    aggregate frequencies, generate the market report
```

Raw responses are kept as-is. When a parsing rule is wrong, the fix is reprocessing — the
original is never overwritten.

## What it measures

- Skill frequency across the whole posting set
- Skill demand by seniority and contract type
- Which stacks appear together
- Week-over-week movement in each demand figure

## Quickstart

```bash
git clone https://github.com/OwlGuild/market-pulse.git
cd market-pulse
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m market_pulse extract
python -m market_pulse transform
python -m market_pulse load
python -m market_pulse report
```

## Output

| File | Contents |
|---|---|
| `output/requirements.json` | structured requirement set per posting |
| `output/requirements.csv` | the same, flattened for spreadsheets |
| `output/market_report.md` | frequency tables and trend commentary |

## Design notes

- **Idempotent stages.** Re-running `transform` on the same raw input yields the same rows.
- **Parsing is validated.** Conflicting required/nice-to-have entries are reported, not
  silently dropped.
- **Counts are derived, never hardcoded.** Every figure in the report is computed at runtime.

## Testing

```bash
pytest
```

Fixtures use captured responses from a small corpus, so a change to the parser that alters
existing output fails until reviewed deliberately.

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