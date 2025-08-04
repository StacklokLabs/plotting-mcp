"""Tests for plotting functionality."""

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.figure import Figure

from plotting_mcp.plot import (
    _auto_rotate_labels,
    _create_pie_plot,
    _create_plot,
    plot_to_bytes,
)


class TestAutoRotateLabels:
    """Test the _auto_rotate_labels function."""

    def test_auto_rotate_labels_x_axis(self):
        """Test auto rotation for x-axis labels."""
        fig, ax = plt.subplots()
        # Create long labels that should trigger rotation
        long_labels = [f"Very Long Label {i}" for i in range(10)]
        ax.set_xticks(range(len(long_labels)))
        ax.set_xticklabels(long_labels)

        _auto_rotate_labels(ax, axis="x")

        # Check that rotation was applied
        for label in ax.get_xticklabels():
            assert label.get_rotation() == 90

        plt.close(fig)

    def test_auto_rotate_labels_y_axis(self):
        """Test auto rotation for y-axis labels."""
        fig, ax = plt.subplots()
        # Create long labels that should trigger rotation
        long_labels = [f"Very Long Label {i}" for i in range(10)]
        ax.set_yticks(range(len(long_labels)))
        ax.set_yticklabels(long_labels)

        _auto_rotate_labels(ax, axis="y")

        # Check that rotation was applied
        for label in ax.get_yticklabels():
            assert label.get_rotation() == 90

        plt.close(fig)

    def test_auto_rotate_labels_short_labels(self):
        """Test that short labels don't get rotated."""
        fig, ax = plt.subplots()
        # Create short labels that shouldn't trigger rotation
        short_labels = ["A", "B", "C", "D"]
        ax.set_xticks(range(len(short_labels)))
        ax.set_xticklabels(short_labels)

        _auto_rotate_labels(ax, axis="x")

        # Check that rotation was not applied (default rotation is 0)
        for label in ax.get_xticklabels():
            assert label.get_rotation() == 0

        plt.close(fig)

    def test_auto_rotate_labels_invalid_axis(self):
        """Test that invalid axis raises ValueError."""
        fig, ax = plt.subplots()

        with pytest.raises(ValueError, match="Axis must be 'x' or 'y'"):
            _auto_rotate_labels(ax, axis="z")

        plt.close(fig)

    def test_auto_rotate_labels_empty_labels(self):
        """Test that empty labels don't cause errors."""
        fig, ax = plt.subplots()
        # No labels set

        # Should not raise any errors
        _auto_rotate_labels(ax, axis="x")
        _auto_rotate_labels(ax, axis="y")

        plt.close(fig)


class TestCreatePiePlot:
    """Test the _create_pie_plot function."""

    def test_create_pie_plot_single_column_value_counts(self):
        """Test pie plot with single column using value counts."""
        df = pd.DataFrame({"category": ["A", "B", "A", "C", "B", "A"]})
        fig, ax = plt.subplots()

        _create_pie_plot(ax, df)

        # Check that pie chart was created (wedges should exist)
        assert len(ax.patches) > 0
        plt.close(fig)

    def test_create_pie_plot_two_columns(self):
        """Test pie plot with two columns (labels and values)."""
        df = pd.DataFrame({"category": ["A", "B", "C"], "values": [30, 45, 25]})
        fig, ax = plt.subplots()

        _create_pie_plot(ax, df)

        # Check that pie chart was created with 3 wedges
        assert len(ax.patches) == 3
        plt.close(fig)

    def test_create_pie_plot_too_many_columns(self):
        """Test that pie plot with too many columns raises ValueError."""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6], "col3": [7, 8, 9]})
        fig, ax = plt.subplots()

        with pytest.raises(ValueError, match="Pie chart requires either one column"):
            _create_pie_plot(ax, df)

        plt.close(fig)

    def test_create_pie_plot_two_columns_with_labels_param(self):
        """Test that pie plot with two columns rejects labels parameter."""
        df = pd.DataFrame({"category": ["A", "B", "C"], "values": [30, 45, 25]})
        fig, ax = plt.subplots()

        with pytest.raises(ValueError, match="does not accept 'labels' parameter"):
            _create_pie_plot(ax, df, labels=["X", "Y", "Z"])

        plt.close(fig)


class TestCreateMatplotlibPlot:
    """Test the _create_matplotlib_plot function."""

    def test_create_line_plot(self):
        """Test creation of line plot."""
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})

        fig, ax = _create_plot(df, "line", x="x", y="y")

        assert isinstance(fig, Figure)
        assert len(ax.lines) > 0  # Line plot should have lines
        plt.close(fig)

    def test_create_bar_plot(self):
        """Test creation of bar plot."""
        df = pd.DataFrame({"category": ["A", "B", "C", "D"], "values": [10, 15, 8, 12]})

        fig, ax = _create_plot(df, "bar", x="category", y="values")

        assert isinstance(fig, Figure)
        assert len(ax.patches) > 0  # Bar plot should have bars (patches)
        plt.close(fig)

    def test_create_pie_plot(self):
        """Test creation of pie plot through matplotlib function."""
        df = pd.DataFrame({"category": ["A", "B", "C"], "values": [30, 45, 25]})

        fig, ax = _create_plot(df, "pie")

        assert isinstance(fig, Figure)
        assert len(ax.patches) > 0  # Pie plot should have wedges (patches)
        plt.close(fig)

    def test_empty_dataframe_raises_error(self):
        """Test that empty DataFrame raises ValueError."""
        df = pd.DataFrame()

        with pytest.raises(ValueError, match="CSV data is empty"):
            _create_plot(df, "line")

    def test_unsupported_plot_type_raises_error(self):
        """Test that unsupported plot type raises ValueError."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        with pytest.raises(ValueError, match="Unsupported plot type"):
            _create_plot(df, "scatter3d")

    def test_plot_with_title_and_labels(self):
        """Test plot creation with title and axis labels."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        fig, ax = _create_plot(
            df, "line", x="x", y="y", title="Test Plot", xlabel="X Axis", ylabel="Y Axis"
        )

        assert ax.get_title() == "Test Plot"
        assert ax.get_xlabel() == "X Axis"
        assert ax.get_ylabel() == "Y Axis"
        plt.close(fig)


class TestPlotToBytes:
    """Test the plot_to_bytes function."""

    def test_plot_to_bytes_returns_bytes(self):
        """Test that plot_to_bytes returns bytes."""
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})

        result = plot_to_bytes(df, "line", x="x", y="y")

        assert isinstance(result, bytes)
        assert len(result) > 0
        # Check PNG header
        assert result.startswith(b"\x89PNG")

    def test_plot_to_bytes_different_plot_types(self):
        """Test plot_to_bytes with different plot types."""
        df_line = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        df_bar = pd.DataFrame({"cat": ["A", "B", "C"], "val": [1, 2, 3]})
        df_pie = pd.DataFrame({"category": ["A", "B", "C"], "values": [30, 45, 25]})

        line_bytes = plot_to_bytes(df_line, "line", x="x", y="y")
        bar_bytes = plot_to_bytes(df_bar, "bar", x="cat", y="val")
        pie_bytes = plot_to_bytes(df_pie, "pie")

        assert all(isinstance(b, bytes) for b in [line_bytes, bar_bytes, pie_bytes])
        assert all(len(b) > 0 for b in [line_bytes, bar_bytes, pie_bytes])
        assert all(b.startswith(b"\x89PNG") for b in [line_bytes, bar_bytes, pie_bytes])
