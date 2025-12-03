# Jatusripitak & Arya (2024) — Regular and Semi-Regular Tessellations of Origami Flashers
Math Notes for Implementation

## 1. Citation and Link

Nachat Jatusripitak and Manan Arya (2024).  
“Regular and Semi-Regular Tessellations of Origami Flashers.”

ResearchGate:  
https://www.researchgate.net/publication/385418669_Regular_and_Semi-Regular_Tessellations_of_Origami_Flashers

**Role in this project**

This paper establishes the geometric rules for assembling **multiple flasher units** into:
- *regular tessellations* (all cells identical),  
- *semi-regular tessellations* (pattern includes multiple unit types),  
while preserving:
- equal edge lengths,
- consistent mountain/valley orientations,
- angular compatibility,
- and non-self-intersection constraints.

Unlike the Arya 2021 and Kreider & Arya algorithms (which solve geometry ring-by-ring), this paper focuses on **multi-cell join conditions**.

This math note is the master reference for implementing tessellation-aware flasher generation in future extensions of `patterns.py`.

---

## 2. Scope Within This Project

We implement:
- The join conditions that enable a flasher cell to meet adjacent cells without geometric conflict.
- Constraints for:
  - angular compatibility,
  - edge length matching,
  - fold-orientation consistency,
  - and rotational symmetry across tessellation vertices.
- Support for:
  - triangular,
  - square,
  - and hexagonal lattice patterns.
- Embedding flasher seeds into tilings by rotation and reflection.

We do **not** implement:
- Material thickness,
- Dynamic deployment behavior,
- Non-Euclidean tessellations.

---

## 3. Coordinate Systems and Conventions

Tessellations occur in the **deployed, flat configuration**, so:
- Geometry lies in **z = 0** plane.
- Each flasher unit has its own local hub with N sectors.
- Flashers are placed at lattice vertices or faces depending on tessellation type.

### Rotational Conventions
For a flasher cell with N sectors:
\[
\beta = \frac{2\pi}{N}
\]

### Tessellation Grid Conventions
- **Triangular tiling** → vertices valence = 6  
- **Square tiling** → valence = 4  
- **Hexagonal tiling** → valence = 3  

These valences must match the local angular budget around tessellation vertices.

---

## 4. Notation

| Symbol | Description | Units | Notes |
|--------|-------------|-------|-------|
| N | Number of flasher sectors | – | N ≥ 4 typically |
| β | Sector angle = 2π/N | rad | |
| α_j | Angular overlap at joint j | rad | must satisfy compatibility |
| L_i | Lengths of fold lines at radius index i | length | must match across neighbors |
| u_k | Radial unit vector of sector k | – | |
| p | Position of flasher hub in tessellation | (x,y) | |
| R | Rotation matrix | – | orientation of flasher cell |
| C | Set of cell centers | – | lattice positions |
| J | Join constraints | – | defined in Section 6 |

---

## 5. Geometric Definitions

### 5.1 Flasher Cell Geometry
Each flasher unit is defined by major and minor fold sets:
- Major folds: radial lines with angles θ_k = kβ.
- Minor folds: connecting lines between major folds.

The unit is rotationally symmetric.

### 5.2 Tessellation Lattice
Three classical lattices:

1. **Triangular:**  
   Basis vectors:  
   \[
   b_1 = (1, 0),\quad b_2 = \left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)
   \]

2. **Square:**  
   \[
   b_1 = (1, 0),\quad b_2 = (0, 1)
   \]

3. **Hexagonal:**  
   \[
   b_1 = (1, 0),\quad b_2 = \left(\frac{1}{2}, \frac{\sqrt{3}}{2}\right)
   \]

Placements obey:
\[
p = x b_1 + y b_2,\quad x,y \in \mathbb{Z}
\]

### 5.3 Flasher Placement
Each flasher is placed at a lattice point:
\[
\text{Cell}(p) = \{ R_p \cdot \text{Flasher Template} + p \}
\]

Orientation R_p must satisfy join constraints.

---

## 6. Constraints and Equations

This paper's core contribution is the definition of **join constraints J** for assembling flashers.

### 6.1 Angular Compatibility
At any tessellation vertex where multiple flashers meet, the sum of their sector angles must equal 2π:

\[
\sum_{\text{cells meeting at vertex}} \beta_{\text{cell}} = 2\pi
\]

For regular tessellations:
- Triangular tiling: 6 flashers → requires β = π/3 → N = 6  
- Square tiling: 4 flashers → β = π/2 → N = 4  
- Hexagonal tiling: 3 flashers → β = 2π/3 → N = 3  

General statement:
\[
N = \frac{2\pi}{\text{valence angle}}
\]

