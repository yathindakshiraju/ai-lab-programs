#!/usr/bin/env python3
"""
8-Puzzle Problem (A* and BFS)
=============================
Classic 3x3 sliding puzzle with 8 numbered tiles and one blank.

Goal state:
  1 2 3
  4 5 6
  7 8 _

Search algorithms demonstrated:
  1. A* with Manhattan distance heuristic (primary)
  2. BFS (uninformed) for comparison on the same start state

Default demo uses a solvable start state and requires no input.
"""

from __future__ import annotations

import heapq
import sys
from collections import deque
from typing import Dict, Iterable, List, Optional, Tuple

# State is a flat 9-tuple; 0 represents the blank.
State = Tuple[int, ...]
GOAL: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Neighbor offsets for blank row/col on a 3x3 grid
MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


def print_state(state: State, label: str = "") -> None:
    """Pretty-print a 3x3 board for screenshots."""
    if label:
        print(f"  {label}")
    print("  +---+---+---+")
    for r in range(3):
        row = state[r * 3 : (r + 1) * 3]
        cells = " | ".join("_" if n == 0 else str(n) for n in row)
        print(f"  | {cells} |")
        print("  +---+---+---+")


def manhattan(state: State) -> int:
    """Sum of Manhattan distances of each tile from its goal position."""
    dist = 0
    for idx, tile in enumerate(state):
        if tile == 0:
            continue
        goal_idx = tile - 1  # tile k belongs at index k-1
        r1, c1 = divmod(idx, 3)
        r2, c2 = divmod(goal_idx, 3)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist


def blank_index(state: State) -> int:
    return state.index(0)


def neighbors(state: State) -> Iterable[Tuple[str, State]]:
    """Generate (move_name, new_state) for legal blank slides."""
    z = blank_index(state)
    r, c = divmod(z, 3)
    for name, (dr, dc) in MOVES.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nz = nr * 3 + nc
            lst = list(state)
            lst[z], lst[nz] = lst[nz], lst[z]
            yield name, tuple(lst)


def is_solvable(state: State) -> bool:
    """
    An 8-puzzle is solvable iff the number of inversions is even
    (for the blank on a flat board / odd-width grid).
    """
    tiles = [t for t in state if t != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0


def reconstruct_path(
    came_from: Dict[State, Tuple[Optional[State], Optional[str]]],
    goal: State,
) -> List[Tuple[Optional[str], State]]:
    path: List[Tuple[Optional[str], State]] = []
    cur: Optional[State] = goal
    while cur is not None:
        prev, move = came_from[cur]
        path.append((move, cur))
        cur = prev
    path.reverse()
    return path


def astar(start: State, goal: State = GOAL) -> Tuple[List[Tuple[Optional[str], State]], int, int]:
    """
    A* search with f(n) = g(n) + h(n), h = Manhattan distance.
    Returns (path, nodes_expanded, path_cost).
    """
    open_heap: List[Tuple[int, int, State]] = []
    counter = 0
    heapq.heappush(open_heap, (manhattan(start), counter, start))

    came_from: Dict[State, Tuple[Optional[State], Optional[str]]] = {
        start: (None, None)
    }
    g_score: Dict[State, int] = {start: 0}
    closed = set()
    nodes_expanded = 0

    while open_heap:
        _, _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        nodes_expanded += 1

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, nodes_expanded, g_score[current]

        for move, nxt in neighbors(current):
            tentative_g = g_score[current] + 1
            if nxt in closed:
                continue
            if tentative_g < g_score.get(nxt, 10**9):
                came_from[nxt] = (current, move)
                g_score[nxt] = tentative_g
                f = tentative_g + manhattan(nxt)
                counter += 1
                heapq.heappush(open_heap, (f, counter, nxt))

    return [], nodes_expanded, -1


def bfs(start: State, goal: State = GOAL) -> Tuple[List[Tuple[Optional[str], State]], int, int]:
    """Breadth-first search (uninformed). Returns (path, nodes_expanded, path_cost)."""
    queue: deque[State] = deque([start])
    came_from: Dict[State, Tuple[Optional[State], Optional[str]]] = {
        start: (None, None)
    }
    depth: Dict[State, int] = {start: 0}
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, nodes_expanded, depth[current]

        for move, nxt in neighbors(current):
            if nxt not in came_from:
                came_from[nxt] = (current, move)
                depth[nxt] = depth[current] + 1
                queue.append(nxt)

    return [], nodes_expanded, -1


def print_solution(
    name: str,
    path: List[Tuple[Optional[str], State]],
    nodes_expanded: int,
    path_cost: int,
    show_every_step: bool = True,
) -> None:
    print("\n" + "-" * 50)
    print(f"  Algorithm      : {name}")
    print(f"  Path cost      : {path_cost} moves")
    print(f"  Nodes expanded : {nodes_expanded}")
    print(f"  Solution length: {len(path) - 1} steps")
    print("-" * 50)

    if not path:
        print("  No solution found.")
        return

    if show_every_step:
        for i, (move, state) in enumerate(path):
            if i == 0:
                print_state(state, f"Step 0 (start)")
            else:
                print(f"\n  Move: {move}")
                print_state(state, f"Step {i}")
    else:
        print_state(path[0][1], "Start")
        print_state(path[-1][1], "Goal reached")


def run_demo(start: State) -> None:
    print("=" * 50)
    print("=== 8-Puzzle Problem Demo (A* + BFS) ===")
    print("=" * 50)
    print("Puzzle : Classic 3x3 sliding puzzle (8 tiles + blank)")
    print("Goal   : tiles in order 1..8 with blank at bottom-right")
    print()

    print_state(start, "Initial state")
    print()
    print_state(GOAL, "Goal state")

    if not is_solvable(start):
        print("\n  ERROR: Start state is not solvable. Aborting.")
        sys.exit(1)
    print("\n  Solvability check: PASSED (even inversion count)")

    # --- A* ---
    print("\n" + "=" * 50)
    print("Running A* (heuristic = Manhattan distance)...")
    print("=" * 50)
    path_a, expanded_a, cost_a = astar(start)
    print_solution("A* (Manhattan)", path_a, expanded_a, cost_a, show_every_step=True)

    # --- BFS comparison ---
    print("\n" + "=" * 50)
    print("Running BFS (for comparison)...")
    print("=" * 50)
    path_b, expanded_b, cost_b = bfs(start)
    # For BFS, print summary + start/goal only to keep screenshot readable;
    # path cost should match A* on an unweighted graph.
    print_solution("BFS", path_b, expanded_b, cost_b, show_every_step=False)

    print("\n" + "=" * 50)
    print("Comparison Summary")
    print("=" * 50)
    print(f"  {'Algorithm':<18} {'Path cost':>10} {'Nodes expanded':>16}")
    print(f"  {'-'*18} {'-'*10} {'-'*16}")
    print(f"  {'A* (Manhattan)':<18} {cost_a:>10} {expanded_a:>16}")
    print(f"  {'BFS':<18} {cost_b:>10} {expanded_b:>16}")
    print()
    print("  Note: Both find an optimal path cost; A* typically expands fewer nodes.")
    print("=" * 50)


def main() -> None:
    # Solvable start (~4 optimal moves - clear for lab screenshots,
    # and shows A* expanding fewer nodes than BFS).
    #   1 3 _
    #   4 2 5
    #   7 8 6
    start: State = (1, 3, 0, 4, 2, 5, 7, 8, 6)

    print("(Default solvable start - no input needed)\n")
    run_demo(start)


if __name__ == "__main__":
    main()
