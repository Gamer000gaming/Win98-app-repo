import tkinter as tk
import random

def open(window):
    Minesweeper(window)


class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.config(width=400, height=400)
        self.grid_size = 10  # Taille de la grille (10x10)
        self.num_mines = 15  # Nombre de mines

        self.buttons = {}
        self.mine_positions = set()
        self.revealed_cells = set()

        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        self.status_label = tk.Label(self.master, text="Démineur : Trouvez toutes les cases sans mine !", bg="white")
        self.status_label.pack(fill=tk.X)

        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(expand=True)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = tk.Button(self.grid_frame, width=2, height=1, command=lambda r=row, c=col: self.reveal_cell(r, c))
                btn.bind("<Button-3>", lambda event, r=row, c=col: self.toggle_flag(event, r, c))
                btn.grid(row=row, column=col)
                self.buttons[(row, col)] = btn

    def place_mines(self):
        while len(self.mine_positions) < self.num_mines:
            pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            self.mine_positions.add(pos)

    def reveal_cell(self, row, col):
        if (row, col) in self.revealed_cells:
            return
        self.revealed_cells.add((row, col))

        btn = self.buttons[(row, col)]
        if (row, col) in self.mine_positions:
            btn.config(text="💣", bg="red")
            self.game_over(False)
        else:
            mine_count = self.count_adjacent_mines(row, col)
            btn.config(text=str(mine_count) if mine_count > 0 else "", bg="lightgray", state=tk.DISABLED)
            if mine_count == 0:
                self.reveal_adjacent_cells(row, col)

            if self.check_win():
                self.game_over(True)

    def toggle_flag(self, event, row, col):
        btn = self.buttons[(row, col)]
        if btn.cget("text") == "🚩":
            btn.config(text="")
        else:
            btn.config(text="🚩")

    def count_adjacent_mines(self, row, col):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (dr != 0 or dc != 0) and (row + dr, col + dc) in self.mine_positions:
                    count += 1
        return count

    def reveal_adjacent_cells(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                adj_row, adj_col = row + dr, col + dc
                if (adj_row, adj_col) not in self.revealed_cells and (adj_row, adj_col) in self.buttons:
                    self.reveal_cell(adj_row, adj_col)

    def check_win(self):
        total_cells = self.grid_size * self.grid_size
        return len(self.revealed_cells) == total_cells - self.num_mines

    def game_over(self, won):
        for (row, col), btn in self.buttons.items():
            btn.config(state=tk.DISABLED)
            if (row, col) in self.mine_positions:
                btn.config(text="💣")
        self.status_label.config(text="Victoire !" if won else "Défaite !")
