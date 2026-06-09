import random
import copy

from game import get_valid_moves, play_move, check_winner


AI_PLAYER = 2
HUMAN_PLAYER = 1


def choose_move(board):
    valid_moves = get_valid_moves(board)

    if not valid_moves:
        return None

    # 1. Si l'IA peut gagner immédiatement
    for col in valid_moves:
        board_copy = copy.deepcopy(board)
        play_move(board_copy, col, AI_PLAYER)

        if check_winner(board_copy, AI_PLAYER):
            return col

    # 2. Si l'humain peut gagner au prochain coup, on bloque
    for col in valid_moves:
        board_copy = copy.deepcopy(board)
        play_move(board_copy, col, HUMAN_PLAYER)

        if check_winner(board_copy, HUMAN_PLAYER):
            return col

    # 3. Jouer au centre si possible
    if 3 in valid_moves:
        return 3

    # 4. Sinon jouer au hasard
    return random.choice(valid_moves)