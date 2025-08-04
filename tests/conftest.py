"""Pytest configuration and shared fixtures."""

import matplotlib


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Use non-interactive backend for matplotlib to avoid GUI issues in tests
    matplotlib.use("Agg")
