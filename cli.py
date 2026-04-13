"""CLI for CSV Insights."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from csv_insights.analyzer import load_rows, profile_columns, summarize_numeric


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-insights",
        description="Inspect CSV files quickly from the command line.",
    )
    parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("profile", help="Show filled/missing/unique per column.")

    summary_parser = subparsers.add_parser(
        "summary", help="Show numeric summary for one column."
    )
    summary_parser.add_argument("--column", required=True, help="Numeric column name.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.csv_file.exists() or not args.csv_file.is_file():
        parser.error(f"csv file not found: {args.csv_file}")

    rows = load_rows(args.csv_file)
    if args.command == "profile":
        print(json.dumps(profile_columns(rows), indent=2))
        return 0

    if args.command == "summary":
        print(json.dumps(summarize_numeric(rows, args.column), indent=2))
        return 0

    parser.error("invalid command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
