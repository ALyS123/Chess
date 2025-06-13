# pieces/base.py

class Piece:
    def __init__(self, color):
        self.color = color  # "w" or "b"

    def get_valid_moves(self, index, board):
        raise NotImplementedError("This should be implemented in subclasses.")
