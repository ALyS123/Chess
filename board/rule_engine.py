# board/rule_engine.py

class GameRules:
    def __init__(self, board):
        self.board = board # <-- reference to Board to access board_pieces

    def get_threatened_tiles(self, by_white: bool):
        threatened = set()
        prefix = "w" if by_white else "b"
        
        for i, piece in enumerate(self.board.board_pieces):
            if piece.startswith(prefix):
                pseudo_moves = self.get_pseudo_moves(i)  # Use raw movement patterns

                threatened.update(pseudo_moves)

        return threatened

    def get_pseudo_moves(self, index):
        
        piece = self.board.board_pieces[index]  # Access the piece at the given index
        moves = []

        def add(target):
            if 0 <= target < 64:
                moves.append(target)

        if piece == "wP":
            for offset in (-9, -7):
                target = index + offset
                if 0 <= target < 64 and abs((index // 8) - (target // 8)) == 1:
                    add(target)

        elif piece == "bP":
            for offset in (7, 9):
                target = index + offset
                if 0 <= target < 64 and abs((index // 8) - (target // 8)) == 1:
                    add(target)

        elif piece in ("wKnight", "bKnight"):
            row, col = divmod(index, 8)
            knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                            (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    add(r * 8 + c)

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
                    target_piece = self.board.board_pieces[target_index]
                    moves.append(target_index)
                    if target_piece != "0":
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
                    add(r * 8 + c)

        return moves
    

    def king_in_check(self, by_white: bool):
        if by_white:
            king_index = self.board.board_pieces.index("wK")
            if king_index in self.get_threatened_tiles(not by_white):
                return True
            else:
                return False

        elif by_white is False:
            king_index = self.board.board_pieces.index("bK")
            if king_index in self.get_threatened_tiles(not by_white):
                return True
            else:
                return False
        

    def is_move_resolving_check(self, from_index, to_index, by_white: bool):
        # Simulate move
        original_from = self.board.board_pieces[from_index]
        original_to = self.board.board_pieces[to_index]

        self.board.board_pieces[to_index] = original_from
        self.board.board_pieces[from_index] = "0"

        still_in_check = self.king_in_check(by_white)

        # Revert move
        self.board.board_pieces[from_index] = original_from
        self.board.board_pieces[to_index] = original_to

        return not still_in_check
    
    def is_checkmate(self, by_white: bool):
        # If not in check, it can't be checkmate
        if not self.king_in_check(by_white):
            return False

        for i, piece in enumerate(self.board.board_pieces):
            if piece.startswith("w" if by_white else "b"):
                valid_moves = self.board.get_valid_moves(i)
                for move in valid_moves:
                    if self.is_move_resolving_check(i, move, by_white):
                        return False  # At least one move saves the king

        return True  # No move can resolve the check → checkmate
    
    def is_stalemate(self, by_white: bool):
        # If the king is in check, it's not stalemate
        if self.king_in_check(by_white):
            return False

        # Try all legal moves for this player
        for i, piece in enumerate(self.board.board_pieces):
            if piece.startswith("w" if by_white else "b"):
                valid_moves = self.board.get_valid_moves(i)
                for move in valid_moves:
                    if self.is_move_resolving_check(i, move, by_white):
                        return False  # At least one legal move exists

        return True  # No legal moves and not in check → stalemate

    def is_draw_by_insufficient_material(self):
        pieces = [p for p in self.board.board_pieces if p != "0"]

        # If only kings remain
        if all(p.endswith("K") for p in pieces):
            return True

        # King + Knight or King + Bishop
        if len(pieces) == 2:
            return any(p.endswith("K") for p in pieces) and (
                any(p.endswith("N") or p.endswith("B") for p in pieces)
            )

        return False

