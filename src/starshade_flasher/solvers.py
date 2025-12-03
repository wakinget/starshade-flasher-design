"""Numerical solvers and helper utilities for starshade flashers."""

from __future__ import annotations

from typing import Any, Callable, Dict, Sequence


def solve_per_ring_isometry(initial_guess: Sequence[float], constraints: Callable[[Sequence[float]], Sequence[float]], **kwargs: Any) -> Dict[str, Any]:
    """
    Placeholder for the per-ring isometry solver.

    The eventual implementation will wrap a SciPy root-finding routine
    to enforce equality of deployed and stowed fold-line lengths for
    each ring of the flasher.
    """

    raise NotImplementedError("Per-ring isometry solver is not yet implemented.")


def numerical_jacobian(func: Callable[[Sequence[float]], Sequence[float]], x0: Sequence[float], **kwargs: Any) -> Any:
    """
    Placeholder for a numerical Jacobian calculator.

    This helper will estimate partial derivatives needed by the solver
    routines using finite differences or more advanced schemes.
    """

    raise NotImplementedError("Numerical Jacobian computation is not yet implemented.")
