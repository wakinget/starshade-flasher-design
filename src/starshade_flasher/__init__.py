"""Starshade flasher design library."""

from __future__ import annotations

from .geometry import Edge, Face, Vertex
from .patterns import generate_thickness_accommodating_pattern, generate_zero_thickness_pattern
from .solvers import numerical_jacobian, solve_per_ring_isometry
from .visualization import plot_3d_mesh, plot_deployed_and_stowed

__all__ = [
    "Edge",
    "Face",
    "Vertex",
    "generate_thickness_accommodating_pattern",
    "generate_zero_thickness_pattern",
    "numerical_jacobian",
    "plot_3d_mesh",
    "plot_deployed_and_stowed",
    "solve_per_ring_isometry",
]

__version__ = "0.0.0"
