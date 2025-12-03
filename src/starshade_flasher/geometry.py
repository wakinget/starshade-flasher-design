"""Geometry data structures for starshade flashers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Tuple

Vec3 = Tuple[float, float, float]
FoldType = Literal["mountain", "valley", "neutral", "major", "minor", "diagonal"]


@dataclass
class Vertex:
    """
    Placeholder for a vertex in 3D space.

    Parameters
    ----------
    position:
        Cartesian coordinates of the vertex.
    index:
        Optional integer identifier for mesh indexing.
    """

    position: Vec3
    index: Optional[int] = None


@dataclass
class Edge:
    """
    Placeholder representation of a crease or mesh edge.

    Parameters
    ----------
    start:
        Starting vertex of the edge.
    end:
        Ending vertex of the edge.
    fold_type:
        Classification for the crease (e.g., mountain, valley, major, minor).
    fold_angle:
        Target fold angle in radians; sign convention to be defined in future work.
    """

    start: Vertex
    end: Vertex
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
