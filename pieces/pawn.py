from pieces.base import Piece

class Pawn(Piece):
    def get_valid_moves(self, index, board):
        moves = []
        direction = -8 if self.color == "w" else 8
        start_row = 6 if self.color == "w" else 1

        one_step = index + direction
        if 0 <= one_step < 64 and board.board_pieces[one_step] == "0":
            moves.append(one_step)

            # Check for two-step move
            if index // 8 == start_row:
                two_step = index + 2 * direction
                if board.board_pieces[two_step] == "0":
                    moves.append(two_step)

        # Diagonal captures
        diag_offsets = (-9, -7) if self.color == "w" else (7, 9)
        for offset in diag_offsets:
            target = index + offset
            if 0 <= target < 64 and abs((index // 8) - (target // 8)) == 1:
                target_piece = board.board_pieces[target]
                if target_piece != "0" and target_piece[0] != self.color and not board.is_king(target_piece):
                    moves.append(target)

        return moves
