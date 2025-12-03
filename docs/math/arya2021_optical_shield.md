# Arya et al. (2021) — Thickness-Accommodating Spiral-Wrapped Flasher
Math Notes for Implementation

## 1. Citation and Link

Manan Arya, David Webb, Samuel C. Bradford, Louis Adams, Velibor Cormarkovic,  
Gary Wang, Mehran Mobrem, Kenzo Neff, Neal Beidleman, John D. Stienmier,  
Gregg Freebury, Kamron A. Medina, David Hepper, Dana E. Turse,  
George Antoun, and Cory Rupp (2021).  
“Origami-Inspired Optical Shield for a Starshade Inner Disk Testbed:  
Design, Fabrication, and Analysis.”  
AIAA Scitech 2021 Forum.

DOI: https://doi.org/10.2514/6.2021-0904

**Role in this project**

This paper introduces the **thickness-accommodating, spiral-wrapped flasher** used for the starshade inner-disk optical shield. The deployed configuration is planar; the stowed configuration is a compact spiral with separate mountain and valley vertex spirals of constant layer spacing. The key contribution is an algorithm to enforce **inextensionality between deployed and stowed states** while accounting for real material thickness.

---

## 2. Scope Within This Project

We implement:
- Spiral geometry for mountain and valley vertices in the **stowed configuration**
- Mapping between deployed (flat) and stowed (wrapped) states
- Per-ring solve that enforces:
  - (1) Equal fold-line lengths (isometry)
  - (2) Planar deployed geometry
  - (3) Prescribed stowed spiral positions
- Mountain/valley orientation conventions
- Rotational symmetry around the hub

We do **not** implement:
- Structural analysis (Abaqus, RAPID, ADAMS)
- Prototype measurements/validation
- Materials, buckling, tolerances

---

## 3. Coordinate Systems and Conventions

### Deployed State (Flat)
- Entire geometry lies in the **z = 0** plane.
- Coordinates: (x, y)
- Origin at the center of the hub.
- Major fold 0 lies along the +x direction.
- Counterclockwise rotation is positive.

### Stowed State (Wrapped)
- The sheet wraps around a cylindrical volume.
- Vertices spiral outward (increasing radius) with constant thickness spacing **d**.
- Coordinates: also represented as (x, y) in a plane after "cutting open" the cylindrical wrap.
  - This is equivalent to an **unwrapped representation** of the spiral.

### Shared Conventions
- Angles in **radians**.
- Rotational symmetry:
  \[
  \beta = \frac{2\pi}{N}.
  \]
- Gores (sectors) indexed **k = 0 … N−1**.

---

## 4. Notation

| Symbol | Description | Units | Notes |
|--------|-------------|-------|-------|
| N | Number of major folds / gores | – | Typical starshade: ~16–24 |
| β | Sector angle 2π/N | radians | |
| A | Hub radius | length | |
| n | Number of vertices per radial fold | – | |
| m_i | Mountain vertices (deployed) | (x,y) | Ring index i |
| v_i | Valley vertices (deployed) | (x,y) | Adjacent major fold |
| m’_i | Mountain vertices (stowed) | (x,y) | On spiral |
| v’_i | Valley vertices (stowed) | (x,y) | On next spiral |
| d | Axial layer spacing | length | Controls thickness |
| L(m_i, v_i) | Length of fold in deployed state | length | |
| L(m’_i, v’_i) | Length in stowed state | length | Must match deployed |
| ψ | Rotation parameter in ring solve | radians | Used in inner root solve |
| h_i | Vertical offset / height parameter | length | Outer loop variable |

All symbols are ring-indexed unless otherwise stated.

---

## 5. Geometric Definitions

### 5.1 Deployed State Geometry (Flat)
As in Guest & Pellegrino:
- Hub polygon defined by vertices p_k at angle 2πk/N.
- Major folds (radial lines) defined by u_k = (cos θ_k, sin θ_k).
- Deployed vertices:
  - m_i = p_0 + L_i u_0
  - v_i = p_1 + L_i u_1

Here, L_i are not fixed; instead, they arise from the **inverse mapping** from the stowed geometry through the length-matching solve.

### 5.2 Stowed Spiral Geometry

The stowed configuration forms **two interleaved spirals**:

1. **Mountain vertex spiral**
   - m’_i has increasing radial distance:
     \[
     r_{m’,i} = R_0 + 2(i-1)d
     \]
   - Angular position:
     \[
     θ_{m’,i} = θ_0 + f_i
     \]

2. **Valley vertex spiral**
   - v’_i offset from mountain spiral by one layer:
     \[
     r_{v’,i} = R_0 + (2i-1)d
     \]
   - Angular position:
     \[
     θ_{v’,i} = θ_{m’,i} + ψ_i
     \]
  
Here:
- `R_0` is the base radius of the wrap.
- `f_i` is an accumulated unfolding angle.
- `ψ_i` is the ring-specific twist between mountain and valley vertices.

Cartesian coordinates:
\[
m’_i = ( r_{m’,i} \cos θ_{m’,i},\; r_{m’,i} \sin θ_{m’,i} )
\]
\[
v’_i = ( r_{v’,i} \cos θ_{v’,i},\; r_{v’,i} \sin θ_{v’,i} )
\]

### 5.3 Sector Replication
Gore k is obtained by rotation:

\[
m’^{(k)}_i = R(2πk/N) \, m’_i
\]
\[
v’^{(k)}_i = R(2πk/N) \, v’_i
\]

