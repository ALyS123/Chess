# main.py

from scenes.menu import Menu
from game import Game

if __name__ == "__main__":


    game_instance = Game()
    menu = Menu(game_instance)
    mode = menu.run()  # mode will be "1v1" or "AI"

    # You can now pass `mode` into the Game class if needed
    game_instance.run()