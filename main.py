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
            print("HOST option selected")  # TODO: connect host flow

        elif mode == "join":
            print("JOIN option selected")  # TODO: connect join flow

        elif mode == "menu":
            continue  # This lets us go back to the main menu

        else:
            break  # Optional: exit gracefully if needed