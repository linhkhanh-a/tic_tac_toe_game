# Tic Tac Toe 🎮

A two-player Tic Tac Toe game with a Python (Flask) backend and a browser UI. There's also a terminal version.

**Heads up: I wrote the game logic myself, but the website UI (`templates/index.html`) was vibe coded with AI.** 😄

## How it works

All the game rules run in Python on the server. The web page just draws the board and sends your clicks to the backend, which checks the move, updates the board, and decides who won.

| File | What it is |
|---|---|
| `game_logic.py` | Board, move validation, win/draw checking (written by me) |
| `app.py` | Flask backend: API for starting a game and making moves |
| `templates/index.html` | The web page UI (vibe coded) |
| `tic_tac_toe_cli.py` | Terminal version (type x, y coordinates) |

## Run it

Requires Python 3.

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

Terminal version: `python tic_tac_toe_cli.py`

## How to play

Player A is **X**, player B is **O**. Take turns clicking a square. Get three in a row (across, down, or diagonal) to win. Press **New round** to play again; the scoreboard keeps counting.

## Edge cases handled

- Can't play a square that's already taken
- Coordinates outside 0 to 2 are rejected (including negatives, which Python would otherwise accept as list indices)
- Non-number input is rejected instead of crashing
- A full board with no winner ends in a draw
- No moves allowed after the game is over
- Each browser tab gets its own game, so two people on different tabs don't overwrite each other

## API

| Endpoint | Body | Returns |
|---|---|---|
| `POST /api/new` | `{"game_id": "..."}` (optional, keeps the score) | game state |
| `POST /api/move` | `{"game_id": "...", "x": 0, "y": 2}` | game state, or `{"error": "..."}` |
