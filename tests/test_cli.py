from subprocess import run


def run_cli(*args: str) -> str:
    result = run(["python3", "cli.py", *args], capture_output=True, text=True, check=True)
    return result.stdout


def test_profile_command() -> None:
    output = run_cli("profile", "tests/fixtures/sales.csv")
    assert "\"orders\"" in output
    assert "\"numeric\": true" in output


def test_numeric_command() -> None:
    output = run_cli("numeric", "tests/fixtures/sales.csv", "--column", "revenue")
    assert "\"avg\"" in output
    assert "\"max\": 6200.0" in output


def test_values_command() -> None:
    output = run_cli("values", "tests/fixtures/sales.csv", "--column", "channel", "--top", "2")
    assert "\"Paid\"" in output
    assert "\"count\": 3" in output


def test_outliers_command() -> None:
    output = run_cli("outliers", "tests/fixtures/sales.csv", "--column", "revenue")
    assert "\"row\": 7" in output


def test_corr_command() -> None:
    output = run_cli("corr", "tests/fixtures/sales.csv")
    assert "\"revenue\"" in output
    assert "\"ad_spend\"" in output


def test_report_command() -> None:
    output = run_cli("report", "tests/fixtures/sales.csv")
    assert "\"row_count\": 6" in output
    assert "\"value_counts\"" in output
