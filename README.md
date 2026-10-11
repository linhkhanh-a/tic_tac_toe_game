# Tic Tac Toe 🎮

A two-player Tic Tac Toe game with a Python (Flask) backend and a browser UI. Play a friend on another device with a **room code**, or share one screen. There's also a terminal version.

**▶ Play it live: https://tic-tac-toe-3mgs.onrender.com** (first load may take about a minute while the free server wakes up)

**Heads up: I wrote the game logic myself, but the website UI (`templates/index.html`) was vibe coded with AI.** 😄

## How it works

All the game rules run in Python on the server. The web page just draws the board and sends your clicks to the backend, which checks whose turn it is, validates the move, updates the board, and decides who won. Each browser asks the server for the latest board every second, so both players see moves appear live.

| File | What it is |
|---|---|
| `game_logic.py` | Board, move validation, win/draw checking (written by me) |
| `app.py` | Flask backend: rooms, turns, moves, rematches |
| `templates/index.html` | The web page UI (vibe coded) |
| `tic_tac_toe_cli.py` | Terminal version (type x, y coordinates) |
| `render.yaml`, `requirements.txt` | Deploy settings for Render |

## Run it

Requires Python 3.

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

Terminal version: `python tic_tac_toe_cli.py`

## Deploy (Render, free)

This repo includes `render.yaml`, so Render can set itself up:

1. Sign in at [render.com](https://render.com) with GitHub
2. **New** → **Blueprint** → pick this repo → **Apply**
3. Your game will be live at `https://tic-tac-toe-xxxx.onrender.com`

The server runs `gunicorn` with a single worker, because games live in memory and every request must reach the same process. On the free plan the site sleeps after 15 minutes without visitors, so the first visit after that takes about a minute to wake up, and open rooms are reset. While two people are playing, the page checks in every second, which keeps the server awake.

## How to play

**Online with a friend**
1. Click **Create a room**. You get a 4-letter code (like `K7QF`) and you play **X**.
2. Send your friend the code, or click **Copy invite link** and send the link.
3. Your friend types the code under **Join a friend's room** (or just opens the link) and plays **O**.
4. Take turns. After each round, press **Rematch**; whoever went second goes first next time.

**One screen:** click **Play on one screen** and take turns on the same device.

Three in a row (across, down, or diagonal) wins.

## Edge cases handled

- Can't play a square that's already taken
- Coordinates outside 0 to 2 are rejected (including negatives, which Python would otherwise accept as list indices)
- Non-number input is rejected instead of crashing
- A full board with no winner ends in a draw
- No moves allowed after the game is over
- You can only move on your own turn, and not before your friend has joined
- A third person who opens the link can watch but not play
- Refreshing the page keeps your seat in the room
- Shows when your friend seems disconnected
- Room codes skip look-alike characters (no 0/O or 1/I) and aren't case-sensitive
- Rooms nobody uses for an hour are cleaned up automatically

## API

| Endpoint | Body | What it does |
|---|---|---|
| `POST /api/rooms` | `{"local": false}` | Create a room, returns the code and your secret player token |
| `POST /api/rooms/<code>/join` | `{"token": "..."}` (optional) | Take the free seat, rejoin your old one, or watch |
| `GET /api/rooms/<code>?token=...` | | Latest board (the page calls this every second) |
| `POST /api/rooms/<code>/move` | `{"token": "...", "x": 0, "y": 2}` | Make a move |
| `POST /api/rooms/<code>/rematch` | `{"token": "..."}` | Start the next round |
