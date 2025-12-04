"""Visualization helpers for starshade flasher geometries."""

from __future__ import annotations

from typing import Any, Iterable, Optional

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def _edge_style(fold_type: Optional[str]) -> tuple[str, float]:
    """Return a color and linewidth for a given fold type."""

    if fold_type == "valley":
        return "red", 1.5
    if fold_type == "mountain":
        return "blue", 1.5
    if fold_type == "major":
        return "blue", 2.5
    if fold_type == "minor":
        return "red", 1.5
    if fold_type == "hub":
        return "black", 1.0
    return "blue", 1.0


def plot_zero_thickness_flasher(
    pattern,
    ax=None,
    show: bool = False,
    save_path: str | None = None,
) -> "matplotlib.axes.Axes":
    """
    Plot a top-down view of a zero-thickness flasher crease pattern.

    Parameters
    ----------
    pattern : object
        The result of generate_zero_thickness_flasher(...), or the
        appropriate pattern object produced in Task 1. It should contain
        vertices and edges with enough information to distinguish
        mountain/valley folds (and major/minor folds if available).
    ax : matplotlib.axes.Axes, optional
        Existing axes to draw into. If None, create a new figure/axes.
    show : bool, default False
        If True, call plt.show() at the end (for interactive use).
    save_path : str or None, default None
        If not None, save the figure to this path (e.g. PNG or PDF).
    """

    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure

    vertices = pattern.get("vertices", [])
    edges = pattern.get("edges", [])
    faces = pattern.get("faces", [])

    if faces:
        for face in faces:
            coords = [(v.position[0], v.position[1]) for v in face.vertices]
            patch = Polygon(coords, closed=True, facecolor="0.9", edgecolor=None, alpha=0.3)
            ax.add_patch(patch)

    for edge in edges:
        start = vertices[edge.start].position
        end = vertices[edge.end].position
        color, linewidth = _edge_style(getattr(edge, "fold_type", None))
        ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=linewidth)

    ax.set_aspect("equal", "box")
    ax.axis("off")

    if save_path is not None:
        fig.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()

    return ax


def plot_3d_mesh(vertices: Iterable[Any], faces: Iterable[Any], *, fold_lines: Optional[Iterable[Any]] = None, ax: Optional[Any] = None) -> Any:
    """
    Placeholder for 3D mesh visualization using matplotlib.

    The final implementation will render triangular faces alongside
    colored fold lines to distinguish mountain and valley creases.
    """

    raise NotImplementedError("3D mesh visualization is not yet implemented.")


def plot_deployed_and_stowed(*args: Any, **kwargs: Any) -> Any:
    """
    Placeholder for side-by-side deployed and stowed visualization.

    Future functionality will plot the deployed crease pattern next to
    a folded configuration to highlight isometry results and collision
    checks.
    """

    raise NotImplementedError("Deployed/stowed visualization is not yet implemented.")
