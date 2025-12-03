"""Geometry data structures for starshade flashers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Tuple

Vec2 = Tuple[float, float]
Vec3 = Tuple[float, float, float]
Vec = Vec2 | Vec3
FoldType = Literal[
    "mountain",
    "valley",
    "neutral",
    "major",
    "minor",
    "diagonal",
    "hub",
]


@dataclass
class Vertex:
    """Vertex in 2D or 3D space.

    The zero-thickness flasher operates entirely in the xy-plane, but we allow
    a 3D coordinate for compatibility with downstream thickness-aware tools.

    Parameters
    ----------
    position:
        Cartesian coordinates of the vertex (2D or 3D).
    index:
        Optional integer identifier for mesh indexing. When vertices are
        returned from pattern generators, this is populated to make edge
        references explicit.
    label:
        Optional human-readable label for debugging or visualization overlays.
    """

    position: Vec
    index: Optional[int] = None
    label: Optional[str] = None


@dataclass
class Edge:
    """Representation of a crease or mesh edge.

    Edges reference vertices by index rather than storing full ``Vertex``
    instances. This keeps the data model lightweight and makes it easier to
    serialize crease patterns.

    Parameters
    ----------
    start:
        Index of the starting vertex.
    end:
        Index of the ending vertex.
    fold_type:
        Classification for the crease (e.g., mountain, valley, major, minor,
        hub). ``None`` can be used for untyped mesh edges.
    fold_angle:
        Target fold angle in radians; sign convention to be defined in future
        work.
    """

    start: int
    end: int
    fold_type: Optional[FoldType] = None
    fold_angle: Optional[float] = None


@dataclass
class Face:
    """
    Placeholder for a triangular face in the flasher mesh.

    Parameters
    ----------
    vertices:
        Ordered tuple of the three vertices defining the face.
    normal:
        Optional precomputed face normal.
    """

    vertices: Tuple[Vertex, Vertex, Vertex]
    normal: Optional[Vec3] = None
