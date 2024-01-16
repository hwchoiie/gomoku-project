import socket
import threading
import tkinter as tk
from logic import GomokuGUI

def handle_client(conn, game):
    while True:
        data = conn.recv(1024)  # Receive data from client (move)
        if not data:
            break
        row, col = map(int, data.decode().split(','))
        game.master.after(0, lambda: game.network_move(row, col))
        game.master.after(0, game.switch_player)

    conn.close()

def server_game():
    host = '127.0.0.1'
    port = 65431
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    conn, addr = server.accept()
    print(f"Connected by {addr}")

    root = tk.Tk()
    game = GomokuGUI(root, on_move=lambda r, c: conn.sendall(f"{r},{c}".encode()), is_my_turn=True)
    threading.Thread(target=handle_client, args=(conn, game)).start()
    root.mainloop()

if __name__ == "__main__":
    server_game()