from pieces.base import Piece

class King(Piece):
    def get_valid_moves(self, index, board):
        moves = []
        row, col = divmod(index, 8)
        king_moves = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0),  (1, 1)]

        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_index = r * 8 + c
                target_piece = board.board_pieces[target_index]
                if target_piece == "0" or (target_piece[0] != self.color and not board.is_king(target_piece)):
                    moves.append(target_index)

        # Castling (simplified - I already check legality elsewhere)
        if self.color == "w" and not board.white_king_moved:
            if board.board_pieces[61] == board.board_pieces[62] == "0" and not board.white_rook_moved[0]:
                moves.append(62)
            if board.board_pieces[59] == board.board_pieces[58] == board.board_pieces[57] == "0" and not board.white_rook_moved[1]:
                moves.append(58)
        elif self.color == "b" and not board.black_king_moved:
            if board.board_pieces[5] == board.board_pieces[6] == "0" and not board.black_rook_moved[0]:
                moves.append(6)
            if board.board_pieces[1] == board.board_pieces[2] == board.board_pieces[3] == "0" and not board.black_rook_moved[1]:
                moves.append(2)

        return moves
