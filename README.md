# CSV Insights CLI

<!-- BrandCloud:readme-standard -->
[![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Showcase](https://img.shields.io/badge/Portfolio-Showcase-blue.svg)](#)

_Part of the `sakib-maho` project showcase series with consistent documentation and quality standards._

`csv-insights-cli` is a practical CSV analysis tool for quick dataset checks from the terminal.
It provides fast column profiling and numeric summaries for small to medium CSV files.

## Features

- Column profile report with `filled`, `missing`, and `unique` counts
- Numeric summary (`count`, `min`, `max`, `avg`) for any selected column
- Simple command interface for local data debugging
- Test suite with fixture data

## Quick Start

```bash
git clone https://github.com/sakib-maho/csv-insights-cli.git
cd csv-insights-cli
python3 -m pip install pytest
```

## Tests

```bash
python3 -m pytest -q
```

## License

MIT License. See `LICENSE`.

## Tech Stack

- Python 3.10+
- Standard library only (`csv`, `argparse`, `json`)
- `pytest` for tests

## Usage

```bash
python3 cli.py tests/fixtures/sales.csv profile
python3 cli.py tests/fixtures/sales.csv summary --column revenue
```

## Project Structure

```text
csv-insights-cli/
├── cli.py
├── csv_insights/
│   └── analyzer.py
└── tests/
    ├── fixtures/sales.csv
    ├── test_analyzer.py
    └── test_cli.py
```
