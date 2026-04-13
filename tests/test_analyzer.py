from pathlib import Path

from csv_insights.analyzer import load_rows, profile_columns, summarize_numeric


FIXTURE = Path("tests/fixtures/sales.csv")


def test_profile_columns() -> None:
    rows = load_rows(FIXTURE)
    profile = profile_columns(rows)
    assert profile["orders"]["filled"] == 3
    assert profile["orders"]["missing"] == 1
    assert profile["region"]["unique"] == 3


def test_summarize_numeric() -> None:
    rows = load_rows(FIXTURE)
    summary = summarize_numeric(rows, "revenue")
    assert summary["count"] == 4.0
    assert summary["min"] == 980.0
    assert summary["max"] == 1500.0
