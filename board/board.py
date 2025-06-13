# board/board.py

import pygame
from settings import ROWS, COLS, SQUARE_SIZE, MARGIN_X, MARGIN_Y, WHITE, BROWN
from utils.tile_utils import tile_center_position
from pieces import piece_images
from board.rule_engine import GameRules
from settings import BOARD_SIZE


class Board:
    def __init__(self):
        """self.board_pieces = [
            "bR", "bKnight", "bB", "bQ", "bK", "bB", "bKnight", "bR",
            "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
            "wR", "wKnight", "wB", "wQ", "wK", "wB", "wKnight", "wR"
        ]"""

        self.board_pieces = [
            "0", "0", "0", "bQ", "bK", "0", "0", "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "wP", "wQ", "wQ", "0", "wP", "0", "0", "0",
            "0", "0", "0", "wQ", "wK", "0", "0", "0"
        ]

        self.game_rules = GameRules(self)


        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_moved = [False, False]
        self.black_rook_moved = [False, False]

        self.king_position = [None, None]  # [index of white king, index of black king]
    
    def draw_tiles(self, surface):
        # Draw the chess squares (your original code)
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BROWN
                x = MARGIN_X + col * SQUARE_SIZE
                y = MARGIN_Y + row * SQUARE_SIZE
                pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        
        # Draw algebraic notation (letters and numbers)
        font = pygame.font.Font(None, 24)
        
        # Draw file letters (a-h) at the bottom
        for col in range(COLS):
            letter = chr(ord('a') + col)
            text = font.render(letter, True, (200, 200, 200))
            x = MARGIN_X + col * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2
            y = MARGIN_Y + BOARD_SIZE + 5
            surface.blit(text, (x, y))
        
        # Draw rank numbers (1-8) on the right side
        for row in range(ROWS):
            number = str(8 - row)  # Chess ranks go from 8 at top to 1 at bottom
            text = font.render(number, True, (200, 200, 200))
            x = MARGIN_X + BOARD_SIZE + 5
            y = MARGIN_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2
            surface.blit(text, (x, y))

    
    def draw_red_tile(self, surface, white_turn):
        if self.game_rules.king_in_check(white_turn):
            king_piece = "wK" if white_turn else "bK"
            try:
                king_index = self.board_pieces.index(king_piece)
                row = king_index // 8
                col = king_index % 8
                x = MARGIN_X + col * SQUARE_SIZE
                y = MARGIN_Y + row * SQUARE_SIZE

                red_overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 120))  # Red with transparency
                surface.blit(red_overlay, (x, y))
            except ValueError:
                print("King piece not found on the board.")
                pass  # King not found — avoid crashing

    def draw_pieces(self, surface):
        for i in range(64):
            piece = self.board_pieces[i]
            if piece != "0":
                surface.blit(piece_images[piece], tile_center_position[i])

    def highlight_tile(self, index, surface):
        from settings import HIGHLIGHT
        if index is None:
            return
        row = index // 8
        col = index % 8
        x = MARGIN_X + col * SQUARE_SIZE
        y = MARGIN_Y + row * SQUARE_SIZE
        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        highlight_surface.fill((*HIGHLIGHT, 100))
        surface.blit(highlight_surface, (x, y))

    def is_king(self, piece):
        return piece in ("wK", "bK")

    def get_valid_moves(self, index, ignore_check=False):
        piece = self.board_pieces[index]
        if piece == "0":
            return []

        color = piece[0]

        from pieces.pawn import Pawn
        from pieces.knight import Knight
        from pieces.bishop import Bishop
        from pieces.rook import Rook
        from pieces.queen import Queen
        from pieces.king import King

        piece_type = piece[1:]
        mapping = {
            "P": Pawn,
            "Knight": Knight,
            "B": Bishop,
            "R": Rook,
            "Q": Queen,
            "K": King,
        }

        PieceClass = mapping.get(piece_type)
        if not PieceClass:
            return []

        handler = PieceClass(color)
        moves = handler.get_valid_moves(index, self)

        # If the selected piece is a king, remove moves that land on threatened tiles
        if piece == "wK":
            moves = [m for m in moves if m not in self.game_rules.get_threatened_tiles(by_white=False)]
        elif piece == "bK":
            moves = [m for m in moves if m not in self.game_rules.get_threatened_tiles(by_white=True)]

        return moves


    def highlight_moves(self, move_indices, surface):
        from settings import HIGHLIGHT
        for index in move_indices:
            row = index // 8
            col = index % 8
            x = MARGIN_X + col * SQUARE_SIZE
            y = MARGIN_Y + row * SQUARE_SIZE
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill((*HIGHLIGHT, 80))
            surface.blit(highlight_surface, (x, y))

    def move_piece(self, from_index, to_index):
        piece = self.board_pieces[from_index]
        self.board_pieces[to_index] = piece
        self.board_pieces[from_index] = "0"

        if piece == "wK":
            self.white_king_moved = True
            if from_index == 60 and to_index == 62:
                self.board_pieces[63] = "0"
                self.board_pieces[61] = "wR"
            elif from_index == 60 and to_index == 58:
                self.board_pieces[56] = "0"
                self.board_pieces[59] = "wR"
        elif piece == "bK":
            self.black_king_moved = True
            if from_index == 4 and to_index == 6:
                self.board_pieces[7] = "0"
                self.board_pieces[5] = "bR"
            elif from_index == 4 and to_index == 2:
                self.board_pieces[0] = "0"
                self.board_pieces[3] = "bR"

        if piece == "wR":
            if from_index == 63:
                self.white_rook_moved[0] = True
            elif from_index == 56:
                self.white_rook_moved[1] = True
        elif piece == "bR":
            if from_index == 7:
                self.black_rook_moved[0] = True
            elif from_index == 0:
                self.black_rook_moved[1] = True

        # Handle pawn promotion to queen
        if piece == "wP" and to_index // 8 == 0:
            self.board_pieces[to_index] = "wQ"
        elif piece == "bP" and to_index // 8 == 7:
            self.board_pieces[to_index] = "bQ"

