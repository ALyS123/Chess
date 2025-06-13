import pygame
import sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.SysFont("Arial", 48)
        self.button_font = pygame.font.SysFont("Arial", 32)
        self.bg_image = pygame.image.load("assets/images/menu_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Button labels
        button_texts = ["1v1 (Offline)", "1v1 (Online) Coming Soon", "1 v Bot Coming Soon", "Quit"]
        self.buttons = []

        # Dynamically size and center each button, starting a bit lower
        for i, text in enumerate(button_texts):
            label = self.button_font.render(text, True, (255, 255, 255))
            width = label.get_width() + 30  # Padding
            height = 50
            x = (WINDOW_WIDTH - width) // 2
            y = 340 + i * 70  # Lower starting position
            self.buttons.append({"text": text, "rect": pygame.Rect(x, y, width, height)})

    def run(self):
        while True:
            self.screen.blit(self.bg_image, (0, 0))

            # Draw buttons
            for button in self.buttons:
                pygame.draw.rect(self.screen, (100, 100, 100), button["rect"])
                label = self.button_font.render(button["text"], True, (255, 255, 255))
                self.screen.blit(
                    label,
                    (
                        button["rect"].x + (button["rect"].width - label.get_width()) // 2,
                        button["rect"].y + (button["rect"].height - label.get_height()) // 2
                    )
                )

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["text"] in ["1v1 (Offline)", "1v1 (Online)", "1 v Bot"]:
                                self.fade_out()
                                return button["text"]  # Return selected mode string
                            elif button["text"] == "Quit":
                                pygame.quit()
                                sys.exit()

            pygame.display.flip()

    def fade_out(self):
        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255, 8):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(15)
