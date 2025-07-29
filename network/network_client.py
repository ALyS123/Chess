# network/network_client.py

import socket
import threading

class NetworkClient:
    def __init__(self, server_ip: str, port: int = 5001):
        self.server_ip = server_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
        self.connected = False
        self.on_move_received = None  # callback: (from_index, to_index)

    def connect(self):
        try:
            self.sock.connect((self.server_ip, self.port))
            self.connected = True
            print("[Client] Connected to server.")
            threading.Thread(target=self.listen_to_server, daemon=True).start()
        except Exception as e:
            print(f"[Client] Connection failed: {e}")

    def listen_to_server(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break

                if data.startswith("CONNECTED"):
                    self.player_id = int(data.split()[1])
                    print(f"[Client] Assigned as Player {self.player_id}")
                else:
                    from_idx, to_idx = map(int, data.split(","))
                    print(f"[Client] Move received: {from_idx} → {to_idx}")
                    if self.on_move_received:
                        self.on_move_received(from_idx, to_idx)
            except:
                break

    def send_move(self, from_index, to_index):
        if self.connected:
            move = f"{from_index},{to_index}"
            self.sock.sendall(move.encode())

    def get_player_id(self):
        return self.player_id

    def close(self):
        self.sock.close()
