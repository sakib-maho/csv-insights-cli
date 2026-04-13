# CSV Insights CLI

`xyzzz` is upgraded into a practical CSV analysis tool for quick dataset checks from the terminal.
It provides fast column profiling and numeric summaries for small to medium CSV files.

## Features

- Column profile report with `filled`, `missing`, and `unique` counts
- Numeric summary (`count`, `min`, `max`, `avg`) for any selected column
- Simple command interface for local data debugging
- Test suite with fixture data

## Tech Stack

- Python 3.10+
- Standard library only (`csv`, `argparse`, `json`)
- `pytest` for tests

## Quick Start

```bash
git clone https://github.com/sakib-maho/xyzzz.git
cd xyzzz
python3 -m pip install pytest
```

## Usage

```bash
python3 cli.py tests/fixtures/sales.csv profile
python3 cli.py tests/fixtures/sales.csv summary --column revenue
```

## Run Tests

```bash
python3 -m pytest -q
```

## Project Structure

```text
xyzzz/
├── cli.py
├── csv_insights/
│   └── analyzer.py
└── tests/
    ├── fixtures/sales.csv
    ├── test_analyzer.py
    └── test_cli.py
```

## License

MIT License. See `LICENSE`.