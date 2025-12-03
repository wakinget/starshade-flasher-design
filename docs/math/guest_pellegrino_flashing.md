# Guest & Pellegrino (1992) — Zero-Thickness Flasher Geometry
Math Notes for Implementation

## 1. Citation and Link

S. D. Guest and S. Pellegrino (1992).  
“Inextensional Wrapping of Flat Membranes.”  
Proceedings of the First International Seminar on Structural Morphology.

URL: https://www.researchgate.net/publication/241730495_Inextensional_wrapping_of_flat_membranes

**Role in this project**

This paper provides the geometric foundation for the **zero-thickness flasher** pattern:
- Major (radial) fold lines emanating from a polygonal hub
- Distributed minor folds between major folds
- A purely *inextensional* (strain-free) transformation between deployed (flat) and stowed (wrapped) states
- Angular relationships near the hub allowing flat wrapping
- Symmetry and crease layout rules

These notes formalize the equations and constraints needed to generate a planar crease pattern suitable for extension into thickness-accommodating algorithms.

---

## 2. Scope Within This Project

We implement:
- Geometry of deployed (flat) flasher crease pattern
- Major fold orientations around hub
- Construction of minor folds between major folds
- Angular relationships ensuring inextensional behavior
- Hub polygon definition and alignment between major folds

We do **not** implement:
- Physical material modeling
- Numerical fitting of membrane curvature
- Experimental measurement/modeling sections

---

## 3. Coordinate Systems and Conventions

- We work in the **deployed (flat) configuration**, entirely in the *z = 0* plane.
- Coordinate system:
  - Origin at the **center of the hub**.
  - x-axis aligned with the first major fold.
  - y-axis rotated +90° counterclockwise from x.
- All angles are in **radians**.
- Positive rotations are **counterclockwise**.
- Length units are arbitrary (dimensionless OK) as long as consistent.

**Symmetry**  
A flasher has **N** identical “gores” around the hub. Each gore occupies an angle:

\[
\beta = \frac{2\pi}{N}.
\]

---

## 4. Notation

| Symbol | Description | Units | Notes |
|--------|-------------|-------|-------|
| N | Number of major folds / gores (hub degree) | – | Typically even; ≥ 4 |
| β | Angular width of a gore: 2π/N | radians | Constant |
| A | Hub radius (circumradius of central N-gon) | length | > 0 |
| p_k | k-th hub vertex | (x,y) | k = 0,…,N−1 |
| θ_k | Hub vertex angle = 2πk/N | radians | p_k = (A cos θ_k, A sin θ_k) |
| m_i | i-th vertex along a major fold in deployed state | (x,y) | radial line |
| v_i | i-th vertex along adjacent major fold | (x,y) | next radial line |
| L_i | Length of major fold segment i | length | User-specified or derived |
| n | Number of vertices per major fold (excluding hub) | – | ≥ 2 |
| s | Minor fold spacing index | – | Uniform between radial lines |

We will ultimately produce:
- Major fold polylines: {m_0 → m_1 → … → m_n}
- Minor fold polylines connecting m_i to v_i

---

## 5. Geometric Definitions

### Hub Polygon
The hub is a regular N-gon with radius A. Vertices:

\[
p_k = \big(A \cos(2\pi k/N),\; A \sin(2\pi k/N)\big)
\]

Major fold line **k** is the ray:

\[
\ell_k = \{ p_k + t\,u_k : t \ge 0 \},
\]
where  
\[
u_k = (\cos\theta_k, \sin\theta_k).
\]

### Major Folds (Radial Lines)
Let **n** be the number of points along each major fold, not counting the hub.

For gore 0 (between u_0 and u_1), we define:

\[
m_i = p_0 + L_i \, u_0,
\]
\[
v_i = p_1 + L_i \, u_1,
\]

where the L_i form a strictly increasing radial sequence such that:

\[
L_0 = 0,\quad L_n = \text{desired radius}.
\]

### Minor Folds (Connecting Folds)
Minor folds are straight segments connecting m_i to v_i:

\[
s_i(t) = (1-t) m_i + t\, v_i,\qquad t \in [0,1].
\]

In the zero-thickness formulation, these are straight lines.

---

## 6. Constraints and Equations

Guest & Pellegrino show that a flat sheet can be wrapped around a polygonal hub *if and only if* certain angular relationships are satisfied near the hub.

### 6.1 Inextensionality Constraint
Edges must maintain the same length in deployed and stowed states.  
In the *pure planar* model here, we only enforce:

\[
\| v_i - m_i \| \;\text{is the same across all gores}.
\]

At the hub:

\[
\| p_1 - p_0 \| = \| p_2 - p_1 \| = \cdots = \| p_{N-1} - p_{N-2} \| = \| p_0 - p_{N-1} \|
\]

