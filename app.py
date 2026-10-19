from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# All winning combinations on a Tic-Tac-Toe board
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def get_winner(board):
    """Return X or O if someone has won, otherwise None."""
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def make_move():
    data = request.get_json()
    board = data.get("board", [])
    position = data.get("position")
    player = data.get("player")

    # Check the request before changing the board.
    if len(board) != 9 or player not in ("X", "O"):
        return jsonify({"error": "Invalid game data."}), 400

    if not isinstance(position, int) or position < 0 or position > 8:
        return jsonify({"error": "That square does not exist."}), 400

    if board[position] != "":
        return jsonify({"error": "That square is already taken."}), 400

    board[position] = player
    winner = get_winner(board)
    draw = winner is None and all(square != "" for square in board)

    return jsonify({
        "board": board,
        "winner": winner,
        "draw": draw
    })


if __name__ == "__main__":
    # Run this file and open the local address shown in your terminal.
    app.run(debug=True)
