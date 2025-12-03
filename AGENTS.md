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

## Mathematical References

Codex should treat the following math notes as the authoritative specifications for
all geometric and numerical algorithms in this project. When implementing or modifying
code related to crease-pattern generation, isometry solves, stowed/deployed mappings,
or tessellation logic, consult these files **first**:

- docs/math/guest_pellegrino_flashing.md  
  Zero-thickness flasher geometry; major/minor fold layout; angular compatibility
  near the hub; analytic planar crease pattern generation.

- docs/math/arya2021_optical_shield.md  
  Thickness-accommodating spiral-wrapped flasher; mountain/valley stowed spirals;
  nested ring-by-ring solver for planar deployed surfaces; length-matching constraints.

- docs/math/kreider_arya_corrugated.md  
  Generalization to corrugated (non-flat) deployed surfaces; full two-level nested
  isometry solver (inner twist angle ψ, outer height/corrugation parameter h);
  developable surface embedding S(u,v).

- docs/math/jatusripitak_arya_tessellations.md  
  Tessellation constraints for joining multiple flasher units into regular or
  semi-regular tilings (triangular, square, hexagonal); join conditions for
  sector angles, fold-type compatibility, and edge-length matching.

These documents define:
- coordinate systems,
- notation tables,
- equations and geometric constraints,
- algorithm descriptions and pseudocode,
- expected inputs and outputs for implementation,
- testable invariants.

When a task involves generating crease patterns, solving ring geometry, or assembling
tessellations, Codex should open the relevant math note and follow the exact equations
and constraints described there.

## What Codex Should Do

- Maintain consistency across modules.
- Follow mathematical definitions from the referenced papers and math docs.
- Respect the roadmap in `docs/ROADMAP.md`.
- When modifying multiple files, group related edits into clear PRs.