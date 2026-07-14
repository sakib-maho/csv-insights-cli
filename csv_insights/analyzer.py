"""Core analytics helpers for CSV files."""

from __future__ import annotations

import csv
import math
from pathlib import Path


def load_rows(path: Path | str) -> list[dict[str, str]]:
    """Load all rows from a CSV file."""
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def _numeric_series(rows: list[dict[str, str]], column: str) -> list[tuple[int, float]]:
    values: list[tuple[int, float]] = []
    for index, row in enumerate(rows, start=2):
        raw = (row.get(column) or "").strip()
        if not raw:
            continue
        try:
            values.append((index, float(raw)))
        except ValueError:
            continue
    return values


def _numeric_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    columns = list(rows[0].keys())
    return [column for column in columns if _numeric_series(rows, column)]


def _percentile(sorted_values: list[float], percentile: float) -> float:
    if not sorted_values:
        raise ValueError("cannot compute percentile for empty data")
    position = (len(sorted_values) - 1) * percentile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def profile_columns(rows: list[dict[str, str]]) -> dict[str, dict[str, int | bool]]:
    """Return per-column shape information."""
    if not rows:
        return {}

    columns = list(rows[0].keys())
    profile: dict[str, dict[str, int | bool]] = {}
    for column in columns:
        values = [(row.get(column) or "").strip() for row in rows]
        filled_values = [value for value in values if value]
        profile[column] = {
            "filled": len(filled_values),
            "missing": len(values) - len(filled_values),
            "unique": len(set(filled_values)),
            "numeric": bool(_numeric_series(rows, column)),
        }
    return profile


def summarize_numeric(rows: list[dict[str, str]], column: str) -> dict[str, float]:
    """Compute descriptive statistics for a numeric column."""
    numeric_values = [value for _, value in _numeric_series(rows, column)]
    if not numeric_values:
        raise ValueError(f"column '{column}' has no numeric values")

    sorted_values = sorted(numeric_values)
    count = len(sorted_values)
    mean = sum(sorted_values) / count
    variance = sum((value - mean) ** 2 for value in sorted_values) / count
    return {
        "count": float(count),
        "min": min(sorted_values),
        "max": max(sorted_values),
        "avg": mean,
        "median": _percentile(sorted_values, 0.5),
        "std_dev": variance ** 0.5,
    }


def value_counts(rows: list[dict[str, str]], column: str, top_n: int = 10) -> list[dict[str, int | str]]:
    """Return the most common non-empty values for a column."""
    if top_n <= 0:
        raise ValueError("top_n must be greater than zero")

    counts: dict[str, int] = {}
    for row in rows:
        value = (row.get(column) or "").strip()
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1

    if not counts and rows and column not in rows[0]:
        raise ValueError(f"unknown column '{column}'")

    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{"value": value, "count": count} for value, count in ordered[:top_n]]


def detect_outliers_iqr(rows: list[dict[str, str]], column: str) -> dict[str, float | list[dict[str, float | int]]]:
    """Detect outliers using the interquartile range rule."""
    numeric_rows = _numeric_series(rows, column)
    values = sorted(value for _, value in numeric_rows)
    if len(values) < 4:
        return {
            "column": column,
            "q1": 0.0,
            "q3": 0.0,
            "iqr": 0.0,
            "lower_bound": 0.0,
            "upper_bound": 0.0,
            "outliers": [],
        }

    q1 = _percentile(values, 0.25)
    q3 = _percentile(values, 0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [
        {"row": row_number, "value": value}
        for row_number, value in numeric_rows
        if value < lower_bound or value > upper_bound
    ]
    return {
        "column": column,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outliers": outliers,
    }


def correlation_matrix(rows: list[dict[str, str]]) -> dict[str, dict[str, float | None]]:
    """Compute Pearson correlation across numeric columns."""
    numeric_columns = _numeric_columns(rows)
    correlations: dict[str, dict[str, float | None]] = {}

    for left in numeric_columns:
        correlations[left] = {}
        for right in numeric_columns:
            if left == right:
                correlations[left][right] = 1.0
                continue

            paired: list[tuple[float, float]] = []
            for row in rows:
                left_raw = (row.get(left) or "").strip()
                right_raw = (row.get(right) or "").strip()
                if not left_raw or not right_raw:
                    continue
                try:
                    paired.append((float(left_raw), float(right_raw)))
                except ValueError:
                    continue

            if len(paired) < 2:
                correlations[left][right] = None
                continue

            xs = [pair[0] for pair in paired]
            ys = [pair[1] for pair in paired]
            mean_x = sum(xs) / len(xs)
            mean_y = sum(ys) / len(ys)
            numerator = sum((x - mean_x) * (y - mean_y) for x, y in paired)
            denominator_x = sum((x - mean_x) ** 2 for x in xs)
            denominator_y = sum((y - mean_y) ** 2 for y in ys)
            denominator = (denominator_x * denominator_y) ** 0.5
            correlations[left][right] = None if denominator == 0 else numerator / denominator

    return correlations


def full_report(path: Path | str) -> dict[str, object]:
    """Load a CSV and return a combined analysis report."""
    rows = load_rows(path)
    numeric_columns = _numeric_columns(rows)
    return {
        "path": str(path),
        "row_count": len(rows),
        "profile": profile_columns(rows),
        "numeric_summary": {
            column: summarize_numeric(rows, column) for column in numeric_columns
        },
        "value_counts": {
            column: value_counts(rows, column, top_n=5) for column in (rows[0].keys() if rows else [])
        },
        "outliers": {
            column: detect_outliers_iqr(rows, column) for column in numeric_columns
        },
        "correlations": correlation_matrix(rows),
    }
