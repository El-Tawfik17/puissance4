import copy
import math

from game import (
    get_valid_moves,
    play_move,
    check_winner,
    game_status,
    ROWS,
    COLS,
    EMPTY
)

AI_PLAYER = 2
HUMAN_PLAYER = 1
nodes_explored = 0

def score_window(window):
    score = 0

    ai_count = window.count(AI_PLAYER)
    human_count = window.count(HUMAN_PLAYER)
    empty_count = window.count(EMPTY)

    if ai_count == 4:
        score += 100000

    elif ai_count == 3 and empty_count == 1:
        score += 100

    elif ai_count == 2 and empty_count == 2:
        score += 10

    if human_count == 4:
        score -= 100000

    elif human_count == 3 and empty_count == 1:
        score -= 120

    elif human_count == 2 and empty_count == 2:
        score -= 10

    return score


def evaluate_board(board):
    score = 0

    # Bonus pour le centre
    center_col = COLS // 2
    center_count = 0

    for row in range(ROWS):
        if board[row][center_col] == AI_PLAYER:
            center_count += 1

    score += center_count * 6

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [
                board[row][col],
                board[row][col + 1],
                board[row][col + 2],
                board[row][col + 3]
            ]
            score += score_window(window)

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [
                board[row][col],
                board[row + 1][col],
                board[row + 2][col],
                board[row + 3][col]
            ]
            score += score_window(window)

    # Diagonale descendante
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [
                board[row][col],
                board[row + 1][col + 1],
                board[row + 2][col + 2],
                board[row + 3][col + 3]
            ]
            score += score_window(window)

    # Diagonale montante
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [
                board[row][col],
                board[row - 1][col + 1],
                board[row - 2][col + 2],
                board[row - 3][col + 3]
            ]
            score += score_window(window)

    return score


def minimax(board, depth, maximizing_player):
    global nodes_explored
    nodes_explored += 1
    status = game_status(board)

    if status == "PLAYER_TWO_WIN":
        return None, 1000000

    if status == "PLAYER_ONE_WIN":
        return None, -1000000

    if status == "DRAW":
        return None, 0

    if depth == 0:
        return None, evaluate_board(board)

    valid_moves = get_valid_moves(board)

    if maximizing_player:
        best_score = -math.inf
        best_col = valid_moves[0]

        for col in valid_moves:
            board_copy = copy.deepcopy(board)
            play_move(board_copy, col, AI_PLAYER)

            _, score = minimax(
                board_copy,
                depth - 1,
                False
            )

            if score > best_score:
                best_score = score
                best_col = col

        return best_col, best_score

    else:
        best_score = math.inf
        best_col = valid_moves[0]

        for col in valid_moves:
            board_copy = copy.deepcopy(board)
            play_move(board_copy, col, HUMAN_PLAYER)

            _, score = minimax(
                board_copy,
                depth - 1,
                True
            )

            if score < best_score:
                best_score = score
                best_col = col

        return best_col, best_score


def choose_move(board, depth=4):
    global nodes_explored
    nodes_explored = 0
    col, score = minimax(board, depth, True)
    print(
    "Minimax explored :",
    nodes_explored
    )
    return col
def get_nodes_explored():
    return nodes_explored