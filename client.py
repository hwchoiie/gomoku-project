import socket
import threading
import tkinter as tk
from logic import GomokuGUI

def listen_for_moves(client, game):
    while True:
        data = client.recv(1024)
        if not data:
            break
        row, col = map(int, data.decode().split(','))
        game.master.after(0, lambda: game.network_move(row, col))
        game.master.after(0, game.switch_player)

def client_game():
    host = '127.0.0.1'
    port = 65431
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    root = tk.Tk()
    game = GomokuGUI(root, on_move=lambda r, c: client.sendall(f"{r},{c}".encode()), is_my_turn=False)

    # Start listening for moves in a separate thread
    threading.Thread(target=listen_for_moves, args=(client, game), daemon=True).start()

    root.mainloop()
    client.close()

if __name__ == "__main__":
    client_game()
