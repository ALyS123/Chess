import socket

BROADCAST_PORT = 5002
GAME_PORT = 5001
DISCOVERY_TIMEOUT = 5  # seconds

def discover_host():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(DISCOVERY_TIMEOUT)
        s.bind(("", BROADCAST_PORT))

        print("[Client] Listening for host broadcast...")

        try:
            data, addr = s.recvfrom(1024)
            if data == b"CHESS_HOST":
                print(f"[Client] Discovered host at {addr[0]}")
                return addr[0]
        except socket.timeout:
            print("[Client] Host discovery timed out.")
            return None
