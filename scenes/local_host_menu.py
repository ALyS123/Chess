import pygame
import sys
import os
import math
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR


class LocalHostMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Enhanced font system
        self.title_font = pygame.font.SysFont("Arial", 56, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 20)
        
        # Load and scale background with proper path handling
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
            image_path = os.path.join(base_path, "assets/images/menu_bg0.png")
            self.bg_image = pygame.image.load(image_path)
            img_width, img_height = self.bg_image.get_size()
            scale = max(WINDOW_WIDTH / img_width, WINDOW_HEIGHT / img_height)
            self.bg_image = pygame.transform.scale(self.bg_image, (int(img_width * scale), int(img_height * scale)))
            self.bg_x = (WINDOW_WIDTH - self.bg_image.get_width()) // 2
            self.bg_y = (WINDOW_HEIGHT - self.bg_image.get_height()) // 2
        except:
            # Fallback - use None to trigger gradient background
            self.bg_image = None
        
        # Enhanced color scheme (matching main menu wood/brown theme)
        self.bg_color = (40, 30, 20)
        self.accent_color = (180, 140, 100)
        self.primary_color = (120, 80, 50)
        self.hover_color = (150, 110, 70)
        self.text_color = (240, 220, 180)
        self.shadow_color = (20, 15, 10)
        
        # Animation variables
        self.time = 0
        self.button_animations = [0, 0, 0]
        self.title_glow = 0
        
        # Create overlay for better text readability over background image
        self.bg_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(WINDOW_HEIGHT):
            alpha = int(120 * (y / WINDOW_HEIGHT))
            pygame.draw.line(self.bg_overlay, (0, 0, 0, alpha), (0, y), (WINDOW_WIDTH, y))
        
        # Button configuration with enhanced properties (removed icons for compatibility)
        self.buttons = [
            {
                "text": "Host Game", 
                "rect": pygame.Rect(0, 0, 400, 80), 
                "hover": False,
                "animation": 0,
                "description": "Create a new game session"
            },
            {
                "text": "Join Game", 
                "rect": pygame.Rect(0, 0, 400, 80), 
                "hover": False,
                "animation": 0,
                "description": "Connect to an existing game"
            },
            {
                "text": "Back", 
                "rect": pygame.Rect(0, 0, 400, 80), 
                "hover": False,
                "animation": 0,
                "description": "Return to main menu"
            }
        ]
        
        # Position buttons with better spacing (increased spacing to prevent text overlap)
        total_height = len(self.buttons) * 140 - 20
        start_y = (WINDOW_HEIGHT - total_height) // 2 + 50
        for i, button in enumerate(self.buttons):
            button["rect"].center = (WINDOW_WIDTH // 2, start_y + i * 140)

    def draw_background(self):
        """Draw the background - either image or animated gradient"""
        if self.bg_image:
            # Apply subtle movement to background
            offset_x = math.sin(self.time * 0.01) * 3
            offset_y = math.cos(self.time * 0.015) * 2
            self.screen.blit(self.bg_image, (self.bg_x + offset_x, self.bg_y + offset_y))
            # Apply overlay for better text readability
            self.screen.blit(self.bg_overlay, (0, 0))
        else:
            # Fallback gradient background with wood/brown tones
            for y in range(WINDOW_HEIGHT):
                # Create a subtle animated gradient with brown tones
                wave = math.sin(self.time * 0.01 + y * 0.01) * 8
                base_brown = 40
                color_intensity = base_brown + wave
                color = (
                    max(0, min(255, int(color_intensity * 1.2))),  # More red for brown
                    max(0, min(255, int(color_intensity * 0.8))),  # Less green
                    max(0, min(255, int(color_intensity * 0.5)))   # Even less blue
                )
                pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))

    def draw_floating_particles(self):
        """Draw subtle floating particles for ambiance"""
        for i in range(20):
            x = (math.sin(self.time * 0.005 + i) * 100 + WINDOW_WIDTH // 2 + i * 40) % WINDOW_WIDTH
            y = (math.cos(self.time * 0.003 + i * 0.5) * 50 + WINDOW_HEIGHT // 2 + i * 30) % WINDOW_HEIGHT
            alpha = int(50 + 30 * math.sin(self.time * 0.01 + i))
            size = 2 + int(math.sin(self.time * 0.02 + i) * 1)
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.accent_color, alpha), (size, size), size)
            self.screen.blit(particle_surface, (x - size, y - size))

    def draw_enhanced_button(self, button, index):
        """Draw a button with enhanced visual effects"""
        rect = button["rect"]
        
        # Animation effects
        if button["hover"]:
            button["animation"] = min(1.0, button["animation"] + 0.1)
        else:
            button["animation"] = max(0.0, button["animation"] - 0.05)
        
        # Calculate animated properties
        scale = 1 + button["animation"] * 0.05
        glow_intensity = button["animation"] * 30
        
        # Create animated button rect
        animated_rect = pygame.Rect(rect)
        size_increase = int(20 * button["animation"])
        animated_rect.inflate_ip(size_increase, size_increase // 2)
        
        # Draw button shadow
        shadow_rect = animated_rect.copy()
        shadow_rect.move_ip(3, 3)
        pygame.draw.rect(self.screen, self.shadow_color, shadow_rect, border_radius=15)
        
        # Draw button glow effect
        if button["hover"]:
            glow_rect = animated_rect.copy()
            glow_rect.inflate_ip(10, 5)
            glow_color = (*self.hover_color, 50)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, glow_rect.width, glow_rect.height), border_radius=20)
            self.screen.blit(glow_surface, glow_rect)
        
        # Draw main button
        button_color = self.hover_color if button["hover"] else self.primary_color
        pygame.draw.rect(self.screen, button_color, animated_rect, border_radius=12)
        
        # Draw button border
        border_color = self.accent_color if button["hover"] else self.primary_color
        pygame.draw.rect(self.screen, border_color, animated_rect, width=2, border_radius=12)
        
        # Draw button text with shadow
        text_surface = self.button_font.render(button["text"], True, self.text_color)
        text_rect = text_surface.get_rect(center=animated_rect.center)
        
        # Text shadow
        shadow_surface = self.button_font.render(button["text"], True, self.shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(animated_rect.centerx + 2, animated_rect.centery + 2))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Main text
        self.screen.blit(text_surface, text_rect)
        
        # Draw description text for hovered button (positioned to avoid overlap)
        if button["hover"]:
            desc_surface = self.subtitle_font.render(button["description"], True, self.accent_color)
            # Position text well below the button to avoid overlap with other buttons
            desc_rect = desc_surface.get_rect(center=(animated_rect.centerx, animated_rect.bottom + 20))
            
            # Draw a subtle background for the description text
            desc_bg_rect = desc_rect.copy()
            desc_bg_rect.inflate_ip(20, 8)
            desc_bg_surface = pygame.Surface((desc_bg_rect.width, desc_bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(desc_bg_surface, (*self.shadow_color, 180), (0, 0, desc_bg_rect.width, desc_bg_rect.height), border_radius=8)
            self.screen.blit(desc_bg_surface, desc_bg_rect)
            
            self.screen.blit(desc_surface, desc_rect)

    def draw_animated_title(self):
        """Draw an animated title with glow effects in wood theme"""
        # Title glow animation
        self.title_glow = math.sin(self.time * 0.02) * 0.3 + 0.7
        
        # Main title (removed emoji for compatibility)
        title_text = "Local Multiplayer"
        title_surface = self.title_font.render(title_text, True, self.text_color)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 120))
        
        # Title glow effect with brown/gold tones
        glow_color = (*self.accent_color, int(100 * self.title_glow))
        glow_surface = pygame.Surface((title_rect.width + 20, title_rect.height + 10), pygame.SRCALPHA)
        glow_text = self.title_font.render(title_text, True, glow_color)
        glow_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
        glow_surface.blit(glow_text, glow_rect)
        
        # Apply blur effect (simplified)
        for offset in [(2, 0), (-2, 0), (0, 2), (0, -2), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            blur_rect = title_rect.copy()
            blur_rect.move_ip(*offset)
            self.screen.blit(glow_surface, (blur_rect.x - 10, blur_rect.y - 5))
        
        # Draw main title
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Connect and play with friends locally"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, self.accent_color)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, title_rect.bottom + 25))
        self.screen.blit(subtitle_surface, subtitle_rect)

    def draw_decorative_elements(self):
        """Draw decorative UI elements"""
        # Draw corner decorations
        corner_size = 40
        corner_color = (*self.accent_color, 80)
        
        # Top corners
        pygame.draw.arc(self.screen, self.accent_color, (20, 20, corner_size, corner_size), 
                       math.pi, math.pi * 1.5, 3)
        pygame.draw.arc(self.screen, self.accent_color, 
                       (WINDOW_WIDTH - corner_size - 20, 20, corner_size, corner_size), 
                       math.pi * 1.5, math.pi * 2, 3)
        
        # Bottom corners
        pygame.draw.arc(self.screen, self.accent_color, 
                       (20, WINDOW_HEIGHT - corner_size - 20, corner_size, corner_size), 
                       math.pi * 0.5, math.pi, 3)
        pygame.draw.arc(self.screen, self.accent_color, 
                       (WINDOW_WIDTH - corner_size - 20, WINDOW_HEIGHT - corner_size - 20, corner_size, corner_size), 
                       0, math.pi * 0.5, 3)

    def run(self):
        while True:
            self.time += 1
            
            # Draw background layers
            self.draw_background()
            self.draw_floating_particles()
            self.draw_decorative_elements()
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw animated title
            self.draw_animated_title()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["text"] == "Host Game":
                                return "host"
                            elif button["text"] == "Join Game":
                                return "join"
                            elif button["text"] == "Back":
                                return "menu"
            
            # Update and draw buttons
            for i, button in enumerate(self.buttons):
                button["hover"] = button["rect"].collidepoint(mouse_pos)
                self.draw_enhanced_button(button, i)
            
            # Add a subtle vignette effect
            vignette_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            for radius in range(0, min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2, 10):
                alpha = max(0, 30 - radius // 20)
                if alpha > 0:
                    pygame.draw.circle(vignette_surface, (0, 0, 0, alpha), 
                                     (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), 
                                     min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2 - radius, 10)
            self.screen.blit(vignette_surface, (0, 0))
            
            pygame.display.flip()
            self.clock.tick(60)