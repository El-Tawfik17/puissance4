ROWS = 6
COLS = 7

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2


def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def is_valid_move(board, col):
    return 0 <= col < COLS and board[0][col] == EMPTY


def get_valid_moves(board):
    return [col for col in range(COLS) if is_valid_move(board, col)]


def play_move(board, col, player):
    if not is_valid_move(board, col):
        return False

    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True

    return False


def check_winner(board, player):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal up-right
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False


def is_full(board):
    return all(board[0][col] != EMPTY for col in range(COLS))


def switch_player(player):
    return PLAYER_TWO if player == PLAYER_ONE else PLAYER_ONE


def game_status(board):
    if check_winner(board, PLAYER_ONE):
        return "PLAYER_ONE_WIN"

    if check_winner(board, PLAYER_TWO):
        return "PLAYER_TWO_WIN"

    if is_full(board):
        return "DRAW"

    return "ONGOING"