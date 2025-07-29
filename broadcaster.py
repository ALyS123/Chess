# broadcaster.py
import socket
import time

BROADCAST_PORT = 5002
MESSAGE = b"CHESS_HOST"

def broadcast_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            s.sendto(MESSAGE, ('<broadcast>', BROADCAST_PORT))
            time.sleep(1)

if __name__ == "__main__":
    broadcast_ip()
