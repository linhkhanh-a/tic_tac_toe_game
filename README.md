# Tic Tac Toe 🎮

A two-player Tic Tac Toe game in Python, playable in the terminal or in a simple desktop window.

**Heads up: I wrote the game logic myself, but the UI (`tic_tac_toe_gui.py`) was vibe coded with AI.** 😄

## Files

| File | What it is |
|---|---|
| `game_logic.py` | Board, move validation, win/draw checking |
| `tic_tac_toe_cli.py` | Terminal version (enter x, y coordinates) |
| `tic_tac_toe_gui.py` | Desktop UI with tkinter (click to play), vibe coded |

## How to run

Requires Python 3. No extra packages needed, tkinter ships with Python.

```bash
python tic_tac_toe_gui.py   # UI version
python tic_tac_toe_cli.py   # terminal version
```

Player A is **X**, player B is **O**. Coordinates in the terminal version go from 0 to 2.

## Edge cases handled

- Non-number input asks again instead of crashing
- Coordinates outside 0–2 are rejected (including negatives, which Python would otherwise accept as list indices)
- Can't play on a cell that's already taken
- Game ends in a draw when the board is full with no winner
- Ctrl+C exits cleanly

## UI features

- Click a cell to play, turn indicator at the top
- Winning line gets highlighted
- Score tracker across rounds + "New game" button