since the hub is regular.

### 6.2 Angular Compatibility Condition
Let α be the angle between adjacent major folds at a given radius i.

Because major folds emanate radially from a regular N-gon:

\[
\alpha = \beta = \frac{2\pi}{N}.
\]

This is the key statement: **major folds must be evenly spaced**.

### 6.3 Straightness Constraint
All major folds must be straight radial lines.  
Formally, for gore k:

\[
m_i^{(k)} = p_k + L_i\,u_k.
\]

### 6.4 Minor Fold Parallelism
Minor folds between major folds at the same i are straight and parallel (in the infinitesimal sense) between gores.

In a single gore:

\[
\frac{v_i - m_i}{\| v_i - m_i \|} = \text{constant direction}
\]

implied by the symmetry of adjacent rays.

---

## 7. Algorithm Overview (High Level)

1. Select flasher parameters:  
   - N (number of gores)  
   - n (points per radial line)  
   - A (hub radius)  
   - L_i sequence (radial distances)

2. Construct the hub polygon p_k.

3. Construct major fold lines along directions u_k for all k.

4. For gore 0:
   - Compute m_i and v_i using radial distances L_i.

5. For gore k:
   - Rotate gore 0 vertices by angle 2πk/N.

6. Construct minor folds connecting m_i to v_i for each i.

7. Assemble the global crease pattern:  
   - All major folds  
   - All minor folds  
   - Hub polygon  

---

## 8. Algorithm Details / Pseudocode

**Inputs:**  
- N: int  
- n: int  
- A: float  
- L: array-like of length n+1 (monotonically increasing)  

**Outputs:**  
- vertices: list of all crease vertices (x,y)  
- edges: list of edges with type {major, minor, hub}  
- faces: can be inferred from triangulation if needed

**Pseudocode:**

```
Compute β = 2π / N
For k in 0..N-1:
    θ_k = k * β
    u_k = (cos θ_k, sin θ_k)
    p_k = (A cos θ_k, A sin θ_k)

For i in 0..n:
    m_i = p_0 + L_i * u_0
    v_i = p_1 + L_i * u_1
    Store minor fold edge (m_i, v_i)

Store major fold edges (p_0 → m_1 → ... → m_n) and (p_1 → v_1 → ... → v_n)

For each gore k:
    Rotation R_k = rotation by 2πk/N
    Rotate all vertices for gore 0 to get gore k
    Store rotated vertices and edges
```

---

## 9. Inputs and Outputs for Implementation

**Function Name (suggested):**

`generate_zero_thickness_flasher(N, n, A, L)`

**Inputs:**
- `N`: number of gores
- `n`: number of points per major fold
- `A`: hub radius
- `L`: radial distances (list or array length n+1)

**Outputs:**
- `vertices`: `(num_vertices, 2)` array
- `edges`: list of `Edge(type, i, j)` referencing vertex indices
- `faces`: optional; may leave for triangulation

---

## 10. Numerical Considerations

- L_i must be strictly increasing.
- For physical flasher designs, L_i often follows a nonlinear profile optimized for deployment mechanics; here we accept any monotonic input.
- Large N requires careful floating-point handling for rotational symmetry:
  - Use `cos`/`sin` of exact multiples of β.
- Tolerances:
  - Edge-length preservation within 1e–8 (for testing symmetry).

---

## 11. Mapping to Code in This Repository

- `patterns.py`:
  - `generate_zero_thickness_flasher(...)` (primary function)
  - `generate_hub_polygon(...)` (helper)
  - `generate_major_folds(...)` (helper)
  - `generate_minor_folds(...)`

- `geometry.py`:
  - Use Vertex and Edge dataclasses to represent crease patterns.

- `visualization.py`:
  - 2D planar plot showing major folds (blue) and minor folds (red).

---

## 12. Test Cases and Invariants

1. **Symmetry Test**
   - Vertices in gore k must be a rotation of vertices in gore 0 by 2πk/N.

2. **Hub Test**
   - Hub polygon edges all same length.

3. **Radial Linearity**
   - All m_i lie on a straight line from p_0.
   - All v_i lie on a straight line from p_1.

4. **Minor Fold Straightness**
   - m_i, v_i should satisfy:
     \[
     \text{angle}(m_{i+1} - m_i, v_{i+1} - v_i) = \beta.
     \]

5. **Edge-Length Consistency**
   - ∥m_i − m_{i−1}∥ = ∥v_i − v_{i−1}∥.

---

## 13. Open Questions / TODOs

- Decide on default L_i generation strategy (linear? exponential? custom?).  
- Incorporate optional curvature-based L_i distributions inspired by later papers.  
- Extend to thickness-accommodating models (handled in separate notes).