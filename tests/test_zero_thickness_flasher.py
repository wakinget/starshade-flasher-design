"""Tests for the zero-thickness flasher generator."""

from __future__ import annotations

import math
from typing import List

import numpy as np

from starshade_flasher.patterns import generate_zero_thickness_flasher


def _coords(vertices, indices: List[int]) -> np.ndarray:
    return np.array([vertices[i].position[:2] for i in indices], dtype=float)


def test_rotational_symmetry():
    pattern = generate_zero_thickness_flasher(N=6, n=3, A=0.5, L=[0.0, 1.0, 2.0, 3.0])
    vertices = pattern["vertices"]
    radial_lines = pattern["radial_lines"]
    beta = pattern["beta"]

    base_line = _coords(vertices, radial_lines[0])
    for k in range(6):
        theta = k * beta
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        rotated = base_line @ rot.T
        target = _coords(vertices, radial_lines[k])
        assert np.allclose(rotated, target, atol=1e-10)


def test_hub_polygon_edge_equality():
    pattern = generate_zero_thickness_flasher(N=8, n=2, A=1.0, L=[0.0, 1.0, 1.5])
    vertices = pattern["vertices"]
    radial_lines = pattern["radial_lines"]

    hub_coords = _coords(vertices, [line[0] for line in radial_lines])
    lengths = np.linalg.norm(np.roll(hub_coords, -1, axis=0) - hub_coords, axis=1)
    assert np.allclose(lengths, lengths[0], atol=1e-12)


def test_radial_major_fold_linearity():
    pattern = generate_zero_thickness_flasher(N=5, n=4, A=0.3, L=[0.0, 0.5, 1.0, 1.5, 2.0])
    vertices = pattern["vertices"]
    radial_lines = pattern["radial_lines"]

    for line in radial_lines:
        coords = _coords(vertices, line)
        direction = coords[1] - coords[0]
        for vec in coords[1:] - coords[0]:
            cross = direction[0] * vec[1] - direction[1] * vec[0]
            assert math.isclose(cross, 0.0, abs_tol=1e-12)
