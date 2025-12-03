# Starshade Flasher Design — Project Roadmap

This roadmap tracks the major phases of development for the starshade flasher design library.

---

## Phase 1 — Foundations (Geometry + Visualization)

### Geometry
- [ ] Implement core data structures:
  - `Vertex` (3D coordinates)
  - `Edge` (type: major/minor/diagonal; mountain/valley; fold angle)
  - `Face` (triangular mesh elements)
- [ ] Add helper functions for:
  - Vector operations (distance, normalization, dot, cross)
  - Rotation matrices (especially n-fold rotations)

### Visualization
- [ ] Basic 3D mesh plotting using matplotlib:
  - Grey triangular faces
  - Red = valley, Blue = mountain fold lines
  - Color saturation proportional to fold angle (as shown in reference figures)
- [ ] Side-by-side deployed/folded view
- [ ] Optional inset zoom for a single gore

---

## Phase 2 — Zero-Thickness Flasher Generation  
*(Guest & Pellegrino 1992)*

- [ ] Generate regular polygon hub for given n
- [ ] Compute major fold angles using β = π/n
- [ ] Generate minor folds (parallel, equally spaced)
- [ ] Produce full crease pattern in the plane
- [ ] Add unit tests:
  - Edge lengths
  - Angle relationships
  - Correct n-fold rotational symmetry

---

## Phase 3 — Thickness Accommodation  
*(Arya et al. 2021; Kreider & Arya 2024)*

- [ ] Implement spiral stowed geometry:
  - Valley and mountain vertex spirals
  - Layer spacing parameter d
- [ ] Implement per-ring isometry solving:
  - Equality of fold-line lengths between deployed and stowed states
  - Use `scipy.optimize` for root-finding + outer optimization
- [ ] Support:
  - Planar deployed shape (starshade case)
  - Conical deployed shape (for validation vs. Arya 2021)
- [ ] Add unit tests for:
  - Consistent fold-line lengths
  - No self-intersections in simple examples

---

## Phase 4 — Tessellation Extensions  
*(Jatusripitak & Arya 2024)*

- [ ] Implement joining conditions between neighboring flashers
- [ ] Explore regular & semi-regular tessellations
- [ ] Add lattice-based generation for:
  - Triangular
  - Square
  - Hexagonal tilings
- [ ] Add tests for join consistency and thickness accommodation

---

## Phase 5 — Starshade-Specific Enhancements

- [ ] Support design of starshade-influenced geometries:
  - Large n (e.g., 14, 24, 28)
  - Constraints for real hardware clearances
- [ ] Add export tools:
  - SVG crease pattern
  - DXF outline
  - JSON geometry state (for external software)
- [ ] Add numerical validation:
  - Fold angle distributions
  - Wrapping radius vs. thickness predictions

---

## Phase 6 — Documentation + Examples

- [ ] Example notebook: “Generate a 6-fold flasher pattern”
- [ ] Example notebook: “Thickness vs zero-thickness comparison”
- [ ] Example notebook: “Visualizing fold angles in 3D”
- [ ] Build full project documentation (MkDocs or Sphinx)

---

This roadmap will evolve as the project matures and as new geometric capabilities are introduced.
