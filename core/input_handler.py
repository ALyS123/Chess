# core/input_handler.py

import pygame
from settings import MARGIN_X, MARGIN_Y, BOARD_SIZE, SQUARE_SIZE, COLS

class InputHandler:
    def __init__(self, board, game):
        self.board = board
        self.game = game  # <- reference to Game to access white_turn
        self.selected_index = None  # First click index
        self.available_moves = []   # Will be set after first click

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            index = self.get_tile_index(event.pos)
            if index is None:
                return

            piece = self.board.board_pieces[index]
            current_turn_prefix = "w" if self.game.white_turn else "b"

            if self.selected_index is None:
                # First click: select only own piece
                if piece != "0" and piece.startswith(current_turn_prefix):
                    self.selected_index = index
                    self.available_moves = self.board.get_valid_moves(index)
                    print(f"First click: {self.selected_index}")
                    print(f"Available moves: {self.available_moves}")
            else:
                if index == self.selected_index:
                    # Deselect
                    print(f"Deselected: {index}")
                    self.selected_index = None
                    self.available_moves = []
                elif index in self.available_moves:
                    # Move piece
                    self.board.move_piece(self.selected_index, index)
                    print(f"Moved from {self.selected_index} to {index}")
                    self.selected_index = None
                    self.available_moves = []
                    self.game.white_turn = not self.game.white_turn  # 🔁 Switch turn
                else:
                    # Clicked a new tile, check if it’s your own piece
                    if piece != "0" and piece.startswith(current_turn_prefix):
                        print(f"Switched selection to: {index}")
                        self.selected_index = index
                        self.available_moves = self.board.get_valid_moves(index)
                        print(f"Available moves: {self.available_moves}")




    def get_tile_index(self, position):
        x, y = position
        x -= MARGIN_X
        y -= MARGIN_Y

        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            return row * COLS + col
        return None
