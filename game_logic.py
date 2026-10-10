"""
Logic chung cua game Tic Tac Toe (dung cho ca ban terminal va ban UI).

Edge cases da xu ly:
- O da co nguoi danh roi -> khong cho danh de
- Toa do ngoai bang (vd 5, -1) -> bao loi
  (luu y: Python cho phep board[-1], nen phai check range thu cong)
- Hoa (bang day ma khong ai thang) -> ket thuc game
"""

EMPTY = " "
SIGNS = {"A": "X", "B": "O"}


def new_board():
    return [[EMPTY] * 3 for _ in range(3)]


def is_valid_move(board, x, y):
    '''
    Tra ve (True, "") neu nuoc di hop le,
    nguoc lai tra ve (False, ly do).
    '''
    if not (0 <= x <= 2 and 0 <= y <= 2):
        return False, "Toa do phai tu 0 den 2."
    if board[x][y] != EMPTY:
        return False, f"O ({x}, {y}) da co nguoi danh roi."
    return True, ""


def write_player_sign(player, board, x, y):
    '''
    player: "A" or "B"
    board: 1 bang 3x3
    x, y: toa do truc x va y cua luot choi ng choi player
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


def check_winning(board):
    '''
    Tra ve "A", "B", "Draw", hoac "No win yet".
    '''
    lines = []
    lines.extend(board)                                          # hang
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # cot
    lines.append([board[i][i] for i in range(3)])                # duong cheo 1
    lines.append([board[i][2 - i] for i in range(3)])            # duong cheo 2

    for line in lines:
        winner = _line_winner(line)
        if winner:
            return winner

    if all(cell != EMPTY for row in board for cell in row):
        return "Draw"

    return "No win yet"


def winning_cells(board):
    '''Tra ve 3 o tao thanh duong thang (de UI to mau), hoac None.'''
    candidates = []
    candidates += [[(r, c) for c in range(3)] for r in range(3)]
    candidates += [[(r, c) for r in range(3)] for c in range(3)]
    candidates.append([(i, i) for i in range(3)])
    candidates.append([(i, 2 - i) for i in range(3)])
    for cells in candidates:
        if _line_winner([board[r][c] for r, c in cells]):
            return cells
    return None
