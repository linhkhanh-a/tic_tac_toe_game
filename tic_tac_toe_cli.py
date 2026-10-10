"""
Terminal version (the original code, with edge cases handled).

Run: python tic_tac_toe_cli.py
"""

from game_logic import new_board, is_valid_move, write_player_sign, check_winning, SIGNS


def print_board(board):
    print("--------")
    for row in board:
        print(row)
    print("--------")


def ask_int(prompt):
    '''Keep asking until the player types a whole number.'''
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(f"'{raw}' is not a whole number, try again.")


def play_turn(player, board):
    sign = SIGNS[player]
    while True:
        x = ask_int(f"Player {player}'s turn ({sign}). Enter row x (0-2): ")
        y = ask_int(f"Player {player}'s turn ({sign}). Enter column y (0-2): ")
        ok, reason = is_valid_move(board, x, y)
        if ok:
            break
        print(reason, "Try again.")

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
        print("It's a draw!")
    else:
        print(f"Player {result} wins!")
    print("End")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame exited.")
