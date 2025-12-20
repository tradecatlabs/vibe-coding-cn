"""
Pytest configuration for tests.

Configures anyio to only use asyncio backend (not trio).
Checks that the skill_seekers package is installed before running tests.
"""

import sys
import pytest


def pytest_configure(config):
    """Check if package is installed before running tests."""
    try:
        import skill_seekers
    except ModuleNotFoundError:
        print("\n" + "=" * 70)
        print("ERROR: skill_seekers package not installed")
        print("=" * 70)
        print("\nPlease install the package in editable mode first:")
        print("  pip install -e .")
        print("\nOr activate your virtual environment if you already installed it.")
        print("=" * 70 + "\n")
        sys.exit(1)


@pytest.fixture(scope="session")
def anyio_backend():
    """Override anyio backend to only use asyncio (not trio)."""
    return "asyncio"
