"""Smoke tests for the zero-thickness flasher plotting helper."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from starshade_flasher.patterns import generate_zero_thickness_flasher
from starshade_flasher.visualization import plot_zero_thickness_flasher


def test_plot_zero_thickness_saves_image(tmp_path):
    pattern = generate_zero_thickness_flasher(N=8, n=5, A=1.0)
    output = tmp_path / "plot.png"

    plot_zero_thickness_flasher(pattern, show=False, save_path=output)

    assert output.exists()
    assert output.stat().st_size > 0
