# D&D 5e Character Sheet & Stat Manager (PyQt5)

A lightweight, self-contained desktop application built with Python and **PyQt5** designed for tabletop role-playing game (TTRPG) players and Dungeon Masters to manage Dungeons & Dragons 5e character sheets, track real-time combat stats, and simulate dice rolls.

---

## Key Features

- **Full Character CRUD & Persistent State:** Create, inspect, update, and delete multiple character sheets seamlessly from a synchronized sidebar list.
- **Robust JSON Data Storage:** Automatically manages local persistence via `personajes.json` with UTF-8 encoding and defensive exception handling to prevent file corruption.
- **D&D 5e Core Mechanics & Dynamic Modifiers:** Computes standard ability modifiers on the fly using the official mathematical rule `(score - 10) // 2`.
- **Custom Interactive Attribute Controls:** Custom button handlers for the four core ability scores (Strength, Dexterity, Constitution, Wisdom) supporting left-click (+1) and right-click (-1) inputs bounded strictly between 1 and 20.
- **Combat Hit Points (HP) Tracker:** Real-time damage and healing controls guarded against edge cases (HP cannot drop below 0 or exceed the maximum pool).
- **Integrated Dice Roller:** Built-in D6 and D20 roll simulator that automatically integrates the active character's Strength modifier with a dedicated, read-only audit log.
- **Zero External Assets:** Built as a clean, single-script architecture with no external asset dependencies (images or audio), ensuring frictionless deployment.

---

## Technologies & Dependencies

- **Language:** Python 3.x
- **GUI Framework:** [PyQt5](https://pypi.org/project/PyQt5/)
- **Built-in Modules:** `sys`, `json`, `random`

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jonathaniha/gestor-dnd-pyqt5.git](https://github.com/jonathaniha/gestor-dnd-pyqt5.git)
   cd gestor-dnd-pyqt5
   ```
   > **Note:** Ensure the clone URL matches your actual repository URL on GitHub.

2. **Create and activate a virtual environment (recommended):**
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install PyQt5
   ```

---

## Usage

Run the main application script:
```bash
python gestor_dnd.py
```
> **Note:** If your script has a different filename like `GestorD&D.py`, adjust the command accordingly.

Upon launch, the application will automatically read or initialize `personajes.json` in the working directory.

---

## Project Architecture

```text
├── gestor_dnd.py        # Core application: UI layout, event handlers, and game logic
├── personajes.json      # Persistent local database (auto-generated)
├── .gitignore           # Python and virtual environment exclusions
└── README.md            # Technical documentation
```

---

## Author

Developed by **Jonathán Herrera Arellano** — focused on robust Python architectures, desktop GUI tooling, and software quality assurance.