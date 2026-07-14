"""CSV Insights package."""

from .analyzer import (
    correlation_matrix,
    detect_outliers_iqr,
    full_report,
    load_rows,
    profile_columns,
    summarize_numeric,
    value_counts,
)

__all__ = [
    "correlation_matrix",
    "detect_outliers_iqr",
    "full_report",
    "load_rows",
    "profile_columns",
    "summarize_numeric",
    "value_counts",
]
