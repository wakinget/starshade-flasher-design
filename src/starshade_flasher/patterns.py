"""Crease-pattern generation utilities for starshade flashers."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence

from .geometry import Edge, Vertex


def generate_zero_thickness_flasher(N: int, n: int, A: float, L: Sequence[float]) -> Dict[str, Any]:
    """Generate the planar zero-thickness flasher pattern.

    This follows the deployed-state geometry in
    :mod:`docs.math.guest_pellegrino_flashing` and uses the notation from the
    accompanying math note. The construction is purely radial: each major fold
    is a ray starting from a hub vertex ``p_k`` with direction ``u_k`` and
    distances ``L_i``. Minor folds connect corresponding points on adjacent
    major folds.

    Parameters
    ----------
    N:
        Number of gores / major folds.
    n:
        Number of vertices along each major fold *excluding* the hub (there are
        ``n+1`` vertices per radial line when the hub is included).
    A:
        Hub radius (circumradius of the central regular polygon).
    L:
        Strictly increasing radial distances of length ``n+1`` with ``L[0]=0``.

    Returns
    -------
    Dict[str, Any]
        A dictionary with the following keys:

        ``vertices``
            List of :class:`~starshade_flasher.geometry.Vertex` objects with
            populated ``index`` fields.
        ``edges``
            List of :class:`~starshade_flasher.geometry.Edge` instances
            referencing vertex indices. Edge ``fold_type`` values are ``"hub"``
            (hub polygon), ``"major"`` (radial folds), and ``"minor"`` (lines
            between adjacent major folds).
        ``radial_lines``
            Indices of vertices along each major fold (including the hub at
            position ``0``). This mirrors the ``m_i`` / ``v_i`` notation in the
            math note and is provided to simplify downstream tests and
            visualization.
        ``beta``
            The angular width of a gore (``2π/N``).

    Notes
    -----
    The function does not deduplicate shared vertices between adjacent gores
    beyond the hub polygon. Each radial line is represented explicitly to keep
    the construction transparent and to align with the symmetry arguments in
    the math note.
    """

    if N < 3:
        raise ValueError("N must be at least 3 to form a polygonal hub.")
    if n < 1:
        raise ValueError("n must be at least 1 to place vertices beyond the hub.")
    if len(L) != n + 1:
        raise ValueError("L must have length n+1, including the hub distance L[0].")
    if any(L[i] <= L[i - 1] for i in range(1, len(L))):
        raise ValueError("L must be strictly increasing from the hub outward.")

    beta = 2 * math.pi / N
    directions = [(math.cos(k * beta), math.sin(k * beta)) for k in range(N)]

    vertices: List[Vertex] = []
    radial_lines: List[List[int]] = [[] for _ in range(N)]

    # Hub vertices p_k.
    for k, (ux, uy) in enumerate(directions):
        position = (A * ux, A * uy)
        idx = len(vertices)
        vertices.append(Vertex(position=position, index=idx, label=f"p{k}"))
        radial_lines[k].append(idx)

    # Points along each radial line (major fold).
    for k, (ux, uy) in enumerate(directions):
        hub_pos = vertices[radial_lines[k][0]].position
        hub_x, hub_y = hub_pos[0], hub_pos[1]
        for i in range(1, n + 1):
            position = (hub_x + L[i] * ux, hub_y + L[i] * uy)
            idx = len(vertices)
            vertices.append(Vertex(position=position, index=idx, label=f"r{k}_{i}"))
            radial_lines[k].append(idx)

    edges: List[Edge] = []

    # Hub polygon edges.
    for k in range(N):
        start = radial_lines[k][0]
        end = radial_lines[(k + 1) % N][0]
        edges.append(Edge(start=start, end=end, fold_type="hub"))

    # Major folds along each radial line.
    for k in range(N):
        line = radial_lines[k]
        for i in range(len(line) - 1):
            edges.append(Edge(start=line[i], end=line[i + 1], fold_type="major"))

    # Minor folds connecting adjacent major folds at the same radial distance.
    for k in range(N):
        next_k = (k + 1) % N
        for i in range(1, n + 1):
            edges.append(
                Edge(start=radial_lines[k][i], end=radial_lines[next_k][i], fold_type="minor")
            )

    return {
        "vertices": vertices,
        "edges": edges,
        "radial_lines": radial_lines,
        "beta": beta,
    }


def generate_thickness_accommodating_pattern(sides: int, radius: float, layer_spacing: float, **kwargs: Any) -> Dict[str, Any]:
    """
    Placeholder for thickness-accommodating flasher pattern generation.

    This stub will later incorporate spiral fold layouts and per-ring
    spacing strategies to reduce panel interference in stowed
    configurations.
    """

    raise NotImplementedError("Thickness-accommodating pattern generation is not yet implemented.")
