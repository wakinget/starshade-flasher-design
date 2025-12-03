# Codex Instructions — Starshade Flasher Design

Codex, you are assisting with the development of a Python 3.11 library that generates and visualizes origami flasher fold patterns for starshade-like deployable structures.

## Project Scope

- Implement geometric + numerical algorithms for:
  - Zero-thickness flashers (Guest & Pellegrino 1992)
  - Thickness-accommodating spiral flashers (Arya et al. 2021; Kreider & Arya 2024)
  - Tessellation-related constraints (Jatusripitak & Arya 2024)

- Provide clean Python interfaces to:
  - Generate deployed & folded vertex coordinates
  - Compute fold-line lengths and enforce isometry constraints
  - Run numerical solvers for thickness accommodation
  - Visualize results using matplotlib (2D & 3D)

- Provide testing, documentation, and examples.

## Coding Guidelines

- Language: **Python 3.11**
- Use `numpy` for geometry; `scipy.optimize` for solvers.
- Structure code under `src/starshade_flasher/`
- Use descriptive, type-annotated functions with docstrings.
- Avoid excessive cleverness: clarity > brevity.
- Include unit tests (`pytest`) whenever adding new modules.

## File Structure Expectations

- `geometry.py`: data classes for vertices, edges (mountain/valley/etc), faces.
- `patterns.py`: flasher generation algorithms.
- `solvers.py`: numerical optimization utilities.
- `visualization.py`: 2D/3D plotting helpers.
- `references.py`: metadata for original papers and citation helpers.
- `tests/`: unit tests for geometry, pattern generation, solvers.

## What Codex Should Do

- Maintain consistency across modules.
- Follow mathematical definitions from the referenced papers.
- Respect the roadmap in `docs/ROADMAP.md`.
- When modifying multiple files, group related edits into clear PRs.