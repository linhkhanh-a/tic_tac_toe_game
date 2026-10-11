"""
Website backend (Flask). All game rules run here in Python;
the browser only shows the board and sends clicks.

Two ways to play:
- Online room: player A creates a room and gets a 4-letter code,
  player B joins with that code from their own device.
- One screen: both players share one device (same API, both seats
  belong to the same browser).

Run: python app.py  ->  open http://127.0.0.1:5000
"""

import secrets
import threading
import time

from flask import Flask, jsonify, render_template, request

from game_logic import new_board, is_valid_move, write_player_sign, check_winning, winning_cells

app = Flask(__name__)

# No 0/O or 1/I so codes are easy to read out loud
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 4
ROOM_TTL = 60 * 60       # delete rooms nobody has touched for 1 hour
OFFLINE_AFTER = 10       # seconds without a poll -> show player as disconnected
MAX_ROOMS = 500

ROOMS = {}               # {code: room}
LOCK = threading.Lock()  # the server handles requests on several threads


# ---------- helpers ----------

def _new_code():
    while True:
        code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
        if code not in ROOMS:
            return code


def _cleanup(now):
    for code in [c for c, r in ROOMS.items() if now - r["last_active"] > ROOM_TTL]:
        del ROOMS[code]
    while len(ROOMS) >= MAX_ROOMS:  # still full: drop the least recently used room
        oldest = min(ROOMS, key=lambda c: ROOMS[c]["last_active"])
        del ROOMS[oldest]


def _seat(room, token):
    '''Which seat does this browser hold? "A", "B", "both" (one screen) or "spectator".'''
    if not token:
        return "spectator"
    if room["local"] and token == room["tokens"]["A"]:
        return "both"
    for seat in ("A", "B"):
        if room["tokens"][seat] == token:
            return seat
    return "spectator"


def _touch(room, seat, now):
    room["last_active"] = now
    if seat in ("A", "B"):
        room["last_seen"][seat] = now
    elif seat == "both":
        room["last_seen"]["A"] = room["last_seen"]["B"] = now


def _state(room, seat, token=None):
    now = time.time()
    data = {
        "code": room["code"],
        "local": room["local"],
        "you": seat,
        "board": room["board"],
        "turn": room["turn"],
        "result": check_winning(room["board"]),  # "A", "B", "Draw" or "No win yet"
        "winning_cells": winning_cells(room["board"]),
        "scores": room["scores"],
        "players": {
            s: {
                "joined": room["tokens"][s] is not None,
                "online": now - room["last_seen"][s] < OFFLINE_AFTER,
            }
            for s in ("A", "B")
        },
    }
    if token:
        data["token"] = token  # only sent to the browser that owns it
    return data


def _body():
    return request.get_json(silent=True) or {}


def _get_room(code):
    return ROOMS.get((code or "").strip().upper())


def _not_found(code):
    return jsonify(error=f"No room with code {code.upper()}. Check the code, or the room may have expired."), 404


# ---------- routes ----------

@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/rooms")
def create_room():
    local = bool(_body().get("local"))
    now = time.time()
    token = secrets.token_urlsafe(16)
    with LOCK:
        _cleanup(now)
        code = _new_code()
        room = {
            "code": code,
            "local": local,
            "board": new_board(),
            "turn": "A",
            "starter": "A",
            "scores": {"A": 0, "B": 0, "Draw": 0},
            "tokens": {"A": token, "B": token if local else None},
            "last_seen": {"A": now, "B": now if local else 0},
            "last_active": now,
        }
        ROOMS[code] = room
        return jsonify(_state(room, _seat(room, token), token))


@app.post("/api/rooms/<code>/join")
def join_room(code):
    token = _body().get("token")
    now = time.time()
    with LOCK:
        room = _get_room(code)
        if not room:
            return _not_found(code)

        seat = _seat(room, token)
        if seat == "spectator":
            if room["tokens"]["B"] is None:
                token = secrets.token_urlsafe(16)
                room["tokens"]["B"] = token
                seat = "B"
            else:
                token = None  # room is full: you can watch, not play

        _touch(room, seat, now)
        return jsonify(_state(room, seat, token))


@app.get("/api/rooms/<code>")
def get_room(code):
    token = request.args.get("token")
    now = time.time()
    with LOCK:
        room = _get_room(code)
        if not room:
            return _not_found(code)
        seat = _seat(room, token)
        _touch(room, seat, now)
        return jsonify(_state(room, seat))


@app.post("/api/rooms/<code>/move")
def move(code):
    data = _body()
    now = time.time()
    with LOCK:
        room = _get_room(code)
        if not room:
            return _not_found(code)

        seat = _seat(room, data.get("token"))
        if seat == "spectator":
            return jsonify(error="You're watching this game, so you can't make moves."), 403
        if room["tokens"]["B"] is None:
            return jsonify(error="Wait for your friend to join first."), 400
        if check_winning(room["board"]) != "No win yet":
            return jsonify(error="This round is over. Press Rematch to play again."), 400
        if seat != "both" and seat != room["turn"]:
            return jsonify(error="It's not your turn yet."), 400

        try:
            x, y = int(data.get("x")), int(data.get("y"))
        except (TypeError, ValueError):
            return jsonify(error="Coordinates must be whole numbers."), 400

        ok, reason = is_valid_move(room["board"], x, y)
        if not ok:
            return jsonify(error=reason), 400

        write_player_sign(room["turn"], room["board"], x, y)
        result = check_winning(room["board"])
        if result == "No win yet":
            room["turn"] = "B" if room["turn"] == "A" else "A"
        else:
            room["scores"][result] += 1

        _touch(room, seat, now)
        return jsonify(_state(room, seat))


@app.post("/api/rooms/<code>/rematch")
def rematch(code):
    now = time.time()
    with LOCK:
        room = _get_room(code)
        if not room:
            return _not_found(code)

        seat = _seat(room, _body().get("token"))
        if seat == "spectator":
            return jsonify(error="Only the players can start a rematch."), 403
        if check_winning(room["board"]) == "No win yet" and not room["local"]:
            return jsonify(error="Finish this round first."), 400

        # Take turns going first each round, so it's fair
        room["starter"] = "B" if room["starter"] == "A" else "A"
        room["turn"] = room["starter"]
        room["board"] = new_board()

        _touch(room, seat, now)
        return jsonify(_state(room, seat))


if __name__ == "__main__":
    app.run(debug=True)
