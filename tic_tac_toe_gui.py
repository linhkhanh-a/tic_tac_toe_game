"""
Ban co UI (tkinter, co san trong Python, khong can cai them gi).

Chay: python tic_tac_toe_gui.py
"""

import tkinter as tk

from game_logic import new_board, is_valid_move, write_player_sign, check_winning, winning_cells

BG = "#1e1e2e"
CELL_BG = "#2a2a3d"
CELL_HOVER = "#34344a"
X_COLOR = "#f38ba8"
O_COLOR = "#89b4fa"
WIN_BG = "#a6e3a1"
TEXT = "#cdd6f4"


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        root.title("Tic Tac Toe")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.scores = {"A": 0, "B": 0, "Draw": 0}

        self.status = tk.Label(root, font=("Helvetica", 16, "bold"), bg=BG, fg=TEXT, pady=10)
        self.status.pack()

        grid = tk.Frame(root, bg=BG, padx=12, pady=6)
        grid.pack()
        self.buttons = []
        for x in range(3):
            row = []
            for y in range(3):
                btn = tk.Button(
                    grid, text="", width=4, height=2,
                    font=("Helvetica", 32, "bold"),
                    bg=CELL_BG, activebackground=CELL_HOVER,
                    relief="flat", bd=0, highlightthickness=0,
                    command=lambda x=x, y=y: self.on_click(x, y),
                )
                btn.grid(row=x, column=y, padx=4, pady=4)
                row.append(btn)
            self.buttons.append(row)

        self.score_label = tk.Label(root, font=("Helvetica", 12), bg=BG, fg=TEXT, pady=6)
        self.score_label.pack()

        tk.Button(
            root, text="Van moi", font=("Helvetica", 12, "bold"),
            bg="#45475a", fg=TEXT, activebackground="#585b70",
            relief="flat", padx=16, pady=6, command=self.reset,
        ).pack(pady=(0, 14))

        self.reset()

    def reset(self):
        self.board = new_board()
        self.player = "A"
        self.game_over = False
        for row in self.buttons:
            for btn in row:
                btn.config(text="", bg=CELL_BG, state="normal")
        self.update_status()

    def update_status(self, message=None):
        if message is None:
            sign = "X" if self.player == "A" else "O"
            message = f"Den luot {self.player} ({sign})"
        self.status.config(text=message)
        self.score_label.config(
            text=f"A (X): {self.scores['A']}    B (O): {self.scores['B']}    Hoa: {self.scores['Draw']}"
        )

    def on_click(self, x, y):
        if self.game_over:
            return
        ok, _ = is_valid_move(self.board, x, y)
        if not ok:  # o da danh roi -> bo qua
            return

        write_player_sign(self.player, self.board, x, y)
        sign = self.board[x][y]
        self.buttons[x][y].config(text=sign, fg=X_COLOR if sign == "X" else O_COLOR,
                                  disabledforeground=X_COLOR if sign == "X" else O_COLOR)

        result = check_winning(self.board)
        if result == "No win yet":
            self.player = "B" if self.player == "A" else "A"
            self.update_status()
            return

        self.game_over = True
        self.scores[result] += 1
        if result == "Draw":
            self.update_status("Hoa roi!")
        else:
            for r, c in winning_cells(self.board):
                self.buttons[r][c].config(bg=WIN_BG)
            self.update_status(f"Nguoi choi {result} thang! 🎉")
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()
