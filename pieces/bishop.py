from pieces.base import Piece

class Bishop(Piece):
    def get_valid_moves(self, index, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        row, col = divmod(index, 8)

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_index = r * 8 + c
                target_piece = board.board_pieces[target_index]

                if target_piece == "0":
                    moves.append(target_index)
                elif target_piece[0] != self.color and not board.is_king(target_piece):
                    moves.append(target_index)
                    break
                else:
                    break

                r += dr
                c += dc

        return moves