---

## 6. Constraints and Equations

### 6.1 Inextensionality: Length Matching
For each ring i:

\[
\| m_i - v_i \| = \| m’_i - v’_i \|
\]

And for major fold segments:

\[
\| m_{i+1} - m_i \| = \| m’_{i+1} - m’_i \|
\]
\[
\| v_{i+1} - v_i \| = \| v’_{i+1} - v’_i \|
\]

These enforce that the deployed mesh and stowed mesh are **isometric**.

### 6.2 Planarity of Deployed Configuration
Deployed coordinates lie in z=0.  
No curvature is allowed.

### 6.3 Spiral Geometry Constraints
Stowed coordinates must exactly follow the spiral equations in Section 5.2.

### 6.4 Ring-by-Ring Consistency
For each ring i:
- m_i, v_i are solved together based on:
  - (1) stowed lengths
  - (2) sector geometry (angle β)
  - (3) rotational neighborhoods

Arya uses a **2-level nested solve**, described below.

---

## 7. Algorithm Overview (High Level)

For each radial ring i:

1. Start from known ring i vertices (m_i, v_i) and stowed ring i vertices (m’_i, v’_i).
2. Guess the “height” parameter h_{i+1}, which influences the deployed triangle geometry.
3. For a given h guess:
   - Solve for angle ψ_{i+1} (inner root solve) such that the length constraints between m_{i+1} and v_{i+1} are satisfied.
4. Evaluate the error between the deployed geometry and allowed planar configuration.
5. Optimize h_{i+1} using 1D scalar minimization.
6. Accept m_{i+1}, v_{i+1}.
7. Repeat for all rings.

After computing gore 0, replicate it to all N sectors by rotation.

---

## 8. Algorithm Details / Pseudocode

### Variables
- **Inputs**: N, n, A, d, R_0 (wrap radius), initial angles.
- **State**:
  - deployed: m_i, v_i  
  - stowed: m’_i, v’_i  
- **Unknown per ring**:
  - ψ_i (twist angle)
  - h_i (height or radial deployed parameter)

### Pseudocode

```
Compute β = 2π / N
Initialize deployed ring 0 using hub geometry
Compute stowed ring 0 spiral positions

For i in 0 .. n-1:

    # Outer loop variable: height h_{i+1}
    Define cost function C(h):

        # Inner solve for ψ
        Solve S(ψ, h) = 0   # Enforces length(m_i, v_i) = length(m’_i, v’_i)

        Compute m_{i+1}(h, ψ), v_{i+1}(h, ψ)
        Return planar deviation / constraint violation

    h_{i+1} = argmin_h C(h)
    Compute ψ_{i+1} via inner solve

    Update m_{i+1}, v_{i+1}

End For

Replicate gore 0 by rotations for all N gores.
```

Codex will turn this into numerical routines in `solvers.py`.

---

## 9. Inputs and Outputs for Implementation

### Suggested function name:
`generate_thickness_accommodating_flasher(...)`

### Inputs:
- `N`: number of gores  
- `n`: vertices per major fold  
- `A`: hub radius  
- `d`: layer spacing  
- `R0`: base spiral radius  
- Optional: initial angles (could default to 0)

### Outputs:
- `vertices_deployed`: array [(num_vertices, 2)]
- `vertices_stowed`: array [(num_vertices, 2)]
- `edges`: mountain/valley fold list  
- `faces`: (optional) for mesh connectivity  
- `metadata`: twist angles ψ_i, heights h_i

---

## 10. Numerical Considerations

- The outer loop minimize(h) is a **scalar optimization**:
  - Use `scipy.optimize.minimize_scalar` or `brentq` depending on formulation.
- The inner loop solve(ψ) is a **scalar root-finding** problem:
  - Use `scipy.optimize.root_scalar`.
- Good initialization is crucial:
  - ψ_i starts near β (sector angle)
  - h_{i+1} close to deployed radial increment
- Tolerances:
  - length-match error < 1e−8  
  - planar deviation < 1e−10

---

## 11. Mapping to Code in This Repository

- `patterns.py`:
  - `generate_thickness_accommodating_flasher`
  - `spiral_stowed_vertices(...)`
- `solvers.py`:
  - `solve_ring_step(...)`
  - `solve_twist_angle_psi(...)`
  - `optimize_height_h(...)`
- `geometry.py`:
  - Vertex and Edge classes (major, minor, mountain, valley)
- `visualization.py`:
  - Deployed vs stowed side-by-side 2D plots
  - Red = valley, Blue = mountain folds

---

## 12. Test Cases and Invariants

1. **Length Matching**
   - For each ring i:
     \[
     \|m_i - v_i\| = \|m’_i - v’_i\|
     \]
   - And similar for radial segments.

2. **Spiral Consistency**
   - Differences:
     \[
     r_{m’,i+1} - r_{m’,i} = 2d
     \]
     \[
     r_{v’,i+1} - r_{v’,i} = 2d
     \]

3. **Symmetry**
   - Rotating gore 0 vertices by βk yields gore k.

4. **Planarity**
   - All deployed vertices satisfy z=0.

5. **Monotonicity**
   - r_{m’,i} and r_{v’,i} must strictly increase.

---

## 13. Open Questions / TODOs

- Decide whether to expose ψ_i and h_i to users or treat as internal solver state.
- Connect this model cleanly with the more general corrugated formulation (Kreider & Arya 2024).
- Calibrate default R_0 and initial angle offsets to match starshade physical constraints.