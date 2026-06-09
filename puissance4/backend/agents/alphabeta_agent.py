import copy
import math

from game import (
    get_valid_moves,
    play_move,
    game_status
)

from agents.minimax_agent import (
    evaluate_board,
    AI_PLAYER,
    HUMAN_PLAYER
)

nodes_explored = 0
def alphabeta(
    board,
    depth,
    alpha,
    beta,
    maximizing_player
):
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

        value = -math.inf
        best_col = valid_moves[0]

        for col in valid_moves:

            board_copy = copy.deepcopy(board)

            play_move(
                board_copy,
                col,
                AI_PLAYER
            )

            _, score = alphabeta(
                board_copy,
                depth - 1,
                alpha,
                beta,
                False
            )

            if score > value:
                value = score
                best_col = col

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return best_col, value

    else:

        value = math.inf
        best_col = valid_moves[0]

        for col in valid_moves:

            board_copy = copy.deepcopy(board)

            play_move(
                board_copy,
                col,
                HUMAN_PLAYER
            )

            _, score = alphabeta(
                board_copy,
                depth - 1,
                alpha,
                beta,
                True
            )

            if score < value:
                value = score
                best_col = col

            beta = min(beta, value)

            if alpha >= beta:
                break

        return best_col, value
    
def choose_move(board, depth=5):
    global nodes_explored

    nodes_explored = 0

    col, score = alphabeta(
        board,
        depth,
        -math.inf,
        math.inf,
        True
    )

    print(
        "AlphaBeta explored :",
        nodes_explored
    )

    return col
def get_nodes_explored():
    return nodes_explored