const API_URL = "http://127.0.0.1:5000";

let board = [];
let currentPlayer = 1;
let gameOver = false;
let gamesPlayed = 0;
let redWins = 0;
let yellowWins = 0;
let draws = 0;

async function newGame() {
    const mode = document.getElementById("gameMode").value;
    const aiType = document.getElementById("aiType").value;
    const aiTypeP1 = document.getElementById("aiTypeP1").value;
    const aiTypeP2 = document.getElementById("aiTypeP2").value;

    const response = await fetch(`${API_URL}/new-game`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mode: mode,
            ai_type: aiType,
            ai_type_p1: aiTypeP1,
            ai_type_p2: aiTypeP2
        })
    });

    const data = await response.json();

    board = data.board;
    currentPlayer = data.current_player;
    gameOver = false;

    updateStatus(data.status);
    renderBoard();
    updateStatsDisplay();
}
async function play(column) {
    if (gameOver) {
        return;
    }

    const response = await fetch(`${API_URL}/play`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            column: column
        })
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    board = data.board;
    currentPlayer = data.current_player;
    if (data.ai_column !== undefined) {
    console.log("L'IA a joué dans la colonne :", data.ai_column);
    }
    if (data.ai_algorithm !== undefined) {
        document.getElementById("aiAlgorithm").innerText = data.ai_algorithm;
        document.getElementById("aiLastMove").innerText = data.ai_column;
        document.getElementById("aiNodes").innerText = data.ai_nodes_explored;
    }

    updateStatus(data.status);
    renderBoard();

    if (data.status !== "ONGOING") {
        gameOver = true;
        updateStats(data.status);
    }
}

function renderBoard() {
    const boardDiv = document.getElementById("board");
    boardDiv.innerHTML = "";

    for (let row = 0; row < 6; row++) {
        for (let col = 0; col < 7; col++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");

            if (board[row][col] === 1) {
                cell.classList.add("player1");
            }

            if (board[row][col] === 2) {
                cell.classList.add("player2");
            }

            cell.addEventListener("click", () => play(col));
            boardDiv.appendChild(cell);
        }
    }
}

function updateStatus(status) {
    const statusDiv = document.getElementById("status");

    if (status === "ONGOING") {
        if (currentPlayer === 1) {
            statusDiv.innerText = "Tour du joueur rouge";
        } else {
            statusDiv.innerText = "Tour du joueur jaune";
        }
    }

    if (status === "PLAYER_ONE_WIN") {
        statusDiv.innerText = "Le joueur rouge a gagné !";
    }

    if (status === "PLAYER_TWO_WIN") {
        statusDiv.innerText = "Le joueur jaune a gagné !";
    }

    if (status === "DRAW") {
        statusDiv.innerText = "Match nul !";
    }
}
function updateStatsDisplay() {
    document.getElementById("gamesPlayed").innerText = gamesPlayed;
    document.getElementById("redWins").innerText = redWins;
    document.getElementById("yellowWins").innerText = yellowWins;
    document.getElementById("draws").innerText = draws;
}
function updateStats(status) {
    if (status === "PLAYER_ONE_WIN") {
        gamesPlayed++;
        redWins++;
    }

    if (status === "PLAYER_TWO_WIN") {
        gamesPlayed++;
        yellowWins++;
    }

    if (status === "DRAW") {
        gamesPlayed++;
        draws++;
    }

    updateStatsDisplay();
}
async function aiStep() {
    if (gameOver) {
        return;
    }

    const response = await fetch(`${API_URL}/ai-step`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    board = data.board;
    currentPlayer = data.current_player;

    updateStatus(data.status);
    renderBoard();

    if (data.ai_algorithm !== undefined) {
        document.getElementById("aiAlgorithm").innerText = data.ai_algorithm;
        document.getElementById("aiLastMove").innerText = data.ai_column;
        document.getElementById("aiNodes").innerText = data.ai_nodes_explored;
    }

    if (data.status !== "ONGOING") {
        gameOver = true;
        updateStats(data.status);
    }
}
document
    .getElementById("newGameBtn")
    .addEventListener("click", newGame);
document
    .getElementById("aiStepBtn")
    .addEventListener("click", aiStep);
newGame();