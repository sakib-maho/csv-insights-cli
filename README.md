# CSV Insights CLI

`csv-insights-cli` helps you inspect a CSV quickly before pulling it into a
notebook or analytics pipeline. It focuses on practical questions: which columns
are complete, which values are common, where outliers appear, and how numeric
columns move together.

## Features

- Column profiling with `filled`, `missing`, `unique`, and `numeric` flags
- Numeric summaries with `min`, `max`, `avg`, `median`, and `std_dev`
- Top value counts for categorical or free-text columns
- IQR-based outlier detection for numeric columns
- Pearson correlation matrix across numeric columns
- Full combined report for one-command inspection

## CLI Usage

```bash
python3 cli.py profile tests/fixtures/sales.csv
python3 cli.py numeric tests/fixtures/sales.csv --column revenue
python3 cli.py values tests/fixtures/sales.csv --column region --top 3
python3 cli.py outliers tests/fixtures/sales.csv --column revenue
python3 cli.py corr tests/fixtures/sales.csv
python3 cli.py report tests/fixtures/sales.csv
```

## Python API

```python
from csv_insights.analyzer import full_report, load_rows, summarize_numeric

rows = load_rows("tests/fixtures/sales.csv")
print(summarize_numeric(rows, "revenue"))
print(full_report("tests/fixtures/sales.csv"))
```

## Included Fixture

The sample dataset contains regional sales metrics with multiple numeric columns,
missing data, repeated categories, and a deliberate outlier so the analytics
commands produce meaningful output.

## Run Tests

```bash
python3 -m pytest -q
```

## License

MIT. See `LICENSE`.