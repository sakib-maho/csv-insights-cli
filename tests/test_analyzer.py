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


FIXTURE = Path("tests/fixtures/sales.csv")


def test_profile_columns() -> None:
    rows = load_rows(FIXTURE)
    profile = profile_columns(rows)
    assert profile["orders"]["filled"] == 5
    assert profile["orders"]["missing"] == 1
    assert profile["region"]["unique"] == 3
    assert profile["revenue"]["numeric"] is True


def test_summarize_numeric() -> None:
    rows = load_rows(FIXTURE)
    summary = summarize_numeric(rows, "revenue")
    assert summary["count"] == 6.0
    assert summary["min"] == 980.0
    assert summary["max"] == 6200.0
    assert summary["median"] == 1350.0


def test_value_counts() -> None:
    rows = load_rows(FIXTURE)
    counts = value_counts(rows, "channel", top_n=2)
    assert counts[0] == {"value": "Paid", "count": 3}
    assert len(counts) == 2


def test_detect_outliers_iqr() -> None:
    rows = load_rows(FIXTURE)
    report = detect_outliers_iqr(rows, "revenue")
    assert report["outliers"] == [{"row": 7, "value": 6200.0}]


def test_correlation_matrix() -> None:
    rows = load_rows(FIXTURE)
    corr = correlation_matrix(rows)
    assert corr["revenue"]["ad_spend"] is not None
    assert corr["revenue"]["revenue"] == 1.0


def test_full_report() -> None:
    report = full_report(FIXTURE)
    assert report["row_count"] == 6
    assert "profile" in report
    assert "correlations" in report
