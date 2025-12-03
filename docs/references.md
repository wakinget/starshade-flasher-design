# References for Starshade Flasher Design

This document lists the main technical references that inform the geometry, algorithms, and numerical methods used in the **starshade-flasher-design** project.  
Each entry includes a short description of why it is relevant to this codebase.

---

## 1. Jatusripitak & Arya (2024)

**Citation**

Nachat Jatusripitak and Manan Arya (2024).  
“Regular and Semi-Regular Tessellations of Origami Flashers.”

URL: https://www.researchgate.net/publication/385418669_Regular_and_Semi-Regular_Tessellations_of_Origami_Flashers

**What this paper is about**

- Introduces **regular** and **semi-regular** tessellations built from origami flasher units.  
- Discusses both **zero-thickness** and **thickness-accommodating** variants of flashers.  
- Analyzes how individual flashers can be joined together consistently in tilings (e.g., triangular, square, hexagonal).  

**How we use it**

- Provides geometric context for extending single-flasher algorithms to **multi-cell tessellations**.  
- Informs future work in this repository on joining conditions and lattice-based layouts.  

---

## 2. Arya et al. (2021)

**Citation**

Manan Arya, David Webb, Samuel C. Bradford, Louis Adams, Velibor Cormarkovic, Gary Wang, Mehran Mobrem,  
Kenzo Neff, Neal Beidleman, John D. Stienmier, Gregg Freebury, Kamron A. Medina, David Hepper,  
Dana E. Turse, George Antoun, Cory Rupp, and Laura Hoffman (2021).  
“Origami-Inspired Optical Shield for a Starshade Inner Disk Testbed: Design, Fabrication, and Analysis.”  
AIAA Scitech 2021 Forum.

DOI: https://doi.org/10.2514/6.2021-0904  
Video Presentation: https://doi.org/10.2514/6.2021-0904.vid

**What this paper is about**

- Describes a **10 m-diameter origami-folded optical shield** used in a starshade inner disk testbed.  
- Presents a **spiral-wrapped, thickness-accommodating** fold pattern that packs into a 2.3 m diameter volume.  
- Explains a **custom algorithm** based on generative design approaches to produce the fold pattern.  
- Includes structural modeling of the shield using tools such as Abaqus, RAPID, and ADAMS.

**How we use it**

- Provides the main reference for the **spiral-wrapped, thickness-accommodating** flasher algorithm.  
- Defines the concept of:
  - Mountain and valley vertex spirals  
  - Layer spacing `d` between wrapped layers  
  - Per-ring **isometry constraints** between deployed and stowed states  
- Guides the design of solver routines in `solvers.py` and the geometric conventions in `patterns.py` and `visualization.py`.

---

## 3. Guest & Pellegrino (1992)

**Citation**

S. D. Guest and Sergio Pellegrino (1992).  
“Inextensional Wrapping of Flat Membranes.”  
Proceedings of the First International Seminar on Structural Morphology.

URL: https://www.researchgate.net/publication/241730495_Inextensional_wrapping_of_flat_membranes

**What this paper is about**

- Studies how a **flat, thin membrane** can be wrapped around a central hub **without stretching** (inextensional behavior).  
- Derives the geometry of a “flasher”-type fold pattern starting from a **polygonal hub** (regular or irregular).  
- Shows how **major folds** (originating at hub vertices) and **minor folds** must be arranged so that:
  - Folds remain straight,
  - The membrane can wrap around the hub,
  - The hub region stays flat.  

**How we use it**

- Forms the foundation for **zero-thickness flasher** patterns in this project.  
- Provides analytical relationships for:
  - Angles between fold lines near the hub,  
  - Placement of major and minor folds.  
- Underpins the initial planar crease pattern generation implemented in `patterns.py`.

---

## 4. Kreider & Arya (2024)

**Citation**

Matthew Kreider and Manan Arya (2024).  
“Origami-Wrapped Structures with Corrugated Unfolded Forms.”  
AIAA Journal, Vol. 62, No. 5, pp. 1789–1801.

DOI: https://doi.org/10.2514/1.J063441

**What this paper is about**

- Introduces a class of **origami-wrapped thin-shell structures** that are **corrugated when deployed** and cannot become flat by design.  
- Uses origami wrapping methods to achieve compact stowage while relying on the persistent corrugations to provide stiffness in the deployed state.  
- Describes a **geometric design method** that guarantees the structure is unstrained both when compactly wrapped and when fully deployed.  
- Presents test articles, stowage and stiffness experiments, and a structural finite element modeling procedure.

**How we use it**

- Provides a **modern, detailed formulation** of the ring-by-ring folding algorithm, including:
  - Inner root-solving over a rotation variable,
  - Outer optimization over folded vertex heights.  
- Offers a clear template for implementing robust numerical solvers in `solvers.py`.  
- Serves as a bridge between the purely planar flasher patterns (Guest & Pellegrino 1992) and more complex 3D deployed geometries.

---

## Summary

These four references together provide:

- The **classical zero-thickness flasher** geometry (Guest & Pellegrino 1992).  
- A **thickness-accommodating, spiral-wrapped** algorithm tailored to starshade inner disks (Arya et al. 2021).  
- A **generalized solver framework** for corrugated, non-flat deployed surfaces (Kreider & Arya 2024).  
- A broader framework for **tessellations of flasher units** and their joining constraints (Jatusripitak & Arya 2024).

This project’s code is intended to mirror and extend these ideas in a reusable Python library.
