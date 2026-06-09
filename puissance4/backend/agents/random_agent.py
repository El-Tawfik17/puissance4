import random
from game import get_valid_moves


def choose_move(board):
    valid_moves = get_valid_moves(board)

    if not valid_moves:
        return None

    return random.choice(valid_moves)