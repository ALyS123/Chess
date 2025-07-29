# main.py

from game import Game
from scenes.menu import Menu

if __name__ == "__main__":
    import pygame
    pygame.init()

    while True:
        game_instance = Game()
        menu = Menu(game_instance)
        mode = menu.run()

        if mode == "offline":
            Game(mode="offline").run()

        elif mode == "host":
            import subprocess
            import time

            try:
                # Start the TCP game server
                subprocess.Popen(["python", "server.py"])

                # Start the UDP broadcaster for LAN discovery
                subprocess.Popen(["python", "broadcaster.py"])

                # Optional: wait a moment to let the server start before connecting
                time.sleep(1)

                # Start the game and connect as host (localhost)
                Game(mode="local_host", host_ip="127.0.0.1").run()

            except Exception as e:
                print(f"Failed to start host mode: {e}")

        elif mode == "join":
            from network.client_auto_connect import discover_host

            host_ip = discover_host()
            if host_ip:
                Game(mode="local_host", host_ip=host_ip).run()
            else:
                print("Could not find host. Returning to menu.")

        elif mode == "menu":
            continue  # This lets us go back to the main menu

        else:
            break  # Optional: exit gracefully if needed