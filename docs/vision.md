# Starshade Flasher Design — Project Vision

This document captures the long-term goals, philosophy, and possible growth paths
for the **starshade-flasher-design** project. It serves as a high-level guide for
future development decisions, user-facing features, and project scope expansion.


# 1. Core Purpose

The foundational purpose of this project is to create a clean, modern, reliable tool
for **generating origami flasher fold patterns** inspired by:

- Guest & Pellegrino (1992) — zero-thickness geometry
- Arya et al. (2021) — thickness-accommodating spiral wrapping
- Kreider & Arya (2024) — corrugated, developable surfaces
- Jatusripitak & Arya (2024) — tessellations of flasher cells

At the simplest level:

**The project should allow a user to generate printable crease patterns that can be
cut and folded into physical scale models.**

Everything else builds upon that central goal.


# 2. Short-Term Vision (MVP)

The near-term objective is to build a small but powerful “flasher workbench” that can:

1. **Generate crease patterns**  
   Using zero-thickness (G&P) or thickness-accommodating (Arya/Kreider) algorithms.

2. **Export printable formats**  
   SVG, PDF, or DXF files with:
   - crease lines,
   - fold types (mountain/valley),
   - hub geometry,
   - optional annotations.

3. **Visualize geometry**  
   - 2D deployed crease pattern
   - 3D stowed/spiral representation (even approximate)

4. **Compare designs**  
   Produce two (or more) crease patterns with different parameters so the user can
   fold physical models and compare stowed size, gore count, thickness effects, etc.

This MVP is primarily for personal exploration and model building, but designed
carefully so that future expansion is easy.


# 3. Medium-Term Vision (Library-Level)

With the mathematical foundations captured in `docs/math/`, this project can naturally
grow into a clean, reusable Python library for:

- Generating flasher-like origami patterns from multiple theoretical formulations.
- Running numerical solvers for thickness accommodation or corrugated surfaces.
- Exporting patterns for simulation, fabrication, or demonstration.
- Conducting parameter studies for wrapped membrane geometries.
- Supporting flexible design exploration for deployable structures.

In this stage, the project becomes a **general-purpose flasher/origami toolkit** with:

- stable APIs (`patterns`, `solvers`, `export`, `visualization`)
- extensive unit tests
- notebooks demonstrating specific techniques and reproducing figures from the papers
- modular surface definitions (planar, conical, corrugated)


# 4. Long-Term Vision (Applications and Extensions)

With a solid core, the project could support a variety of advanced applications:

## 4.1 Design Trade Tools
- Explore wrap-to-diameter relationships.
- Compare different gore counts (N) for compactness and strain.
- Visualize wrap thickness vs stowed diameter.
- Analyze pattern sensitivity to layer spacing or corrugation depth.

## 4.2 Research and Education
- Provide a reference implementation of multiple flasher geometries.
- Offer interactive notebooks for teaching origami-inspired design.
- Allow researchers to reproduce figures from the cited papers using code.

## 4.3 Multi-Cell Tessellations
- Use Jatusripitak & Arya (2024) join conditions to assemble larger structures.
- Allow users to generate custom tilings (triangular, square, hexagonal).
- Export tessellated crease patterns.

## 4.4 Integration with CAD and Fabrication
- Export DXF/SVG for laser cutting or plotter fabrication.
- Generate metadata for downstream mechanical/optical modeling tools.

## 4.5 Optional GUI Layer
A future graphical interface (web-based or desktop) could:
- Provide sliders and text inputs for flasher parameters.
- Live-render deployed and stowed configurations.
- Allow “side-by-side comparison” between designs.
- Offer one-click export to PDF/SVG.
- Make the tool approachable for education, outreach, and rapid prototyping.

This GUI should remain a thin layer on top of the library’s stable API.


# 5. Project Philosophy

This project aims to balance **high-fidelity mathematics** with **practical usability**:

- Use mathematically correct formulations rooted in the referenced papers.
- Favor clarity in code over cleverness.
- Maintain modular structure: geometry → solver → pattern → export.
- Let the math notes serve as the authoritative source for algorithms.
- Encourage experimentation (e.g., custom surfaces or tessellations).
- Enable both simple usage (“give me a fold pattern”) and deep research workflows.


# 6. Guiding Design Principles

1. **Mathematical correctness first.**
   Follow the equations and constraints in `docs/math/` exactly.

2. **Modularity.**
   Users should be able to swap surfaces, solvers, or export formats.

3. **Extensibility.**
   Future algorithms (e.g., new surface types, new tilings) should fit easily.

4. **Traceability.**
   All implemented equations must point back to the math notes and cited papers.

5. **User-centric workflows.**
   Make it easy to:
   - generate a crease pattern,
   - visualize it,
   - export it,
   - fold it,
   - compare it.

6. **Low barrier to entry, high ceiling.**
   Beginners get printable patterns; experts get a research-grade library.


# 7. Summary

This project begins as a tool to generate crease patterns for physical demonstrations
but has the potential to grow into a flexible, mathematically grounded platform for
origami-inspired flasher design, analysis, and visualization.

By maintaining clean structure, clear math references, and modular code, the project
can scale naturally from paper-folding demonstrations to research-grade modeling and
design tools — and potentially to a full GUI or interactive design environment.
