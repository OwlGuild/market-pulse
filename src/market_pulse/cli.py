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


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command in PENDING:
        print(f"the {args.command} stage is not implemented yet", file=sys.stderr)
        return 2

    path = Path(args.input)
    if not path.exists():
        print(f"no such file: {path}", file=sys.stderr)
        return 1

    records = json.loads(path.read_text(encoding="utf-8"))
    table = to_markdown(skill_frequency(records), total=len(records))

    if args.output:
        Path(args.output).write_text(table + "\n", encoding="utf-8")
    else:
        print(table)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
