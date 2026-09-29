# Name: yathindakshiraju
# Email: yathindakshiraju.cs24@bmsce.ac.in
# AI Laboratory - Program 2: Tic Tac Toe using Minimax

# Default run is AI vs AI so it finishes without waiting for input.


WIN = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def show(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(board):
    for a, b, c in WIN:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def free_squares(board):
    return [i for i in range(9) if board[i] == " "]


def minimax(board, is_max, ai, human):
    # returns best score for the AI player
    w = check_winner(board)
    if w == ai:
        return 1
    if w == human:
        return -1
    if not free_squares(board):
        return 0

    if is_max:
        best = -999
        for i in free_squares(board):
            board[i] = ai
            best = max(best, minimax(board, False, ai, human))
            board[i] = " "
        return best
    else:
        best = 999
        for i in free_squares(board):
            board[i] = human
            best = min(best, minimax(board, True, ai, human))
            board[i] = " "
        return best


def best_move(board, player):
    opponent = "O" if player == "X" else "X"
    move = None
    best = -999
    for i in free_squares(board):
        board[i] = player
        score = minimax(board, False, player, opponent)
        board[i] = " "
        if score > best:
            best = score
            move = i
    return move


def main():
    print("Program 2: Tic Tac Toe")
    print("Minimax AI vs AI (both play optimally)")

    board = [" "] * 9
    show(board)
    turn = "X"
    n = 0

    while True:
        n += 1
        pos = best_move(board, turn)
        board[pos] = turn
        print(f"Turn {n}: {turn} plays at {pos + 1}")
        show(board)

        w = check_winner(board)
        if w:
            print(f"Winner: {w}")
            break
        if not free_squares(board):
            print("Result: DRAW")
            break

        turn = "O" if turn == "X" else "X"

    print("Finished.")


if __name__ == "__main__":
    main()
