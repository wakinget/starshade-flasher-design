"""Visualization helpers for starshade flasher geometries."""

from __future__ import annotations

from typing import Any, Iterable, Optional

import matplotlib.pyplot as plt


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
