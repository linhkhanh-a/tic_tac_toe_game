"""
Ban choi tren terminal (code goc, da them xu ly edge cases).

Chay: python tic_tac_toe_cli.py
"""

from game_logic import new_board, is_valid_move, write_player_sign, check_winning


def print_board(board):
    print("--------")
    for row in board:
        print(row)
    print("--------")


def ask_int(prompt):
    '''Hoi cho den khi nguoi choi nhap dung 1 so nguyen.'''
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(f"'{raw}' khong phai so nguyen, nhap lai nhe.")


def play_turn(player, board):
    sign = "X" if player == "A" else "O"
    while True:
        x = ask_int(f"Den luot {player} ({sign}). Nhap toa do x (0-2): ")
        y = ask_int(f"Den luot {player} ({sign}). Nhap toa do y (0-2): ")
        ok, reason = is_valid_move(board, x, y)
        if ok:
            break
        print(reason, "Thu lai.")

    write_player_sign(player, board, x, y)
    print_board(board)


def main():
    board = new_board()
    player = "A"
    print_board(board)

    while check_winning(board) == "No win yet":
        play_turn(player, board)
        player = "B" if player == "A" else "A"

    result = check_winning(board)
    if result == "Draw":
        print("Hoa roi!")
    else:
        print(f"Nguoi choi {result} thang!")
    print("End")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nDa thoat game.")
