from pieces.base import Piece

class Knight(Piece):
    def get_valid_moves(self, index, board):
        moves = []
        row, col = divmod(index, 8)
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_index = r * 8 + c
                target_piece = board.board_pieces[target_index]
                if target_piece == "0" or (target_piece[0] != self.color and not board.is_king(target_piece)):
                    moves.append(target_index)

        return moves
