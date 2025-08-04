import io
from typing import Literal

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from cartopy.mpl.geoaxes import GeoAxes

from plotting_mcp.constants import PLOT_DPI, PLOT_FIGURE_SIZE


def _auto_rotate_labels(ax: plt.Axes, axis: Literal["x", "y"] = "x") -> None:
    """Automatically rotate axis labels if they are too numerous or too long."""
    if axis not in ["x", "y"]:
        raise ValueError("Axis must be 'x' or 'y'")

    if axis == "x":
        labels = ax.get_xticklabels()
    else:
        labels = ax.get_yticklabels()

    if not labels:
        return

    # Get the actual text content of labels
    label_texts = [label.get_text() for label in labels if label.get_text()]

    if not label_texts:
        return

    # Check conditions for rotation
    num_labels = len(label_texts)
    max_label_length = max(len(str(text)) for text in label_texts)
    avg_label_length = sum(len(str(text)) for text in label_texts) / num_labels

    # Rotation criteria:
    # 1. More than 8 labels
    # 2. Any label longer than 15 characters
    # 3. Average label length > 10 characters
    should_rotate = num_labels > 8 or max_label_length > 15 or avg_label_length > 10

    if should_rotate:
        ax.tick_params(axis=axis, labelrotation=90)


def _create_world_map_plot(ax: GeoAxes, df: pd.DataFrame, **kwargs) -> None:
    """Create a world map with coordinate points."""
    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN, color="lightblue")
    ax.add_feature(cfeature.LAND, color="lightgray")

    # Set global extent
    ax.set_global()

    # Extract coordinate columns - support common naming conventions
    lat_col = None
    lon_col = None

    # Try to find latitude column
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ["lat", "latitude", "y"]:
            lat_col = col
            break

    # Try to find longitude column
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ["lon", "lng", "long", "longitude", "x"]:
            lon_col = col
            break

    if lat_col is None or lon_col is None:
        raise ValueError(
            "Could not find latitude/longitude columns. "
            "Expected columns named: lat/latitude/y and lon/long/lng/longitude/x"
        )

    # Extract plotting parameters
    marker_size = kwargs.pop("s", 50)
    marker_color = kwargs.pop("c", "red")
    marker_alpha = kwargs.pop("alpha", 0.7)
    marker_style = kwargs.pop("marker", "o")

    # Plot points on the map
    ax.scatter(
        df[lon_col],
        df[lat_col],
        s=marker_size,
        c=marker_color,
        alpha=marker_alpha,
        marker=marker_style,
        transform=ccrs.PlateCarree(),
        **kwargs,
    )

    # Add gridlines
    ax.gridlines(draw_labels=True, alpha=0.3)


def _create_pie_plot(ax: plt.Axes, df: pd.DataFrame, **kwargs) -> None:
    """Create a pie chart."""
    # Ensure we have a single column for pie chart
    if len(df.columns) > 2:
        raise ValueError(
            "Pie chart requires either one column of data or two columns for a breakdown, "
            "where the first column is the category and the second is the value."
        )

    if len(df.columns) == 1:
        labels = kwargs.pop("labels", None)
        if labels is None:
            labels = df.iloc[:, 0].unique()

        # If only one column, use it as the value counts
        ax.pie(df.iloc[:, 0].value_counts(), labels=labels, autopct="%1.1f%%", **kwargs)
    elif len(df.columns) == 2:
        provided_labels = kwargs.pop("labels", None)
        if provided_labels is not None:
            raise ValueError(
                "Pie chart with two columns does not accept 'labels' parameter. "
                "Use the first column as labels and the second as values."
            )

        # If two columns, assume first is category and second is value
        ax.pie(
            df.iloc[:, 1],
            labels=df.iloc[:, 0],
            autopct="%1.1f%%",
            **kwargs,
        )


def _create_plot(  # noqa: C901
    df: pd.DataFrame, plot_type: str, **kwargs
) -> tuple[plt.Figure, plt.Axes]:
    """Create a plot using matplotlib/seaborn."""
    if df.empty:
        raise ValueError("CSV data is empty")

    # Validate that the DataFrame contains no NaN values
    if df.isnull().any().any():
        raise ValueError("CSV data contains NaN/null values. Please ensure all data is complete.")

    supported_plot_types = ["line", "bar", "pie", "worldmap"]
    if plot_type not in supported_plot_types:
        raise ValueError(
            f"Unsupported plot type: {plot_type}. Supported types: {supported_plot_types}"
        )

    # Create figure with appropriate projection for world map
    if plot_type == "worldmap":
        fig = plt.figure(figsize=PLOT_FIGURE_SIZE, dpi=PLOT_DPI)
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    else:
        fig, ax = plt.subplots(figsize=PLOT_FIGURE_SIZE, dpi=PLOT_DPI)

    # Extract optional parameters for figure title and axis labels
    # These are not accepted by Seaborn
    fig_title = kwargs.pop("title", None)
    xlabel = kwargs.pop("xlabel", None)
    ylabel = kwargs.pop("ylabel", None)

    if plot_type == "line":
        sns.lineplot(data=df, ax=ax, **kwargs)
    elif plot_type == "bar":
        sns.barplot(data=df, ax=ax, **kwargs)
    elif plot_type == "pie":
        _create_pie_plot(ax, df, **kwargs)
    elif plot_type == "worldmap":
        # Cartopy doesn't return correct Axes type, so we ignore type checking
        _create_world_map_plot(ax, df, **kwargs)  # ty: ignore[invalid-argument-type]

    # Auto-rotate x-axis labels if needed (not applicable for pie charts or world maps)
    if plot_type not in ["pie", "worldmap"]:
        _auto_rotate_labels(ax, axis="x")

    # Set titles and labels
    if fig_title:
        ax.set_title(fig_title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    fig.tight_layout()

    return fig, ax


def plot_to_bytes(df: pd.DataFrame, plot_type: str, **kwargs) -> bytes:
    """Generate a plot and return it as bytes."""
    fig, _ = _create_plot(df, plot_type, **kwargs)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def plot_and_show(df: pd.DataFrame, plot_type: str, **kwargs) -> None:
    """Generate a plot and display it."""
    fig, _ = _create_plot(df, plot_type, **kwargs)
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    # Example data for worldmap plot
    # data = {
    #     "lat": [-33.941, -33.942, -33.941, -33.936, -33.944],
    #     "long": [18.467, 18.468, 18.467, 18.467, 18.470],
    # }
    # Example data for pie plot
    data = {
        "version": ["0.2.0", "0.1.8", "0.1.5", "0.1.9", "0.2.1"],
        "event_count": [2083, 1298, 1267, 537, 533],
    }
    df = pd.DataFrame(data)
    plot_and_show(df, "pie")
