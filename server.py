# server.py

import socket
import threading

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5001  # Match your port forwarding

clients = []

def handle_client(conn, addr, player_id):
    print(f"Player {player_id} connected from {addr}")
    conn.sendall(f"CONNECTED {player_id}".encode())

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[Player {player_id}] {data.decode()}")
            # Relay to other player
            for c in clients:
                if c != conn:
                    c.sendall(data)
        except:
            break

    print(f"Player {player_id} disconnected.")
    conn.close()
    clients.remove(conn)

def main():
    print("Starting Chess Server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on port {PORT}...")

        while len(clients) < 2:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr, len(clients))).start()

        print("Two players connected. Game can begin!")

if __name__ == "__main__":
    main()
