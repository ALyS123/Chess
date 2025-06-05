# Chess

A simple chess game built with Python and [pygame](https://www.pygame.org/).

## Features

- 8×8 board with piece images
- Highlights the selected square and all valid moves
- Basic castling and pawn promotion
- Uses settings in `settings.py` for window size and colours

## Requirements

- Python 3.10+
- `pygame` library (`pip install pygame`)

## Running

From the repository root run:

```bash
python main.py
```

Click a piece to select it and view its legal moves. Click again on one of the
highlighted squares to move. Close the window or press <kbd>Esc</kbd> to exit.

## Repository layout

- `board/` contains board representation and movement rules
- `core/` holds input handling code
- `pieces/` loads chess piece images from `assets/images`
- `scenes/` contains placeholder modules for menus and game scenes
- `utils/` helper functions
- `settings.py` configuration constants

This code base is a work in progress and currently does not implement every
rule of chess or AI opponents, but it provides a starting point for a Pygame
chess project.