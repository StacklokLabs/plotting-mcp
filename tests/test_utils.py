"""Tests for utility functions."""

from plotting_mcp.utils import sizeof_fmt


class TestUtilsIntegration:
    """Integration tests for utility functions."""

    def test_sizeof_fmt_realistic_file_sizes(self):
        """Test sizeof_fmt with realistic file sizes."""
        # Common file sizes
        sizes = {
            1024: "1.0KiB",  # 1KB file
            4096: "4.0KiB",  # 4KB file
            102400: "100.0KiB",  # 100KB file
            1048576: "1.0MiB",  # 1MB file
            10485760: "10.0MiB",  # 10MB file
            104857600: "100.0MiB",  # 100MB file
            1073741824: "1.0GiB",  # 1GB file
        }

        for size, expected in sizes.items():
            assert sizeof_fmt(size) == expected
