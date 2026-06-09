
from flask import Flask, jsonify, request
from flask_cors import CORS

from game import create_board, play_move, game_status, switch_player
from agents.heuristic_agent import choose_move as heuristic_ai_move
from agents.random_agent import choose_move as random_ai_move
from agents.minimax_agent import (
    choose_move as minimax_ai_move,
    get_nodes_explored as minimax_nodes
)
from agents.alphabeta_agent import (
    choose_move as alphabeta_ai_move,
    get_nodes_explored as alphabeta_nodes
)
app = Flask(__name__)
CORS(app)

board = create_board()
current_player = 1
game_mode = "HUMAN_VS_HUMAN"
ai_type = "RANDOM"
ai_type_p1 = "RANDOM"
ai_type_p2 = "HEURISTIC"
def get_ai_move(board, ai_type):
    ai_nodes_explored = 0

    if ai_type == "HEURISTIC":
        ai_column = heuristic_ai_move(board)
        ai_algorithm = "Heuristique"

    elif ai_type == "MINIMAX":
        ai_column = minimax_ai_move(board, depth=4)
        ai_nodes_explored = minimax_nodes()
        ai_algorithm = "Minimax"

    elif ai_type == "ALPHABETA":
        ai_column = alphabeta_ai_move(board, depth=5)
        ai_nodes_explored = alphabeta_nodes()
        ai_algorithm = "Alpha-Beta"

    else:
        ai_column = random_ai_move(board)
        ai_algorithm = "Aléatoire"

    return ai_column, ai_algorithm, ai_nodes_explored

@app.route("/")
def home():
    return jsonify({
        "message": "API Puissance 4 fonctionne"
    })


@app.route("/new-game", methods=["POST"])
def new_game():
    global board, current_player, game_mode, ai_type, ai_type_p1, ai_type_p2

    data = request.get_json()

    game_mode = data.get("mode", "HUMAN_VS_HUMAN")
    ai_type = data.get("ai_type", "RANDOM")
    ai_type_p1 = data.get("ai_type_p1", "RANDOM")
    ai_type_p2 = data.get("ai_type_p2", "HEURISTIC")

    board = create_board()
    current_player = 1

    return jsonify({
        "board": board,
        "current_player": current_player,
        "status": "ONGOING",
        "mode": game_mode,
        "ai_type": ai_type,
        "ai_type_p1": ai_type_p1,
        "ai_type_p2": ai_type_p2
    })
@app.route("/play", methods=["POST"])
@app.route("/play", methods=["POST"])
def play():
    global board, current_player, game_mode, ai_type

    ai_nodes_explored = 0
    ai_algorithm = "-"
    ai_column = None

    data = request.get_json()
    column = data.get("column")

    if column is None:
        return jsonify({"error": "Colonne manquante"}), 400

    success = play_move(board, column, current_player)

    if not success:
        return jsonify({"error": "Coup invalide"}), 400

    status = game_status(board)

    if status != "ONGOING":
        return jsonify({
            "board": board,
            "current_player": current_player,
            "status": status,
            "mode": game_mode,
            "ai_column": ai_column,
            "ai_algorithm": ai_algorithm,
            "ai_nodes_explored": ai_nodes_explored
        })

    if game_mode == "HUMAN_VS_HUMAN":
        current_player = switch_player(current_player)

        return jsonify({
            "board": board,
            "current_player": current_player,
            "status": status,
            "mode": game_mode,
            "ai_column": ai_column,
            "ai_algorithm": ai_algorithm,
            "ai_nodes_explored": ai_nodes_explored
        })

    if game_mode == "HUMAN_VS_AI":
        current_player = 2

        ai_column, ai_algorithm, ai_nodes_explored = get_ai_move(
            board,
            ai_type
        )

        if ai_column is not None:
            play_move(board, ai_column, current_player)

        status = game_status(board)

        if status == "ONGOING":
            current_player = 1

        return jsonify({
            "board": board,
            "current_player": current_player,
            "status": status,
            "mode": game_mode,
            "ai_column": ai_column,
            "ai_algorithm": ai_algorithm,
            "ai_nodes_explored": ai_nodes_explored
        })

    return jsonify({
        "error": "Mode de jeu inconnu",
        "mode": game_mode
    }), 400
@app.route("/ai-step", methods=["POST"])
def ai_step():
    global board, current_player, game_mode, ai_type_p1, ai_type_p2

    if game_mode != "AI_VS_AI":
        return jsonify({"error": "Le mode actuel n'est pas IA vs IA"}), 400

    status = game_status(board)

    if status != "ONGOING":
        return jsonify({
            "board": board,
            "current_player": current_player,
            "status": status
        })

    if current_player == 1:
        selected_ai = ai_type_p1
    else:
        selected_ai = ai_type_p2

    ai_column, ai_algorithm, ai_nodes_explored = get_ai_move(
        board,
        selected_ai
    )

    if ai_column is not None:
        play_move(board, ai_column, current_player)

    status = game_status(board)

    if status == "ONGOING":
        current_player = switch_player(current_player)

    return jsonify({
        "board": board,
        "current_player": current_player,
        "status": status,
        "ai_column": ai_column,
        "ai_algorithm": ai_algorithm,
        "ai_nodes_explored": ai_nodes_explored,
        "played_by": "Rouge" if current_player == 2 else "Jaune"
    })
@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()

    agent1 = data.get("agent1", "RANDOM")
    agent2 = data.get("agent2", "HEURISTIC")
    games = data.get("games", 100)

    results = {
        "games": games,
        "player1_wins": 0,
        "player2_wins": 0,
        "draws": 0
    }

    for _ in range(games):
        sim_board = create_board()
        sim_player = 1

        while True:
            if sim_player == 1:
                col, _, _ = get_ai_move(sim_board, agent1)
            else:
                col, _, _ = get_ai_move(sim_board, agent2)

            if col is not None:
                play_move(sim_board, col, sim_player)

            status = game_status(sim_board)

            if status == "PLAYER_ONE_WIN":
                results["player1_wins"] += 1
                break

            if status == "PLAYER_TWO_WIN":
                results["player2_wins"] += 1
                break

            if status == "DRAW":
                results["draws"] += 1
                break

            sim_player = switch_player(sim_player)

    return jsonify(results)
if __name__ == "__main__":
    app.run(debug=True)