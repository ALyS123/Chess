# client.py

import socket
import threading

SERVER_IP = input("Enter server IP: ")  # e.g., 174.162.xx.xx
PORT = 5001

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print(f"[Opponent] {data.decode()}")
        except:
            print("Connection closed by server.")
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print("Connected to server.")

        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        while True:
            msg = input()
            if msg.lower() == "exit":
                break
            s.sendall(msg.encode())

if __name__ == "__main__":
    main()
