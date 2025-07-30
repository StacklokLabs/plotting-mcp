import io
from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from plotting_mcp.constants import (
    DEFAULT_DPI,
    DEFAULT_FIGURE_SIZE,
)


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


def _create_matplotlib_plot(  # noqa: C901
    df: pd.DataFrame, plot_type: str, **kwargs
) -> tuple[plt.Figure, plt.Axes]:
    """Create a plot using matplotlib/seaborn."""
    if df.empty:
        raise ValueError("CSV data is empty")

    supported_plot_types = ["line", "bar", "pie"]
    if plot_type not in supported_plot_types:
        raise ValueError(
            f"Unsupported plot type: {plot_type}. Supported types: {supported_plot_types}"
        )

    fig, ax = plt.subplots(figsize=DEFAULT_FIGURE_SIZE, dpi=DEFAULT_DPI)

    # Extract optional parameters for figure title and axis labels
    # These are not accepted by Seaborn
    fig_title, xlabel, ylabel = None, None, None
    if "title" in kwargs:
        fig_title = kwargs.pop("title")
    if "xlabel" in kwargs:
        xlabel = kwargs.pop("xlabel")
    if "ylabel" in kwargs:
        ylabel = kwargs.pop("ylabel")

    if plot_type == "line":
        sns.lineplot(data=df, ax=ax, **kwargs)
    elif plot_type == "bar":
        sns.barplot(data=df, ax=ax, **kwargs)
    elif plot_type == "pie":
        ax.pie(df, **kwargs)

    # Auto-rotate x-axis labels if needed (not applicable for pie charts)
    if plot_type != "pie":
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
    fig, _ = _create_matplotlib_plot(df, plot_type, **kwargs)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def plot_and_show(df: pd.DataFrame, plot_type: str, **kwargs) -> None:
    """Generate a plot and display it."""
    fig, _ = _create_matplotlib_plot(df, plot_type, **kwargs)
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    # Example usage
    data = {"x": [1, 2, 3, 4, 5], "y": [2, 3, 5, 7, 11]}
    df = pd.DataFrame(data)
    plot_and_show(df, "line")
