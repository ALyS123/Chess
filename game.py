# game.py

import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, FPS
from board.board import Board
from controllers.input_handler import InputHandler
from board.rule_engine import GameRules
from scenes.result_screen import ResultScreen


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.running = True
        self.white_turn = True
        self.king_in_check : bool


        self.board = Board()
        self.game_rules = GameRules(self.board)  # Initialize game_rules with the board reference
        self.input_handler = InputHandler(self.board, self)


    def run(self):
        while self.running:
            self.screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                
                self.input_handler.handle(event)


            # use this for locking only the king will be played or a piece that can move the king out of check
            self.king_in_check = self.game_rules.king_in_check(self.white_turn)  # True if the king is in check False if not 
            # Check for checkmate
            if self.game_rules.is_checkmate(self.white_turn):
                message = f"{'Black' if self.white_turn else 'White'} Wins by Checkmate!"
                result = ResultScreen(self, message).run()
                if result == "menu":
                    self.running = False
                    from scenes.menu import Menu
                    from game import Game
                    Menu(self).run()
                    Game().run()
                    return  # <- This prevents drawing to a closed screen
                else:
                    self.running = False

            elif self.game_rules.is_stalemate(self.white_turn):
                result = ResultScreen(self, "Stalemate! It's a draw.").run()
                if result == "menu":
                    self.running = False
                    from scenes.menu import Menu
                    from game import Game
                    Menu(self).run()
                    Game().run()
                    return  # <- This prevents drawing to a closed screen
                else:
                    self.running = False

            elif self.game_rules.is_draw_by_insufficient_material():
                result = ResultScreen(self, "Draw! Insufficient material.").run()
                if result == "menu":
                    self.running = False
                    from scenes.menu import Menu
                    from game import Game
                    Menu(self).run()
                    Game().run()
                    return  # <- This prevents drawing to a closed screen
                else:
                    self.running = False




            
            self.board.draw_tiles(self.screen)# draws the tiles of the board
            self.board.draw_red_tile(self.screen, self.white_turn)# draws the red tile if the king is in check


            self.board.highlight_tile(self.input_handler.selected_index, self.screen)
            self.board.highlight_moves(self.input_handler.available_moves, self.screen)


            self.board.draw_pieces(self.screen)
            
            
            
            
            
            pygame.display.set_caption(f"Chess - {'White' if self.white_turn else 'Black'}'s Turn")
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
