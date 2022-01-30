"""Tests for `fbro` package."""

# First party modules
import fbro


def test_version():
    assert fbro.__version__.count(".") == 2
