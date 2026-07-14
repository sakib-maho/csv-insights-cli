"""CLI for CSV Insights."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from csv_insights.analyzer import (
    correlation_matrix,
    detect_outliers_iqr,
    full_report,
    load_rows,
    profile_columns,
    summarize_numeric,
    value_counts,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-insights",
        description="Inspect CSV files quickly from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    profile_parser = subparsers.add_parser("profile", help="Show filled, missing, unique, and numeric flags.")
    profile_parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")

    numeric_parser = subparsers.add_parser("numeric", help="Show numeric summary for one column.")
    numeric_parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")
    numeric_parser.add_argument("--column", required=True, help="Numeric column name.")

    values_parser = subparsers.add_parser("values", help="Show top value counts for one column.")
    values_parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")
    values_parser.add_argument("--column", required=True, help="Column name.")
    values_parser.add_argument("--top", type=int, default=10, help="Top N values to return.")

    outliers_parser = subparsers.add_parser("outliers", help="Detect numeric outliers with IQR.")
    outliers_parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")
    outliers_parser.add_argument("--column", required=True, help="Numeric column name.")

    corr_parser = subparsers.add_parser("corr", help="Show Pearson correlation matrix for numeric columns.")
    corr_parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")

    report_parser = subparsers.add_parser("report", help="Show a combined report for the CSV file.")
    report_parser.add_argument("csv_file", type=Path, help="Path to input CSV file.")

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
    if args.command == "numeric":
        print(json.dumps(summarize_numeric(rows, args.column), indent=2))
        return 0
    if args.command == "values":
        print(json.dumps(value_counts(rows, args.column, top_n=args.top), indent=2))
        return 0
    if args.command == "outliers":
        print(json.dumps(detect_outliers_iqr(rows, args.column), indent=2))
        return 0
    if args.command == "corr":
        print(json.dumps(correlation_matrix(rows), indent=2))
        return 0
    if args.command == "report":
        print(json.dumps(full_report(args.csv_file), indent=2))
        return 0

    parser.error("invalid command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
