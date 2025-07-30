#!/usr/bin/env python3
"""
Pre-download Cartopy map data during Docker build to avoid runtime downloads.
"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from cartopy.mpl.geoaxes import GeoAxes


def download_cartopy_features():
    """Download all Cartopy features used in the plotting code."""
    print("Downloading Cartopy map data...")

    # Create a temporary figure to trigger feature downloads
    fig = plt.figure(figsize=(10, 8))
    ax: GeoAxes = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())  # ty: ignore[invalid-assignment]

    # Add all features used in the plotting code
    print("- Downloading COASTLINE...")
    ax.add_feature(cfeature.COASTLINE)

    print("- Downloading BORDERS...")
    ax.add_feature(cfeature.BORDERS)

    print("- Downloading OCEAN...")
    ax.add_feature(cfeature.OCEAN)

    print("- Downloading LAND...")
    ax.add_feature(cfeature.LAND)

    # Set global extent to ensure all data is downloaded
    ax.set_global()

    # Force rendering to trigger downloads
    fig.canvas.draw()

    # Clean up
    plt.close(fig)

    print("Cartopy map data downloaded successfully!")


if __name__ == "__main__":
    download_cartopy_features()
