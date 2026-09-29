#!/usr/bin/env python3
"""
Tic-Tac-Toe with Minimax AI
===========================
AI lab program: adversarial search using the Minimax algorithm.

Modes:
  - Default (demo): AI vs AI - fully automatic, screenshot-friendly
  - Interactive: Human (X) vs AI (O) when run with --interactive

Board positions are numbered 1-9 (row-major):
  1 | 2 | 3
  ---------
  4 | 5 | 6
  ---------
  7 | 8 | 9
"""

from __future__ import annotations

import sys
from typing import List, Optional, Tuple

Player = str  # "X" or "O"
Board = List[str]

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def empty_board() -> Board:
    return [" "] * 9


def print_board(board: Board, title: str = "Board") -> None:
    print(f"\n  --- {title} ---")
    rows = [
        f"   {board[0]} | {board[1]} | {board[2]} ",
        "  -----------",
        f"   {board[3]} | {board[4]} | {board[5]} ",
        "  -----------",
        f"   {board[6]} | {board[7]} | {board[8]} ",
    ]
    for line in rows:
        print(line)
    print()


def winner(board: Board) -> Optional[Player]:
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: Board) -> bool:
    return all(c != " " for c in board)


def available_moves(board: Board) -> List[int]:
    return [i for i, c in enumerate(board) if c == " "]


def evaluate(board: Board, maximizer: Player) -> int:
    """Terminal utility from maximizer's perspective."""
    w = winner(board)
    if w == maximizer:
        return 1
    if w is not None:
        return -1
    return 0


def minimax(
    board: Board,
    depth: int,
    is_maximizing: bool,
    maximizer: Player,
    minimizer: Player,
) -> Tuple[int, Optional[int]]:
    """
    Classic minimax.
    Returns (score, best_move_index).
    """
    if winner(board) is not None or is_full(board):
        return evaluate(board, maximizer), None

    best_move: Optional[int] = None

    if is_maximizing:
        best_score = -999
        for move in available_moves(board):
            board[move] = maximizer
            score, _ = minimax(board, depth + 1, False, maximizer, minimizer)
            board[move] = " "
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    best_score = 999
    for move in available_moves(board):
        board[move] = minimizer
        score, _ = minimax(board, depth + 1, True, maximizer, minimizer)
        board[move] = " "
        if score < best_score:
            best_score = score
            best_move = move
    return best_score, best_move


def best_move_for(board: Board, player: Player) -> int:
    opponent = "O" if player == "X" else "X"
    # Current player is the maximizer for this decision
    _, move = minimax(board, 0, True, player, opponent)
    if move is None:
        moves = available_moves(board)
        return moves[0]
    return move


def announce_result(board: Board) -> None:
    w = winner(board)
    if w:
        print(f"  >>> Winner: {w}")
    else:
        print("  >>> Result: DRAW")


def play_ai_vs_ai() -> None:
    """Non-interactive demo: two minimax agents play until terminal state."""
    print("=" * 50)
    print("=== Tic-Tac-Toe Demo (AI vs AI, Minimax) ===")
    print("=" * 50)
    print("X = Maximizing AI")
    print("O = Minimizing AI")
    print("Both players choose optimal minimax moves.")

    board = empty_board()
    print_board(board, "Initial (empty)")
    current: Player = "X"
    turn = 0

    while True:
        turn += 1
        move = best_move_for(board, current)
        board[move] = current
        print(f"  Turn {turn}: Player {current} plays position {move + 1}")
        print_board(board, f"After {current}'s move")

        if winner(board) or is_full(board):
            announce_result(board)
            break
        current = "O" if current == "X" else "X"

    print("=" * 50)
    print("Demo complete. (Both play optimally -> expected DRAW)")
    print("=" * 50)


def play_human_vs_ai() -> None:
    """Interactive: Human X vs Minimax AI O."""
    print("=" * 50)
    print("=== Tic-Tac-Toe (Human X vs AI O) ===")
    print("=" * 50)
    print("Enter a position 1-9 when prompted.")

    board = empty_board()
    print_board(board, "Initial")

    while True:
        # Human move
        while True:
            raw = input("  Your move (1-9): ").strip()
            if not raw.isdigit():
                print("  Please enter a number 1-9.")
                continue
            pos = int(raw) - 1
            if pos not in range(9) or board[pos] != " ":
                print("  Invalid / occupied square. Try again.")
                continue
            board[pos] = "X"
            break

        print_board(board, "After your move")
        if winner(board) or is_full(board):
            announce_result(board)
            break

        # AI move
        move = best_move_for(board, "O")
        board[move] = "O"
        print(f"  AI plays position {move + 1}")
        print_board(board, "After AI move")
        if winner(board) or is_full(board):
            announce_result(board)
            break

    print("=" * 50)


def main() -> None:
    if "--interactive" in sys.argv:
        play_human_vs_ai()
    else:
        print("(Default: AI vs AI demo - no input needed)")
        print("(Re-run with --interactive for Human vs AI)\n")
        play_ai_vs_ai()


if __name__ == "__main__":
    main()
