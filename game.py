# game.py

import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, FPS
from board.board import Board
from core.input_handler import InputHandler
from board.util import util



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
        self.util = util(self.board)  # Initialize util with the board reference
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
            self.king_in_check = self.util.king_in_check(self.white_turn)  # True if the king is in check False if not 
            # Check for checkmate
            if self.util.is_checkmate(self.white_turn):
                print(f"Checkmate! {'Black' if self.white_turn else 'White'} wins.")
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
