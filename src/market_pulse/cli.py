"""Command line entry point for the market-pulse pipeline."""
import argparse
import json
import sys
from pathlib import Path

from .report import skill_frequency, to_markdown

PENDING = ("extract", "transform", "load")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="market-pulse")
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="render the skill frequency table")
    report.add_argument("--input", required=True, help="JSON file with normalised records")
    report.add_argument("--output", help="write the markdown table to this file")

    for name in PENDING:
        sub.add_parser(name, help=f"{name} stage (not implemented yet)")

    return parser


def _load_records(path: Path) -> list[dict] | None:
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return None
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"not valid UTF-8: {path}", file=sys.stderr)
        return None
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr)
        return None
    try:
        records = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"invalid JSON in {path}: {exc}", file=sys.stderr)
        return None
    if not isinstance(records, list):
        print(f"expected a JSON array of objects in {path}", file=sys.stderr)
        return None
    if not all(isinstance(item, dict) for item in records):
        print(f"every element in {path} must be a JSON object", file=sys.stderr)
        return None
    return records


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command in PENDING:
        print(f"the {args.command} stage is not implemented yet", file=sys.stderr)
        return 2

    records = _load_records(Path(args.input))
    if records is None:
        return 1

    table = to_markdown(skill_frequency(records), total=len(records))

    if args.output:
        try:
            Path(args.output).write_text(table + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"cannot write {args.output}: {exc}", file=sys.stderr)
            return 1
    else:
        print(table)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
