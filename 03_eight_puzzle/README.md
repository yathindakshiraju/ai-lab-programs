# 8-Puzzle Problem

## Problem
Classic **3×3** sliding puzzle (8 tiles + blank). Not an 8×8 board.

Goal:
```
1 2 3
4 5 6
7 8 _
```

## Algorithms
1. **A\*** with Manhattan-distance heuristic (primary — prints every step)
2. **BFS** for comparison (same start; summary metrics)

Also prints path cost, nodes expanded, and a side-by-side comparison.

## How to run
```powershell
python 03_eight_puzzle/eight_puzzle.py
```

## What to screenshot
- Header `=== 8-Puzzle Problem Demo (A* + BFS) ===`
- Initial and goal boards
- A* step-by-step boards with move names
- Comparison table (path cost + nodes expanded for A* vs BFS)
