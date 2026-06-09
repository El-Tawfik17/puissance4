from game import create_board, play_move, check_winner

board = create_board()

play_move(board, 0, 1)
play_move(board, 1, 1)
play_move(board, 2, 1)
play_move(board, 3, 1)

for row in board:
    print(row)

print("Victoire joueur 1 :", check_winner(board, 1))