import tkinter as tk
from tkinter import messagebox

class GomokuGUI:
    def __init__(self, master, on_move=None, is_my_turn=False):
        self.master = master
        self.master.title("Gomoku")
        self.on_move = on_move
        self.is_my_turn = is_my_turn
        self.initialize_game()

    def initialize_game(self):
        self.board_size = 15
        self.cell_size = 40
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'B'  # 'B' for black, 'W' for white
        self.game_over = False
        self.create_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.master, width=self.board_size*self.cell_size, 
                                height=self.board_size*self.cell_size, bg='brown')
        self.canvas.pack()

        for i in range(self.board_size):
            self.canvas.create_line(self.cell_size/2, (i + 0.5)*self.cell_size,
                                    self.board_size*self.cell_size - self.cell_size/2, 
                                    (i + 0.5)*self.cell_size, fill='black')
            self.canvas.create_line((i + 0.5)*self.cell_size, self.cell_size/2,
                                    (i + 0.5)*self.cell_size, 
                                    self.board_size*self.cell_size - self.cell_size/2, 
                                    fill='black')
        self.canvas.bind("<Button-1>", self.on_click)

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.is_my_turn = not self.is_my_turn   # Toggle the turn

    def on_click(self, event):
        if self.game_over or not self.is_my_turn:
            return
        x, y = event.x, event.y
        row, col = int(y // self.cell_size), int(x // self.cell_size)
        if self.is_valid_move(row, col):
            self.place_stone(row, col)
            if self.on_move:
                self.on_move(row, col)

    def network_move(self, row, col):
        self.master.after(0, lambda: self._network_move(row, col))

    def _network_move(self, row, col):
        if self.is_valid_move(row, col):
            self.place_stone(row, col)
            if self.check_winner(row, col):
                messagebox.showinfo("Gomoku", f"Player {self.current_player} wins!")
                self.game_over = True
            else:
                self.switch_player()

    def is_valid_move(self, row, col):
        return self.board[row][col] == ' '

    def place_stone(self, row, col):
        stone_color = 'black' if self.current_player == 'B' else 'white'
        self.canvas.create_oval((col + 0.25) * self.cell_size, (row + 0.25) * self.cell_size,
                                (col + 0.75) * self.cell_size, (row + 0.75) * self.cell_size,
                                fill=stone_color, outline=stone_color)
        self.board[row][col] = self.current_player
        if self.check_winner(row, col):
            messagebox.showinfo("Gomoku", f"Player {self.current_player} wins!")
            self.game_over = True
        else:
            self.switch_player()

    def check_winner(self, row, col):
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # right, down, diagonal down-right, diagonal down-left

        for dr, dc in directions:
            count = 1  # Count the current stone

            # Check in one direction
            for i in range(1, 5):
                if (0 <= row + dr*i < self.board_size and 0 <= col + dc*i < self.board_size 
                        and self.board[row + dr*i][col + dc*i] == player):
                    count += 1
                else: break

            # Check in the opposite direction
            for i in range(1, 5):
                if (0 <= row - dr*i < self.board_size and 0 <= col - dc*i < self.board_size 
                        and self.board[row - dr*i][col - dc*i] == player):
                    count += 1
                else:
                    break

            if count >= 5:  # Winning condition: at least 5 stones in a row
                return True

        return False

def ask_replay(self):
    if messagebox.askyesno("Play Again", "Do you want to play again?"):
        self.canvas.delete("all")
        self.initialize_game()
    else:
        self.master.quit()


# run the game
if __name__ == '__main__':
    root = tk.Tk()
    game = GomokuGUI(root)
    root.mainloop()