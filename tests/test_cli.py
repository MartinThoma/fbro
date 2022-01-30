"""Tests for `fbro` package."""

# Third party modules
from click.testing import CliRunner

# First party modules
import fbro.cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(fbro.cli.entry_point, ["--version"])
    assert result.exit_code == 0
