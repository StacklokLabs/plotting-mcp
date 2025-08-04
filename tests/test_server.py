"""Tests for server functionality."""

import base64
import json

import pytest
from mcp.types import ImageContent, TextContent
from pandas.errors import EmptyDataError

from plotting_mcp.server import generate_plot


class TestGeneratePlot:
    """Test the generate_plot MCP tool."""

    def test_generate_plot_basic_line_plot(self):
        """Test basic line plot generation."""
        csv_data = "x,y\n1,2\n2,4\n3,6\n4,8\n5,10"

        result = generate_plot(csv_data, "line", json_kwargs='{"x": "x", "y": "y"}')

        assert isinstance(result, tuple)
        assert len(result) == 2

        text_content, image_content = result
        assert isinstance(text_content, TextContent)
        assert isinstance(image_content, ImageContent)

        assert text_content.type == "text"
        assert text_content.text == "Plot generated successfully"

        assert image_content.type == "image"
        assert image_content.mimeType == "image/png"
        assert len(image_content.data) > 0

        # Verify the image data is valid base64
        decoded_data = base64.b64decode(image_content.data)
        assert decoded_data.startswith(b"\x89PNG")

    def test_generate_plot_bar_chart(self):
        """Test bar chart generation."""
        csv_data = "category,values\nA,10\nB,15\nC,8\nD,12"

        result = generate_plot(csv_data, "bar", json_kwargs='{"x": "category", "y": "values"}')

        text_content, image_content = result
        assert text_content.text == "Plot generated successfully"
        assert image_content.mimeType == "image/png"

        # Verify the image data is valid
        decoded_data = base64.b64decode(image_content.data)
        assert decoded_data.startswith(b"\x89PNG")

    def test_generate_plot_pie_chart(self):
        """Test pie chart generation."""
        csv_data = "category,values\nA,30\nB,45\nC,25"

        result = generate_plot(csv_data, "pie")

        text_content, image_content = result
        assert text_content.text == "Plot generated successfully"
        assert image_content.mimeType == "image/png"

        # Verify the image data is valid
        decoded_data = base64.b64decode(image_content.data)
        assert decoded_data.startswith(b"\x89PNG")

    def test_generate_plot_default_parameters(self):
        """Test plot generation with default parameters."""
        csv_data = "x,y\n1,2\n2,4\n3,6"

        # Using defaults: plot_type="line", json_kwargs="None"
        result = generate_plot(csv_data)

        text_content, image_content = result
        assert text_content.text == "Plot generated successfully"
        assert image_content.mimeType == "image/png"

    def test_generate_plot_with_title_and_labels(self):
        """Test plot generation with title and axis labels."""
        csv_data = "x,y\n1,2\n2,4\n3,6"
        kwargs = {"x": "x", "y": "y", "title": "Test Plot", "xlabel": "X Axis", "ylabel": "Y Axis"}

        result = generate_plot(csv_data, "line", json.dumps(kwargs))

        text_content, image_content = result
        assert text_content.text == "Plot generated successfully"
        assert image_content.mimeType == "image/png"

    def test_generate_plot_invalid_json_kwargs(self):
        """Test that invalid JSON kwargs raises exception."""
        csv_data = "x,y\n1,2\n2,4\n3,6"
        invalid_json = '{"x": "x", "y": "y", invalid}'

        with pytest.raises(json.JSONDecodeError):
            generate_plot(csv_data, "line", invalid_json)

    def test_generate_plot_invalid_csv_data(self):
        """Test that invalid CSV data raises exception."""
        invalid_csv = "not,valid,csv\ndata"

        with pytest.raises(ValueError, match="CSV data contains NaN/null values"):
            generate_plot(invalid_csv, "line", '{"x": "not", "y": "valid"}')

    def test_generate_plot_empty_csv_data(self):
        """Test that empty CSV data raises exception."""
        empty_csv = ""

        with pytest.raises(EmptyDataError, match="No columns to parse from file"):
            generate_plot(empty_csv, "line")

    def test_generate_plot_unsupported_plot_type(self):
        """Test that unsupported plot type raises exception."""
        csv_data = "x,y\n1,2\n2,4\n3,6"

        with pytest.raises(ValueError, match="Unsupported plot type"):
            generate_plot(csv_data, "unsupported_type")

    def test_generate_plot_worldmap_type(self):
        """Test worldmap plot generation."""
        csv_data = "lat,lon\n-33.941,18.467\n-33.942,18.468\n-33.941,18.467"

        result = generate_plot(csv_data, "worldmap")

        text_content, image_content = result
        assert text_content.text == "Plot generated successfully"
        assert image_content.mimeType == "image/png"

        # Verify the image data is valid
        decoded_data = base64.b64decode(image_content.data)
        assert decoded_data.startswith(b"\x89PNG")

    def test_generate_plot_with_seaborn_hue(self):
        """Test plot generation with seaborn hue parameter."""
        csv_data = "x,y,category\n1,2,A\n2,4,B\n3,6,A\n4,8,B\n5,10,A"
        kwargs = {"x": "x", "y": "y", "hue": "category"}

        result = generate_plot(csv_data, "line", json.dumps(kwargs))

        text_content, image_content = result
        assert text_content.text == "Plot generated successfully"
        assert image_content.mimeType == "image/png"

    def test_generate_plot_rejects_nan_values(self):
        """Test that CSV data with NaN values raises ValueError."""
        csv_data_with_nan = "x,y\n1,2\n2,\n3,6"  # Missing value in second row

        with pytest.raises(ValueError, match="CSV data contains NaN/null values"):
            generate_plot(csv_data_with_nan, "line", '{"x": "x", "y": "y"}')

    def test_generate_plot_rejects_completely_empty_cells(self):
        """Test that CSV data with completely empty cells raises ValueError."""
        csv_data_with_empty = "x,y\n1,2\n,4\n3,6"  # Missing value in first column

        with pytest.raises(ValueError, match="CSV data contains NaN/null values"):
            generate_plot(csv_data_with_empty, "line", '{"x": "x", "y": "y"}')
