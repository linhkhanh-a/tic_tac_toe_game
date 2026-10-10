"""
Core Tic Tac Toe logic, shared by the terminal version and the website.

Edge cases handled:
- A cell that's already taken can't be played again
- Coordinates outside the board (e.g. 5 or -1) are rejected
  (note: Python accepts board[-1], so the range must be checked by hand)
- A full board with no winner ends the game as a draw
"""

EMPTY = " "
SIGNS = {"A": "X", "B": "O"}


def new_board():
    return [[EMPTY] * 3 for _ in range(3)]


def is_valid_move(board, x, y):
    '''
    Returns (True, "") if the move is allowed,
    otherwise (False, reason).
    '''
    if not (0 <= x <= 2 and 0 <= y <= 2):
        return False, "Coordinates must be between 0 and 2."
    if board[x][y] != EMPTY:
        return False, f"Cell ({x}, {y}) is already taken."
    return True, ""


def write_player_sign(player, board, x, y):
    '''
    player: "A" or "B"
    board: a 3x3 board
    x, y: the row and column the player chose
    '''
    board[x][y] = SIGNS[player]
    return board


def _line_winner(cells):
    cells = set(cells)
    if len(cells) == 1:
        if "X" in cells:
            return "A"
        if "O" in cells:
            return "B"
    return None


def _all_lines():
    '''Every set of 3 cells that wins: rows, columns, both diagonals.'''
    lines = [[(r, c) for c in range(3)] for r in range(3)]   # rows
    lines += [[(r, c) for r in range(3)] for c in range(3)]  # columns
    lines.append([(i, i) for i in range(3)])                 # diagonal 1
    lines.append([(i, 2 - i) for i in range(3)])             # diagonal 2
    return lines


def winning_cells(board):
    '''Returns the 3 cells of the winning line, or None.'''
    for cells in _all_lines():
        if _line_winner([board[r][c] for r, c in cells]):
            return cells
    return None


def check_winning(board):
    '''
    Returns "A", "B", "Draw", or "No win yet".
    '''
    cells = winning_cells(board)
    if cells:
        r, c = cells[0]
        return _line_winner([board[r][c]])

    if all(cell != EMPTY for row in board for cell in row):
        return "Draw"

    return "No win yet"
