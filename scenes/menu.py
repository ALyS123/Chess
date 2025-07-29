import pygame
import sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR
import random
import math
import os
from scenes.local_host_menu import LocalHostMenu

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = pygame.time.Clock()

        self.button_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24)

        # Load and properly scale background image
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
        image_path = os.path.join(base_path, "assets/images/menu_bg0.png")
        self.bg_image = pygame.image.load(image_path)

        # Calculate scaling to cover the entire window while maintaining aspect ratio
        img_width, img_height = self.bg_image.get_size()
        scale_x = WINDOW_WIDTH / img_width
        scale_y = WINDOW_HEIGHT / img_height
        scale = max(scale_x, scale_y)  # Use max to cover entire window
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        self.bg_image = pygame.transform.scale(self.bg_image, (new_width, new_height))
        
        # Calculate centering offsets
        self.bg_x = (WINDOW_WIDTH - new_width) // 2
        self.bg_y = (WINDOW_HEIGHT - new_height) // 2

        # Create warm wood-toned overlay for better text readability
        self.bg_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(WINDOW_HEIGHT):
            alpha = int(60 * (y / WINDOW_HEIGHT))  # Gradient from transparent to semi-transparent
            pygame.draw.line(self.bg_overlay, (20, 15, 10, alpha), (0, y), (WINDOW_WIDTH, y))

        # Warm wood/brown color palette
        self.primary_color = (180, 140, 100)     # Golden brown
        self.secondary_color = (150, 110, 70)    # Medium brown
        self.accent_color = (220, 180, 120)      # Light golden
        self.bg_color = (40, 30, 20)            # Dark brown
        self.hover_color = (200, 160, 110)      # Warm hover
        self.text_color = (240, 220, 180)       # Cream
        self.shadow_color = (20, 15, 10)        # Dark shadow

        self.time = 0
        self.particles = []
        self.selected_button = None

        # Create warm floating dust particles instead of neon ones
        for _ in range(40):
            self.particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'speed': random.uniform(0.2, 0.8),
                'size': random.randint(1, 3),
                'color': random.choice([self.primary_color, self.secondary_color, self.accent_color]),
                'pulse_offset': random.uniform(0, math.pi * 2),
                'drift_speed': random.uniform(0.05, 0.3),
                'alpha': random.randint(30, 80)
            })

        # Game title
        self.title_text = "CHESS MASTER"
        self.subtitle_text = "The Ultimate Strategy Game"

        # Button configuration
        button_texts = ["1v1 (Offline)", "Local Host", "1v1 (Online) Coming Soon", "1 v Bot Coming Soon", "Quit"]
        self.buttons = []

        # Calculate button layout - make buttons wider for longer text
        button_width = 480
        button_height = 70
        total_height = len(button_texts) * button_height + (len(button_texts) - 1) * 20
        start_y = (WINDOW_HEIGHT - total_height) // 2 + 100

        for i, text in enumerate(button_texts):
            enabled = text == "1v1 (Offline)" or text == "Local Host" or text == "Quit"
            x = (WINDOW_WIDTH - button_width) // 2
            y = start_y + i * (button_height + 20)

            button_data = {
                "text": text,
                "rect": pygame.Rect(x, y, button_width, button_height),
                "enabled": enabled,
                "hover": False,
                "glow_intensity": 0,
                "pulse": 0,
                "original_y": y,
                "animation": 0
            }
            self.buttons.append(button_data)

    def draw_wood_grain_border(self, rect, color, thickness=3):
        """Draw a wooden-style border with subtle texture"""
        # Main border
        pygame.draw.rect(self.screen, color, rect, thickness, border_radius=8)
        
        # Inner highlight for wood effect
        inner_rect = rect.inflate(-thickness*2, -thickness*2)
        highlight_color = tuple(min(255, c + 30) for c in color)
        pygame.draw.rect(self.screen, highlight_color, inner_rect, 1, border_radius=6)

    def draw_warm_glow(self, rect, color, intensity=1.0):
        """Draw a warm, subtle glow effect"""
        glow_size = int(15 * intensity)
        for i in range(glow_size, 0, -1):
            alpha = int(20 * intensity * (i / glow_size))
            glow_rect = rect.inflate(i * 2, i * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*color, alpha), (0, 0, glow_rect.width, glow_rect.height), border_radius=12)
            self.screen.blit(glow_surface, glow_rect.topleft)

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.time += dt * 0.001
            mouse_pos = pygame.mouse.get_pos()

            # Draw background
            self.screen.fill(self.bg_color)
            self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))
            self.screen.blit(self.bg_overlay, (0, 0))

            # Update and draw warm dust particles
            for particle in self.particles:
                # Update position
                particle['y'] -= particle['speed']
                if particle['y'] < -10:
                    particle['y'] = WINDOW_HEIGHT + 10
                    particle['x'] = random.randint(0, WINDOW_WIDTH)
                
                # Add gentle drift movement
                particle['x'] += math.sin(self.time * particle['drift_speed'] + particle['pulse_offset']) * 0.3
                
                # Gentle pulse effect
                pulse = math.sin(self.time * 2 + particle['pulse_offset']) * 0.3 + 0.7
                current_size = particle['size'] * pulse
                
                # Draw particle with warm glow
                if current_size > 0:
                    particle_surface = pygame.Surface((int(current_size * 4), int(current_size * 4)), pygame.SRCALPHA)
                    center = (int(current_size * 2), int(current_size * 2))
                    
                    # Soft outer glow
                    pygame.draw.circle(particle_surface, (*particle['color'], particle['alpha'] // 3), 
                                     center, int(current_size * 2))
                    # Bright center
                    pygame.draw.circle(particle_surface, (*particle['color'], particle['alpha']), 
                                     center, max(1, int(current_size)))
                    
                    self.screen.blit(particle_surface, (particle['x'] - current_size * 2, particle['y'] - current_size * 2))

            # Draw title with warm glow
            title_y = 80
            title_surface = self.title_font.render(self.title_text, True, self.text_color)
            title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, title_y))
            
            # Title warm glow effect (much subtler than neon)
            glow_intensity = math.sin(self.time * 2) * 0.3 + 0.7
            for i in range(3, 0, -1):
                glow_surface = self.title_font.render(self.title_text, True, (*self.accent_color, int(50 * glow_intensity)))
                glow_rect = title_rect.copy()
                glow_rect.x += i
                glow_rect.y += i
                self.screen.blit(glow_surface, glow_rect)
            
            self.screen.blit(title_surface, title_rect)
            
            # Draw subtitle
            subtitle_surface = self.subtitle_font.render(self.subtitle_text, True, self.secondary_color)
            subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, title_y + 60))
            self.screen.blit(subtitle_surface, subtitle_rect)

            # Update and draw buttons
            for i, button in enumerate(self.buttons):
                button["hover"] = button["rect"].collidepoint(mouse_pos) and button["enabled"]
                
                # Update effects
                if button["hover"]:
                    button["animation"] = min(1.0, button["animation"] + 0.08)
                    button["pulse"] = math.sin(self.time * 6) * 2
                else:
                    button["animation"] = max(0.0, button["animation"] - 0.05)
                    button["pulse"] = 0

                button_rect = button["rect"].copy()
                button_rect.y = button["original_y"] + int(button["pulse"])

                # Scale effect for hover
                if button["animation"] > 0:
                    scale_increase = int(10 * button["animation"])
                    button_rect.inflate_ip(scale_increase, scale_increase // 2)

                # Button colors
                if not button["enabled"]:
                    bg_color = (60, 45, 35, 120)
                    border_color = (80, 60, 45)
                    text_color = (120, 100, 80)
                elif button["hover"]:
                    bg_color = (*self.hover_color, 180)
                    border_color = self.hover_color
                    text_color = (40, 30, 20)
                else:
                    bg_color = (*self.primary_color, 100)
                    border_color = self.primary_color
                    text_color = self.text_color

                # Draw button warm glow for hover
                if button["hover"]:
                    self.draw_warm_glow(button_rect, border_color, button["animation"])

                # Draw button shadow
                shadow_rect = button_rect.copy()
                shadow_rect.move_ip(3, 3)
                shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(shadow_surface, (*self.shadow_color, 100), (0, 0, shadow_rect.width, shadow_rect.height), border_radius=8)
                self.screen.blit(shadow_surface, shadow_rect)

                # Draw button background
                button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(button_surface, bg_color, (0, 0, button_rect.width, button_rect.height), border_radius=8)
                self.screen.blit(button_surface, button_rect.topleft)

                # Draw wooden border
                self.draw_wood_grain_border(button_rect, border_color, 3)

                # Draw wood grain texture for enabled buttons
                if button["enabled"]:
                    # Subtle horizontal lines to simulate wood grain
                    for y_offset in range(0, button_rect.height, 8):
                        y_pos = button_rect.top + y_offset
                        alpha = 30 + int(20 * math.sin(self.time * 2 + y_offset * 0.1))
                        grain_color = (*border_color, alpha)
                        grain_surface = pygame.Surface((button_rect.width - 10, 1), pygame.SRCALPHA)
                        grain_surface.fill(grain_color)
                        self.screen.blit(grain_surface, (button_rect.left + 5, y_pos))

                # Draw button text with proper sizing
                label = self.button_font.render(button["text"], True, text_color)
                label_rect = label.get_rect(center=button_rect.center)
                
                # Ensure text fits within button bounds
                if label_rect.width > button_rect.width - 20:
                    # Use smaller font if text is too wide
                    smaller_font = pygame.font.SysFont("Arial", 28, bold=True)
                    label = smaller_font.render(button["text"], True, text_color)
                    label_rect = label.get_rect(center=button_rect.center)
                
                # Text shadow for depth
                shadow_label = self.button_font.render(button["text"], True, self.shadow_color)
                if label_rect.width > button_rect.width - 20:
                    shadow_label = smaller_font.render(button["text"], True, self.shadow_color)
                shadow_rect = shadow_label.get_rect(center=(button_rect.centerx + 1, button_rect.centery + 1))
                self.screen.blit(shadow_label, shadow_rect)
                self.screen.blit(label, label_rect)

                # Subtle shine effect for disabled buttons (instead of holographic)
                if not button["enabled"]:
                    shine_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
                    for y in range(0, button_rect.height, 6):
                        alpha = int(abs(math.sin(self.time * 1.5 + y * 0.1)) * 25)
                        pygame.draw.line(shine_surface, (255, 255, 255, alpha), 
                                       (5, y), (button_rect.width - 5, y), 1)
                    self.screen.blit(shine_surface, button_rect.topleft)

            # Draw warm corner decorations (wood-style instead of cyberpunk)
            corner_size = 50
            corner_color = self.accent_color
            
            # Top-left corner
            pygame.draw.lines(self.screen, corner_color, False, 
                            [(20, 20 + corner_size), (20, 20), (20 + corner_size, 20)], 4)
            # Top-right corner  
            pygame.draw.lines(self.screen, corner_color, False,
                            [(WINDOW_WIDTH - 20 - corner_size, 20), (WINDOW_WIDTH - 20, 20), 
                             (WINDOW_WIDTH - 20, 20 + corner_size)], 4)
            # Bottom-left corner
            pygame.draw.lines(self.screen, corner_color, False,
                            [(20, WINDOW_HEIGHT - 20 - corner_size), (20, WINDOW_HEIGHT - 20), 
                             (20 + corner_size, WINDOW_HEIGHT - 20)], 4)
            # Bottom-right corner
            pygame.draw.lines(self.screen, corner_color, False,
                            [(WINDOW_WIDTH - 20 - corner_size, WINDOW_HEIGHT - 20), 
                             (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20), 
                             (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20 - corner_size)], 4)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos) and button["enabled"]:
                            if button["text"] == "1v1 (Offline)":
                                self.fade_out()
                                return "offline"
                            
                            elif button["text"] == "Local Host":
                                local_menu = LocalHostMenu(self.screen)
                                choice = local_menu.run()
                                return choice
    
                            elif button["text"] == "Quit":
                                pygame.quit()
                                sys.exit()
                                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    def fade_out(self):
        """Warm, wood-themed fade out effect instead of cyberpunk glitch"""
        warm_colors = [
            (180, 140, 100),  # Golden brown
            (150, 110, 70),   # Medium brown  
            (220, 180, 120),  # Light golden
            (200, 160, 110),  # Warm brown
            (240, 200, 140),  # Cream
            (160, 120, 80),   # Dark golden
        ]
        
        # Create surfaces with proper alpha support
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Capture the original screen
        original_screen = self.screen.copy()
        
        total_frames = 60
        
        for frame in range(total_frames):
            progress = frame / total_frames
            
            # Start with original screen
            self.screen.blit(original_screen, (0, 0))
            
            # === PHASE 1: WARM PARTICLES (0-40%) ===
            if progress < 0.4:
                particle_intensity = progress / 0.4
                for _ in range(int(particle_intensity * 100)):
                    x = random.randint(0, WINDOW_WIDTH - 1)
                    y = random.randint(0, WINDOW_HEIGHT - 1)
                    color = random.choice(warm_colors)
                    size = random.randint(1, 4)
                    alpha = int(particle_intensity * 150)
                    
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (*color, alpha), (size, size), size)
                    self.screen.blit(particle_surface, (x - size, y - size))
            
            # === PHASE 2: GENTLE BLUR (30-70%) ===
            if 0.3 < progress < 0.7:
                blur_intensity = (progress - 0.3) / 0.4
                
                # Create gentle blur by layering offset copies
                blur_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                for offset in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]:
                    offset_x, offset_y = offset
                    alpha = int(30 * blur_intensity)
                    blur_surface.set_alpha(alpha)
                    blur_surface.blit(original_screen, (offset_x, offset_y))
                    self.screen.blit(blur_surface, (0, 0))
            
            # === PHASE 3: WARM VIGNETTE (50-100%) ===
            if progress > 0.5:
                vignette_intensity = (progress - 0.5) / 0.5
                
                # Create warm vignette
                vignette_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
                max_radius = max(WINDOW_WIDTH, WINDOW_HEIGHT) // 2
                
                for radius in range(0, max_radius, 5):
                    alpha = int(vignette_intensity * (radius / max_radius) * 200)
                    color = (*warm_colors[0], min(255, alpha))
                    pygame.draw.circle(vignette_surface, color, (center_x, center_y), max_radius - radius, 5)
                
                self.screen.blit(vignette_surface, (0, 0))
            
            # === PHASE 4: FINAL DISSOLVE (70-100%) ===
            if progress > 0.7:
                dissolve_intensity = (progress - 0.7) / 0.3
                
                # Create dissolving effect with warm particles
                for _ in range(int(dissolve_intensity * 200)):
                    x = random.randint(0, WINDOW_WIDTH)
                    y = random.randint(0, WINDOW_HEIGHT)
                    color = random.choice(warm_colors)
                    size = random.randint(2, 6)
                    alpha = int((1 - progress) * 255)
                    
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (*color, alpha), (size, size), size)
                    self.screen.blit(particle_surface, (x - size, y - size))
            
            # === OVERALL DARKENING ===
            darken_alpha = int(progress * 180)
            darken_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            darken_surface.fill((20, 15, 10, darken_alpha))
            self.screen.blit(darken_surface, (0, 0))
            
            pygame.display.flip()
            pygame.time.delay(25)
        
        # === FINAL WARM FLASH ===
        flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        flash_surface.fill((240, 220, 180))  # Warm cream color
        self.screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(50)