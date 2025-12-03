# Kreider & Arya (2024) — Origami-Wrapped Structures with Corrugated Unfolded Forms
Math Notes for Implementation

## 1. Citation and Link

Matthew Kreider and Manan Arya (2024).  
“Origami-Wrapped Structures with Corrugated Unfolded Forms.”  
AIAA Journal, Vol. 62, No. 5, pp. 1789–1801.

DOI: https://doi.org/10.2514/1.J063441

**Role in this project**

This paper generalizes the spiral-wrapped flasher algorithm (Arya 2021) to **corrugated unfolded geometries** — i.e., surfaces that are *developable but not planar*. The key contribution is a rigorous **ring-by-ring isometry solver** that:

1. Accepts *any* developable unfolded surface (e.g., a prescribed corrugation).
2. Computes a wrapped/stowed configuration via a **spiral layer model** like the 2021 paper.
3. Provides a clean **two-level nested numerical algorithm**:
   - Inner: solve for rotation parameter ψ  
   - Outer: optimize vertical parameter h (or equivalent corrugation coordinate)

This paper is the most implementation-friendly source for the general solver structure.  
The core algorithm here will directly power `solvers.py`.

---

## 2. Scope Within This Project

We implement:
- General developable-surface model for deployed configuration.
- Mountain/valley stowed spirals with layer spacing.
- Per-ring nested solve:
  - Unknown twist ψ  
  - Unknown “height” or generalized corrugation coordinate h
- Mapping from deployed ring i → ring i+1 using:
  - Geometric constraints  
  - Length preservation  
  - Surface constraints  
- Replication to N symmetric sectors.

We do **not** implement:
- Material stiffness tuning
- Experimental validations
- Finite element modeling
- Non-developable surfaces

---

## 3. Coordinate Systems and Conventions

### 3.1 Deployed Surface (Corrugated)
- A **developable surface S** defined by a parametric function:

  \[
  S(u,v) = (x(u,v), y(u,v), z(u,v)),
  \]

  where:
  - u parameterizes radial direction (rings)
  - v parameterizes circumferential direction (between mountain/valley folds)

- Developable ⇒ zero Gaussian curvature ⇒  
  \[
  \det\left(\frac{\partial^2 S}{\partial u \partial v}\right) = 0.
  \]

### 3.2 Stowed Geometry
- Stowed spirals are as in Arya 2021:
  - Mountain radii: \( r_{m’,i} = R_0 + 2(i-1)d \)
  - Valley radii:   \( r_{v’,i} = R_0 + (2i-1)d \)
  - Angular coordinates increment by accumulated twist.

### 3.3 Symmetry
- System has N identical sectors:
  \[
  \beta = 2\pi / N.
  \]
- Sector k obtained via rotation by βk.

---

## 4. Notation

| Symbol | Description | Units | Notes |
|--------|-------------|-------|-------|
| N | Number of gores | – | |
| β | Sector angle 2π/N | rad | |
| S(u,v) | Deployed surface embedding | length³ | Corrugated surface |
| u_i | Radial coordinate of ring i | – | i = 0..n |
| v_m, v_v | Circumferential parameters for mountain and valley | – | |
| m_i, v_i | Deployed mountain/valley vertices on S | 3D | |
| m’_i, v’_i | Stowed spiral positions | 2D | Unwrapped cylinder |
| L(m_i,v_i) | Edge length in deployed | length | |
| ψ_i | Twist angle between mountain and valley at ring i | rad | root-solve variable |
| h_i | Generalized “height” parameter for corrugation at ring i | length or dimensionless | outer-loop variable |
| d | Layer spacing | length | controls thickness |
| n | Number of radial rings | – | |
| R_0 | Inner stow radius | length | |

---

## 5. Geometric Definitions

### 5.1 Deployed Corrugated Surface S
The deployed geometry is a patch of a developable surface S.

For each ring i, the deployed mountain and valley vertices lie at:

\[
m_i = S(u_i, v_m)
\]
\[
v_i = S(u_i, v_v)
\]

Here:
- u_i controls radial position,
- v_m and v_v are fixed offsets within each sector.

### 5.2 Stowed Spirals
As in Arya (2021):

- Mountain spiral:
  \[
  r_{m’,i} = R_0 + 2(i-1)d
  \]
  \[
  θ_{m’,i} = θ_0 + f_i
  \]

- Valley spiral:
  \[
  r_{v’,i} = R_0 + (2i-1)d
  \]
  \[
  θ_{v’,i} = θ_{m’,i} + ψ_i
  \]

Cartesian coordinates:
\[
m’_i = (r_{m’,i}\cos θ_{m’,i},\; r_{m’,i}\sin θ_{m’,i})
\]
\[
v’_i = (r_{v’,i}\cos θ_{v’,i},\; r_{v’,i}\sin θ_{v’,i})
\]

### 5.3 Sector Replication
Gore k obtained by rotation by βk.

---

## 6. Constraints and Equations

We require **exact isometry** between deployed surface S and stowed spirals.

### 6.1 Length Constraints (Major and Minor Folds)

**Mountain-major segment:**
\[
\| m_{i+1} - m_i \| = \| m’_{i+1} - m’_i \|
\]

**Valley-major segment:**
\[
\| v_{i+1} - v_i \| = \| v’_{i+1} - v’_i \|
\]

**Minor fold between mountain & valley:**
\[
\| m_i - v_i \| = \| m’_i - v’_i \|
\]

These hold for each ring i.

### 6.2 Surface Constraint
Deployed vertices must lie on S:

\[
m_i = S(u_i, v_m)
\]
\[
v_i = S(u_i, v_v)
\]

