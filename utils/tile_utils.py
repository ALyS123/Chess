# utils/tile_utils.py

from settings import ROWS, COLS, SQUARE_SIZE, MARGIN_X, MARGIN_Y

# Precompute the center position of each tile (used to blit pieces)
tile_center_position = []

for row in range(ROWS):
    for col in range(COLS):
        center_x = MARGIN_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = MARGIN_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
        tile_center_position.append((center_x - 40, center_y - 40))  # 80x80 image = offset by 40

# Optional helpers

def index_to_coords(index):
    """Given a 0-63 index, return (row, col)."""
    return divmod(index, COLS)

def coords_to_index(row, col):
    """Given row and col, return 0-63 index."""
    return row * COLS + col
