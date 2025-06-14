# main.py

from game import Game
from scenes.menu import Menu

if __name__ == "__main__":
    import pygame
    pygame.init()

    game_instance = Game()
    menu = Menu(game_instance)
    mode = menu.run()

    if mode in ("offline", "local_host"):
        Game(mode=mode).run()
