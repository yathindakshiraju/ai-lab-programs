# yathindakshiraju
# yathindakshiraju.cs24@bmsce.ac.in
# AI Laboratory
# Program 3: 8 Puzzle - A* (Manhattan) and BFS

from collections import deque
import heapq

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def print_board(state, title=""):
    if title:
        print(title)
    for r in range(3):
        row = state[r * 3:(r + 1) * 3]
        print(" ".join("_" if x == 0 else str(x) for x in row))
    print()


def manhattan(state):
    # sum of |row diff| + |col diff| for each tile (ignore blank)
    h = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_pos = tile - 1
        r1, c1 = divmod(i, 3)
        r2, c2 = divmod(goal_pos, 3)
        h += abs(r1 - r2) + abs(c1 - c2)
    return h


def get_neighbors(state):
    blank = state.index(0)
    r, c = divmod(blank, 3)
    moves = []
    for dr, dc, name in [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_blank = nr * 3 + nc
            lst = list(state)
            lst[blank], lst[new_blank] = lst[new_blank], lst[blank]
            moves.append((name, tuple(lst)))
    return moves


def reconstruct(parent, goal):
    path = []
    cur = goal
    while cur is not None:
        move, prev = parent[cur]
        path.append((move, cur))
        cur = prev
    path.reverse()
    return path


def astar(start):
    # f = g + manhattan
    heap = []
    count = 0
    heapq.heappush(heap, (manhattan(start), count, start))
    parent = {start: (None, None)}
    g = {start: 0}
    visited = set()
    expanded = 0

    while heap:
        _, _, cur = heapq.heappop(heap)
        if cur in visited:
            continue
        visited.add(cur)
        expanded += 1

        if cur == GOAL:
            return reconstruct(parent, cur), expanded, g[cur]

        for move, nxt in get_neighbors(cur):
            new_g = g[cur] + 1
            if nxt in visited:
                continue
            if new_g < g.get(nxt, 999999):
                g[nxt] = new_g
                parent[nxt] = (move, cur)
                count += 1
                heapq.heappush(heap, (new_g + manhattan(nxt), count, nxt))

    return [], expanded, -1


def bfs(start):
    q = deque([start])
    parent = {start: (None, None)}
    depth = {start: 0}
    expanded = 0

    while q:
        cur = q.popleft()
        expanded += 1
        if cur == GOAL:
            return reconstruct(parent, cur), expanded, depth[cur]

        for move, nxt in get_neighbors(cur):
            if nxt not in parent:
                parent[nxt] = (move, cur)
                depth[nxt] = depth[cur] + 1
                q.append(nxt)

    return [], expanded, -1


def main():
    print("8 Puzzle")
    print("Goal: 1 2 3 / 4 5 6 / 7 8 _")
    print()

    # solvable start (about 4 moves)
    # 1 3 _
    # 4 2 5
    # 7 8 6
    start = (1, 3, 0, 4, 2, 5, 7, 8, 6)

    print_board(start, "Start:")
    print_board(GOAL, "Goal:")

    print("--- A* with Manhattan heuristic ---")
    path, expanded, cost = astar(start)
    print(f"Path cost: {cost}")
    print(f"Nodes expanded: {expanded}")
    for i, (move, state) in enumerate(path):
        if i == 0:
            print_board(state, "Step 0:")
        else:
            print(f"Move: {move}")
            print_board(state, f"Step {i}:")

    print("--- BFS ---")
    path2, expanded2, cost2 = bfs(start)
    print(f"Path cost: {cost2}")
    print(f"Nodes expanded: {expanded2}")
    print_board(path2[0][1], "Start:")
    print_board(path2[-1][1], "Reached goal:")

    print("Comparison")
    print(f"  A*: cost={cost}, expanded={expanded}")
    print(f"  BFS: cost={cost2}, expanded={expanded2}")


if __name__ == "__main__":
    main()