### 6.2 Edge-Length Matching
Radial lengths at matched join points must satisfy:

\[
L_i^{(cell\ A)} = L_i^{(cell\ B)}
\]

When connecting cells A and B along sector boundaries.

### 6.3 Sector Orientation Compatibility
If cell A’s sector boundary labeled k meets cell B’s sector boundary labeled l:

\[
R_A u_k = \pm R_B u_l
\]

The sign indicates whether valley ↔ mountain orientation flips (depending on tessellation type).

### 6.4 Fold-Type Compatibility
Fold assignments (mountain/valley) must satisfy:

\[
\text{fold\_type}_A(k) = 
\begin{cases}
\text{fold\_type}_B(l), & \text{if no reflection}\\[6pt]
\text{opposite}(\text{fold\_type}_B(l)), & \text{if reflection applied}
\end{cases}
\]

This supports semi-regular tessellations where reflections occur.

### 6.5 Non-Intersection Constraint
Cells must not overlap. Formally:

\[
\text{Cell}(p_i) \cap \text{Cell}(p_j) = \emptyset,\quad \text{for } i \neq j
\]

This is typically tested numerically by bounding boxes or polygon overlap tests.

---

## 7. Algorithm Overview (High Level)

1. Choose tessellation type (triangular, square, hexagonal).
2. Determine required N for each flasher cell.
3. Construct base flasher for N using zero-thickness (or thickness-accommodating) method.
4. Generate lattice positions p = x b_1 + y b_2.
5. For each lattice point:
   - Assign orientation R_p to satisfy:
     - Sector alignment
     - Fold assignment consistency
6. Assemble global crease pattern:
   - Duplicate and transform flasher template
   - Stitch boundaries together
7. Validate:
   - Angular compatibility
   - Edge-length matching
   - Fold-type compatibility
   - Non-intersection

---

## 8. Algorithm Details / Pseudocode

### Pseudocode for Tessellation Assembly

```
Select tessellation type T
Compute required sector count N for T
Compute β = 2π/N

# Step 1: Generate base flasher
base = generate_zero_thickness_flasher(N, ...)

# Step 2: Build lattice
lattice = compute_lattice_points(T, size=(M,N))

# Step 3: For each cell
for p in lattice:

    # Determine orientation R_p
    R_p = compute_orientation(T, p)

    # Transform flasher
    cell_vertices = R_p @ base.vertices + p
    cell_edges    = R_p @ base.edges    + p

    # Store
    add to global pattern

# Step 4: Validate joins
validate_edge_lengths(global_pattern)
validate_fold_assignments(global_pattern)
validate_non_intersection(global_pattern)
```

---

## 9. Inputs and Outputs for Implementation

### Suggested function:
`assemble_flasher_tessellation(tessellation_type, N_cells, flasher_params)`

### Inputs:
- `tessellation_type`: "triangular" | "square" | "hexagonal"
- `N_cells`: number of cells in each direction
- `flasher_params`: parameters passed to flasher generator

### Outputs:
- `vertices_global`: concatenated vertices of all flashers
- `edges_global`: edges with mountain/valley fold labels
- `cell_metadata`: positions, orientations, connectivity

---

## 10. Numerical Considerations

- Transformations R_p must be exact to avoid drift in edge matching.
- Validation steps should allow tiny tolerance (e.g. 1e−8).
- Non-intersection tests can be expensive for large tessellations; consider bounding-box prechecks.

---

## 11. Mapping to Code in This Repository

### `patterns.py`
- `assemble_flasher_tessellation(...)`
- `compute_lattice_vectors(...)`
- `compute_cell_orientation(...)`

### `geometry.py`
- Must support batching/superposition of multiple flasher units.

### `solvers.py`
- Not used directly for tessellation (unless using thickness-accommodating flashers for each cell).

### `visualization.py`
- Global 2D plot of tessellations.
- Optional color-coding by cell or fold type.

---

## 12. Test Cases and Invariants

### Angular Compatibility Test
Around each lattice vertex:
\[
\sum \beta_i = 2\pi.
\]

### Edge-Matching Test
Joined flasher boundaries must satisfy:
\[
\| p_i^{(A)} - p_j^{(A)} \| = \| p_i^{(B)} - p_j^{(B)} \|
\]

### Fold-Type Consistency
Mountain/valley labeling must be consistent across joins.

### Non-Intersection
Edges and faces of different cells may not overlap.

---

## 13. Open Questions / TODOs

- Determine the best interface for specifying mixed N in semi-regular patterns.
- Consider allowing mirrors/reflections for more complex tessellations.
- Add support for thickness-accommodating flasher tessellations (requires careful stowed-state overlap analysis).
- Integrate tessellation constraints into solver-based design tools.