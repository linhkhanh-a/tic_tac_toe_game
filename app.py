"""
Website backend (Flask). All game rules run here in Python;
the browser only shows the board and sends clicks.

Run: python app.py  ->  open http://127.0.0.1:5000
"""

import uuid

from flask import Flask, jsonify, render_template, request

from game_logic import new_board, is_valid_move, write_player_sign, check_winning, winning_cells, SIGNS

app = Flask(__name__)

# Games kept in memory, one per browser tab: {game_id: state}
GAMES = {}
MAX_GAMES = 1000  # so the server doesn't fill up its memory forever


def game_state(game_id):
    game = GAMES[game_id]
    result = check_winning(game["board"])
    return {
        "game_id": game_id,
        "board": game["board"],
        "player": game["player"],
        "sign": SIGNS[game["player"]],
        "result": result,  # "A", "B", "Draw", or "No win yet"
        "winning_cells": winning_cells(game["board"]),
        "scores": game["scores"],
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/new")
def new_game():
    data = request.get_json(silent=True) or {}
    game_id = data.get("game_id")

    if game_id in GAMES:
        # New round, same players: keep the scoreboard
        scores = GAMES[game_id]["scores"]
    else:
        if len(GAMES) >= MAX_GAMES:
            GAMES.pop(next(iter(GAMES)))  # drop the oldest game
        game_id = uuid.uuid4().hex
        scores = {"A": 0, "B": 0, "Draw": 0}

    GAMES[game_id] = {"board": new_board(), "player": "A", "scores": scores}
    return jsonify(game_state(game_id))


@app.post("/api/move")
def move():
    data = request.get_json(silent=True) or {}
    game_id = data.get("game_id")
    if game_id not in GAMES:
        return jsonify(error="Game not found. Start a new game."), 404

    try:
        x, y = int(data.get("x")), int(data.get("y"))
    except (TypeError, ValueError):
        return jsonify(error="Coordinates must be whole numbers."), 400

    game = GAMES[game_id]
    if check_winning(game["board"]) != "No win yet":
        return jsonify(error="This game is over. Start a new one."), 400

    ok, reason = is_valid_move(game["board"], x, y)
    if not ok:
        return jsonify(error=reason), 400

    write_player_sign(game["player"], game["board"], x, y)

    result = check_winning(game["board"])
    if result == "No win yet":
        game["player"] = "B" if game["player"] == "A" else "A"
    else:
        game["scores"][result] += 1

    return jsonify(game_state(game_id))


if __name__ == "__main__":
    app.run(debug=True)
