# Starshade Flasher Design

Algorithms and visualization tools for generating origami “flasher” fold patterns for starshade-like deployable structures.

This project implements the geometric and numerical methods described in:

- **Jatusripitak & Arya (2024)** – Regular and semi-regular tessellations of origami flashers
- **Arya et al. (2021)** – Origami-inspired optical shield for a starshade inner disk
- **Guest & Pellegrino (1992)** – Inextensional wrapping of flat membranes

The goal is to generate customizable flasher-type fold patterns—from classical zero-thickness patterns to fully thickness-accommodating spiral wraps—and to visualize both deployed and stowed configurations with annotated mountain (blue) and valley (red) folds.

---

## ✨ Features (Current & Planned)

- Zero-thickness flasher fold generation (after Guest & Pellegrino 1992)
- Thickness-accommodating spiral-wrapped flasher generation (after Arya 2021, Kreider & Arya 2024)
- Support for arbitrary n-fold rotational symmetry
- Geometry primitives for vertices, edges, faces
- Numerical solvers enforcing isometry between deployed and stowed configurations
- 2D + 3D visualization tools (matplotlib)
- Support for future starshade-specific constraints

---

## 📦 Installation

This project targets **Python 3.11**.

    git clone https://github.com/<your-user>/starshade-flasher-design.git
    cd starshade-flasher-design
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -e .

---

## 🧭 Project Structure

    starshade-flasher-design/
    │
    ├── README.md
    ├── AGENTS.md
    ├── docs/
    │   ├── ROADMAP.md
    │   └── references.md
    │
    ├── src/
    │   └── starshade_flasher/
    │       ├── __init__.py
    │       ├── geometry.py
    │       ├── patterns.py
    │       ├── solvers.py
    │       ├── visualization.py
    │       ├── references.py
    │
    └── tests/
        └── test_basic.py

---

## 🚀 Development Setup

Open in PyCharm:

1. Select “Get from Version Control”
2. Paste the GitHub repo URL
3. Allow PyCharm to create a Python 3.11 virtual environment
4. Install dependencies:

       pip install -e .

---

## 🤝 Contributing

Use pull requests via GitHub or Codex. Tests use `pytest`.

---

## 📄 License

MIT License.