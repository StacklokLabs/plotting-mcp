import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from plotting_mcp.constants import (
    DEFAULT_DPI,
    DEFAULT_FIGURE_SIZE,
)


def _create_matplotlib_plot(
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

    if plot_type == "line":
        sns.lineplot(data=df, ax=ax, **kwargs)
    elif plot_type == "bar":
        sns.barplot(data=df, ax=ax, **kwargs)
    elif plot_type == "pie":
        ax.pie(df, **kwargs)

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
