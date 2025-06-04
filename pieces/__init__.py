import pygame
import os

piece_images = {}

# Map in-code names to filenames
piece_map = {
    "wP": "whitePawn.png",
    "wR": "whiteRook.png",
    "wKnight": "whiteKnight.png",
    "wB": "whiteBishop.png",
    "wQ": "whiteQueen.png",
    "wK": "whiteKing.png",
    "bP": "blackPawn.png",
    "bR": "blackRook.png",
    "bKnight": "blackKnight.png",
    "bB": "blackBishop.png",
    "bQ": "blackQueen.png",
    "bK": "blackKing.png",
}

ASSET_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
ASSET_PATH = os.path.abspath(ASSET_PATH)

def load_images():
    for key, filename in piece_map.items():
        path = os.path.join(ASSET_PATH, filename)
        image = pygame.image.load(path)  # No scaling needed
        image = pygame.transform.scale(image, (80, 80))
        piece_images[key] = image

load_images()

