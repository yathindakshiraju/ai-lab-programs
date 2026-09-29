# AI Lab Programs

Coursework programs for AI lab submission (BMSCE).

**Student:** yathindakshiraju.cs24@bmsce.ac.in

## Programs

| # | Topic | Folder | Algorithm |
|---|--------|--------|-----------|
| 1 | Vacuum Cleaner Agent | `01_vacuum_cleaner/` | Simple reflex agent (two-room world) |
| 2 | Tic-Tac-Toe | `02_tic_tac_toe/` | Minimax (AI vs AI demo) |
| 3 | 8-Puzzle | `03_eight_puzzle/` | A* (Manhattan) + BFS comparison |

All scripts use **Python 3 standard library only** (see empty/minimal `requirements.txt`).

## Requirements

- Python 3.8+ (3.10+ recommended)
- Windows PowerShell or any terminal

No `pip install` needed for the default demos.

## How to run

From this repository root:

```powershell
python 01_vacuum_cleaner/vacuum_cleaner_agent.py
python 02_tic_tac_toe/tic_tac_toe.py
python 03_eight_puzzle/eight_puzzle.py
```

Optional interactive modes (not needed for screenshots):

```powershell
python 01_vacuum_cleaner/vacuum_cleaner_agent.py --interactive
python 02_tic_tac_toe/tic_tac_toe.py --interactive
```

## What to screenshot for lab submission

1. **Vacuum cleaner** — environment grid each step, percepts, actions, performance score / summary.
2. **Tic-tac-toe** — ASCII board each turn and final DRAW/winner line from the AI vs AI demo.
3. **8-puzzle** — initial + goal boards, A* step boards, and the A* vs BFS comparison table.

Each program prints a clear header such as `=== Vacuum Cleaner Agent Demo ===`.

## Project layout

```
ai-lab-programs/
  README.md
  requirements.txt
  01_vacuum_cleaner/
    vacuum_cleaner_agent.py
    README.md
  02_tic_tac_toe/
    tic_tac_toe.py
    README.md
  03_eight_puzzle/
    eight_puzzle.py
    README.md
```
