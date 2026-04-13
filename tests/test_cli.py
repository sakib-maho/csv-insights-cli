from subprocess import run


def run_cli(*args: str) -> str:
    result = run(["python3", "cli.py", *args], capture_output=True, text=True, check=True)
    return result.stdout


def test_profile_command() -> None:
    output = run_cli("tests/fixtures/sales.csv", "profile")
    assert "\"orders\"" in output
    assert "\"missing\": 1" in output


def test_summary_command() -> None:
    output = run_cli("tests/fixtures/sales.csv", "summary", "--column", "revenue")
    assert "\"avg\"" in output
    assert "\"max\": 1500.0" in output
