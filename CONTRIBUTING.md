# Contributing

Part of [OwlGuild](https://github.com/OwlGuild).

## Ground rules

- Small pull requests; one concern per commit.
- English commit messages in the imperative mood ("Add report test for n != 2").
- Behaviour changes ship with a test that fails before the fix.
- Derived values stay derived: counts and shares are computed, never hardcoded.

## Local checks

```bash
pip install -r requirements.txt
pytest -q
PYTHONPATH=src python -m market_pulse.cli --help
```

## Review

Both maintainers review before merge. Keep discussion in the PR, keep scope in the diff.
