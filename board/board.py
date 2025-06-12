# board/board.py

import pygame
from settings import ROWS, COLS, SQUARE_SIZE, MARGIN_X, MARGIN_Y, WHITE, BROWN
from utils.tile_utils import tile_center_position
from pieces import piece_images
from board.util import util


class Board:
    def __init__(self):
        self.board_pieces = [
            "bR", "bKnight", "bB", "bQ", "bK", "bB", "bKnight", "bR",
            "bP", "wP", "bP", "bP", "bP", "bP", "bP", "bP",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP",
            "wR", "wKnight", "wB", "wQ", "wK", "wB", "wKnight", "wR"
        ]

        """self.board_pieces = [
            "0", "0", "0", "bQ", "bK", "0", "0", "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0",  "0",  "0",  "0",  "0",  "0",  "0",  "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
            "0", "0", "0", "wQ", "wK", "0", "0", "0"
        ]"""





        self.util = util(self)


        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_moved = [False, False]
        self.black_rook_moved = [False, False]

        self.king_position = [None, None]  # [index of white king, index of black king]


    def draw_tiles(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BROWN
                x = MARGIN_X + col * SQUARE_SIZE
                y = MARGIN_Y + row * SQUARE_SIZE
                pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    
    def draw_red_tile(self, surface, white_turn):
        if self.util.king_in_check(white_turn):
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
        moves = []
        piece = self.board_pieces[index]
        ally_prefix = piece[0] if piece != "0" else None

        def add_move(target_index):
            target_piece = self.board_pieces[target_index]
            if target_piece == "0":
                moves.append(target_index)
            elif not target_piece.startswith(ally_prefix) and not self.is_king(target_piece):
                moves.append(target_index)

        if piece == "wP":
            one_step = index - 8
            if 0 <= one_step < 64 and self.board_pieces[one_step] == "0":
                moves.append(one_step)
                if 48 <= index <= 55:
                    two_step = index - 16
                    if self.board_pieces[two_step] == "0":
                        moves.append(two_step)
            for offset in (-9, -7):
                target = index + offset
                if 0 <= target < 64 and abs((index // 8) - (target // 8)) == 1:
                    if self.board_pieces[target].startswith("b") and not self.is_king(self.board_pieces[target]):
                        moves.append(target)

        elif piece == "bP":
            one_step = index + 8
            if 0 <= one_step < 64 and self.board_pieces[one_step] == "0":
                moves.append(one_step)
                if 8 <= index <= 15:
                    two_step = index + 16
                    if self.board_pieces[two_step] == "0":
                        moves.append(two_step)
            for offset in (7, 9):
                target = index + offset
                if 0 <= target < 64 and abs((index // 8) - (target // 8)) == 1:
                    if self.board_pieces[target].startswith("w") and not self.is_king(self.board_pieces[target]):
                        moves.append(target)

        elif piece in ("wKnight", "bKnight"):
            row, col = divmod(index, 8)
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                            (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    add_move(r * 8 + c)

        elif piece in ("wR", "bR", "wB", "bB", "wQ", "bQ"):
            directions = []
            if piece[1] == "R" or piece[1] == "Q":
                directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if piece[1] == "B" or piece[1] == "Q":
                directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            row, col = divmod(index, 8)
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    target_index = r * 8 + c
                    target_piece = self.board_pieces[target_index]
                    if target_piece == "0":
                        moves.append(target_index)
                    elif not target_piece.startswith(ally_prefix) and not self.is_king(target_piece):
                        moves.append(target_index)
                        break
                    else:
                        break
                    r += dr
                    c += dc

        elif piece in ("wK", "bK"):
            row, col = divmod(index, 8)
            king_moves = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1),          (0, 1),
                          (1, -1), (1, 0),  (1, 1)]
            for dr, dc in king_moves:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    add_move(r * 8 + c)

            if piece == "wK" and not self.white_king_moved:
                if self.board_pieces[61] == self.board_pieces[62] == "0" and not self.white_rook_moved[0]:
                    moves.append(62)
                if self.board_pieces[59] == self.board_pieces[58] == self.board_pieces[57] == "0" and not self.white_rook_moved[1]:
                    moves.append(58)
            elif piece == "bK" and not self.black_king_moved:
                if self.board_pieces[5] == self.board_pieces[6] == "0" and not self.black_rook_moved[0]:
                    moves.append(6)
                if self.board_pieces[1] == self.board_pieces[2] == self.board_pieces[3] == "0" and not self.black_rook_moved[1]:
                    moves.append(2)

        
        if (self.board_pieces[index].startswith("w")) and self.board_pieces[index] == "wK":
            # by_white is True here, but we want to check what black can threaten so we pass by_white=False

            var = self.util.get_threatened_tiles(by_white=False) # call the util object method
            # var stores true / false.

            #print(f"threatened tiles: {var}")
            moves = [m for m in moves if m not in var] # removes the threatened tiles from the moves list

        elif (self.board_pieces[index].startswith("b")) and self.board_pieces[index] == "bK":
            # by_white is False here, but we want to check what white can threaten so we pass by_white=True

            var = self.util.get_threatened_tiles(by_white=True)

            #print(f"threatened tiles: {var}")
            moves = [m for m in moves if m not in var]

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