### 6.3 Twist Constraint (ψ inner solve)
ψ controls the relative angular offset between mountain and valley stowed vertices.  
We enforce:

\[
\| m_i - v_i \| - \| m’_i(ψ) - v’_i(ψ) \| = 0
\]

This equation defines the **inner root solve**.

### 6.4 Height / Corrugation Parameter (h outer solve)
h_i determines the deployed ring i geometry by setting u_{i+1} or another corrugation coordinate.

The outer scalar optimization enforces:
- Planarity of ring triangles (constraining S geometry)
- Minimization of constraint violation:
  \[
  C(h) = \left(\| m_{i+1}(h) - m_i \| - \| m’_{i+1} - m’_i \|\right)^2
  + \left(\| v_{i+1}(h) - v_i \| - \| v’_{i+1} - v’_i \|\right)^2
  + \text{additional geometric penalties}
  \]

---

## 7. Algorithm Overview (High Level)

**For each ring i:**

1. Compute stowed (spiral) geometry (m’_i, v’_i).
2. Set initial guess for the corrugation parameter h_{i+1}.
3. Perform **outer optimization** over h:
   - For each h:
     1. Solve for twist ψ (inner root solve).
     2. Compute deployed vertices m_{i+1}, v_{i+1} by solving:
        \[
        m_{i+1} = S(u_{i+1}(h), v_m)
        \]
        \[
        v_{i+1} = S(u_{i+1}(h), v_v)
        \]
     3. Evaluate cost C(h).
4. Optimal h gives deployed ring (i+1).
5. Repeat until all rings are computed.

After generating gore 0, replicate for all N sectors.

---

## 8. Algorithm Details / Pseudocode

### Definitions
Let `surface(u, v)` return S(u,v).  
Let `spiral_m(i)` return m’_i.  
Let `spiral_v(i)` return v’_i.

### Pseudocode

```
Compute β = 2π/N
Initialize ring 0 deployed: m_0, v_0 on S(u_0, ·)
Initialize ring 0 stowed: m’_0, v’_0 on spiral

For i in 0..n-1:

    Define outer cost function C(h):

        # Compute deployed coordinates for given h:
        u_next = compute_u_from_h(h, i)
        m_next = surface(u_next, v_m)
        v_next = surface(u_next, v_v)

        # Inner solve for ψ:
        Solve: G(ψ) = |m_next - v_next| - |m’_{i+1}(ψ) - v’_{i+1}(ψ)| = 0

        Compute m’_{i+1}(ψ), v’_{i+1}(ψ)

        # Cost: sum of squared length errors
        C(h) = (|m_next - m_i| - |m’_{i+1} - m’_i|)^2
             + (|v_next - v_i| - |v’_{i+1} - v’_i|)^2
             + (|m_next - v_next| - |m’_{i+1} - v’_{i+1}|)^2

        return C(h)

    # Outer optimization:
    h_{i+1} = argmin_h C(h)

    # Finalization step:
    Compute ψ_{i+1}
    Compute final m_{i+1}, v_{i+1}

End For

# Replicate gore 0 to all sectors by rotation
For k in 1..N-1:
    Rotate all vertices of gore 0 by βk
```

---

## 9. Inputs and Outputs for Implementation

### Function Name
`generate_corrugated_flasher(...)`

### Inputs
- `N`: number of gores  
- `n`: number of rings  
- `d`: layer spacing  
- `surface`: a callable S(u,v)  
- `u_values`: discretization of u (optional)  
- `v_m, v_v`: circumferential parameters  
- `R_0`: initial stow radius  
- Optional initial guesses: ψ_0, h_0.

### Outputs
- `vertices_deployed`: array of deployed vertices on S  
- `vertices_stowed`: array of stowed spiral positions  
- `edges`: major/minor fold metadata  
- `metadata`: {u_i}, {ψ_i}, {h_i}

---

## 10. Numerical Considerations

- Outer optimization must be robust:
  - `minimize_scalar` on bounded interval recommended.
- Inner solve must be stable:
  - Use `root_scalar` with bracketing if possible.
- Corrugated surfaces have stronger curvature; good initial guesses for u_{i+1}(h) help stabilizing.
- Spiral angle increments must remain monotonic.

---

## 11. Mapping to Code in This Repository

### `patterns.py`
- `generate_corrugated_flasher(...)`
- `compute_stowed_spiral_vertices(...)`

### `solvers.py`
- `solve_ring_step_corrugated(...)`
- `inner_solve_twist_angle_psi(...)`
- `outer_optimize_height_h(...)`
- `surface_embedding_wrapper(...)`

### `geometry.py`
- Vertex/Edge dataclasses must support 3D.

### `visualization.py`
- 3D deployed visualization using surface S.
- 2D stowed spiral visualization.

---

## 12. Test Cases and Invariants

1. **Surface inclusion**  
   For all m_i, v_i:  
   \[
   m_i = S(u_i, v_m),\quad v_i = S(u_i, v_v)
   \]

2. **Length matching**  
   As in Arya 2021, but now in 3D.

3. **Monotonicity of u_i**  
   u_{i+1} > u_i for all i.

4. **Spiral consistency**  
   r_{m’,i+1} - r_{m’,i} = 2d  
   r_{v’,i+1} - r_{v’,i} = 2d

5. **Isometry**  
   Deployed and stowed lengths match within tolerance.

---

## 13. Open Questions / TODOs

- Decide whether to support user-specified developable surfaces (e.g., conical, cylindrical, custom).
- Establish safe bounds for outer optimization variable h.
- Determine appropriate discretization strategies for surface parametrization u.
- Provide optional autogeneration of surface S for standard corrugated geometries.