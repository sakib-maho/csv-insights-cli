"""Core analytics helpers for CSV files."""

from __future__ import annotations

import csv
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    """Load all rows from CSV file."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def profile_columns(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    """Return basic per-column profile (filled/missing/unique)."""
    if not rows:
        return {}

    columns = list(rows[0].keys())
    profile: dict[str, dict[str, int]] = {}
    for column in columns:
        values = [row.get(column, "") for row in rows]
        filled = sum(1 for value in values if value.strip() != "")
        unique = len({value for value in values if value.strip() != ""})
        profile[column] = {
            "filled": filled,
            "missing": len(values) - filled,
            "unique": unique,
        }
    return profile


def summarize_numeric(rows: list[dict[str, str]], column: str) -> dict[str, float]:
    """Compute min/max/avg for numeric column."""
    numeric_values: list[float] = []
    for row in rows:
        value = (row.get(column) or "").strip()
        if not value:
            continue
        try:
            numeric_values.append(float(value))
        except ValueError:
            continue

    if not numeric_values:
        raise ValueError(f"column '{column}' has no numeric values")

    total = sum(numeric_values)
    return {
        "count": float(len(numeric_values)),
        "min": min(numeric_values),
        "max": max(numeric_values),
        "avg": total / len(numeric_values),
    }
