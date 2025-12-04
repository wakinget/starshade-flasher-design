"""Quick script to visualize a zero-thickness flasher pattern."""

from starshade_flasher.patterns import generate_zero_thickness_flasher
from starshade_flasher.visualization import plot_zero_thickness_flasher


if __name__ == "__main__":
    pattern = generate_zero_thickness_flasher(N=12, n=8, A=1.0)
    plot_zero_thickness_flasher(pattern, show=True)
