import pygame
import sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR
import random
import math
import os

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = pygame.time.Clock()

        self.button_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24)

        # Load and properly scale background image
        #self.bg_image = pygame.image.load("assets/images/menu_bg0.png")
        
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

        # Create gradient overlay for better text readability
        self.bg_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for y in range(WINDOW_HEIGHT):
            alpha = int(80 * (y / WINDOW_HEIGHT))  # Gradient from transparent to semi-transparent
            pygame.draw.line(self.bg_overlay, (0, 0, 0, alpha), (0, y), (WINDOW_WIDTH, y))

        # Enhanced color palette
        self.primary_color = (0, 255, 255)      # Cyan
        self.secondary_color = (255, 20, 147)   # Deep Pink
        self.accent_color = (255, 215, 0)       # Gold
        self.bg_color = (20, 20, 40)
        self.hover_color = (100, 255, 255)
        self.neon_purple = (138, 43, 226)
        self.neon_green = (50, 205, 50)

        self.time = 0
        self.particles = []
        self.selected_button = None

        # Create more dynamic particles
        for _ in range(80):
            self.particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'speed': random.uniform(0.3, 1.5),
                'size': random.randint(1, 4),
                'color': random.choice([self.primary_color, self.secondary_color, self.accent_color, self.neon_purple, self.neon_green]),
                'pulse_offset': random.uniform(0, math.pi * 2),
                'drift_speed': random.uniform(0.1, 0.5)
            })

        # Game title
        self.title_text = "CHESS MASTER"
        self.subtitle_text = "The Ultimate Strategy Game"

        # Button configuration
        button_texts = ["1v1 (Offline)", "Local Host" , "1v1 (Online) Coming Soon", "1 v Bot Coming Soon", "Quit"]
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
                "scan_line": 0
            }
            self.buttons.append(button_data)

    def draw_glitch_text(self, text, font, x, y, main_color, offset=2):
        """Draw text with cyberpunk glitch effect"""
        # Draw background layers for glitch effect
        glitch_colors = [(255, 0, 0, 100), (0, 255, 0, 100), (0, 0, 255, 100)]
        offsets = [(-offset, -1), (offset, 1), (-1, offset)]
        
        for i, (color, (dx, dy)) in enumerate(zip(glitch_colors, offsets)):
            if random.random() > 0.7:  # Random glitch appearance
                glitch_surface = font.render(text, True, color[:3])
                glitch_surface.set_alpha(color[3])
                self.screen.blit(glitch_surface, (x + dx, y + dy))
        
        # Draw main text
        main_surface = font.render(text, True, main_color)
        self.screen.blit(main_surface, (x, y))

    def draw_neon_border(self, rect, color, thickness=3, glow_size=10):
        """Draw a glowing neon border"""
        # Outer glow
        for i in range(glow_size, 0, -1):
            alpha = int(50 * (i / glow_size))
            glow_rect = rect.inflate(i * 2, i * 2)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*color, alpha), (0, 0, glow_rect.width, glow_rect.height), border_radius=15)
            self.screen.blit(glow_surface, glow_rect.topleft)
        
        # Main border
        pygame.draw.rect(self.screen, color, rect, thickness, border_radius=10)

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.time += dt * 0.001
            mouse_pos = pygame.mouse.get_pos()

            # Draw background
            self.screen.fill(self.bg_color)
            self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))
            self.screen.blit(self.bg_overlay, (0, 0))

            # Update and draw particles
            for particle in self.particles:
                # Update position
                particle['y'] -= particle['speed']
                if particle['y'] < -10:
                    particle['y'] = WINDOW_HEIGHT + 10
                    particle['x'] = random.randint(0, WINDOW_WIDTH)
                
                # Add drift movement
                particle['x'] += math.sin(self.time * particle['drift_speed'] + particle['pulse_offset']) * 0.5
                
                # Pulse effect
                pulse = math.sin(self.time * 3 + particle['pulse_offset']) * 0.5 + 0.5
                current_size = particle['size'] * (0.5 + pulse * 0.5)
                
                # Draw particle with glow
                glow_size = int(current_size + 3)
                glow_surface = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
                
                # Outer glow
                pygame.draw.circle(glow_surface, (*particle['color'], 30), 
                                 (glow_size * 2, glow_size * 2), glow_size * 2)
                # Inner bright core
                pygame.draw.circle(glow_surface, (*particle['color'], int(200 * pulse)), 
                                 (glow_size * 2, glow_size * 2), int(current_size))
                
                self.screen.blit(glow_surface, (particle['x'] - glow_size * 2, particle['y'] - glow_size * 2))

            # Draw title
            title_y = 80
            title_surface = self.title_font.render(self.title_text, True, self.primary_color)
            title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, title_y))
            
            # Title glow effect
            for i in range(5, 0, -1):
                glow_surface = self.title_font.render(self.title_text, True, (*self.primary_color, 50))
                glow_rect = title_rect.copy()
                glow_rect.x += random.randint(-i, i)
                glow_rect.y += random.randint(-i, i)
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
                    button["glow_intensity"] = min(255, button["glow_intensity"] + 8)
                    button["pulse"] = math.sin(self.time * 8) * 3
                else:
                    button["glow_intensity"] = max(0, button["glow_intensity"] - 12)
                    button["pulse"] = 0

                # Update scan line for enabled buttons
                if button["enabled"]:
                    button["scan_line"] = (button["scan_line"] + 2) % button["rect"].height

                button_rect = button["rect"].copy()
                button_rect.y = button["original_y"] + int(button["pulse"])

                # Button colors
                if not button["enabled"]:
                    bg_color = (40, 40, 60, 150)
                    border_color = (100, 100, 120)
                    text_color = (120, 120, 140)
                elif button["hover"]:
                    bg_color = (*self.hover_color, 120)
                    border_color = self.hover_color
                    text_color = (0, 0, 0)
                else:
                    bg_color = (*self.primary_color, 30)
                    border_color = self.primary_color
                    text_color = (255, 255, 255)

                # Draw button glow
                if button["glow_intensity"] > 0:
                    self.draw_neon_border(button_rect, border_color, 2, int(button["glow_intensity"] / 20))

                # Draw button background
                button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(button_surface, bg_color, (0, 0, button_rect.width, button_rect.height), border_radius=10)
                self.screen.blit(button_surface, button_rect.topleft)

                # Draw button border
                pygame.draw.rect(self.screen, border_color, button_rect, width=3, border_radius=10)

                # Draw scanning line for enabled buttons
                if button["enabled"] and not button["hover"]:
                    scan_y = button_rect.top + button["scan_line"]
                    scan_color = (*border_color, 100)
                    scan_surface = pygame.Surface((button_rect.width, 2), pygame.SRCALPHA)
                    scan_surface.fill(scan_color)
                    self.screen.blit(scan_surface, (button_rect.left, scan_y))

                # Draw button text with proper sizing
                if button["enabled"] and button["hover"]:
                    # For hovered buttons, use regular text (no glitch effect that might overflow)
                    label = self.button_font.render(button["text"], True, text_color)
                    label_rect = label.get_rect(center=button_rect.center)
                    
                    # Ensure text fits within button bounds
                    if label_rect.width > button_rect.width - 20:
                        # Use smaller font if text is too wide
                        smaller_font = pygame.font.SysFont("Arial", 28, bold=True)
                        label = smaller_font.render(button["text"], True, text_color)
                        label_rect = label.get_rect(center=button_rect.center)
                    
                    self.screen.blit(label, label_rect)
                else:
                    label = self.button_font.render(button["text"], True, text_color)
                    label_rect = label.get_rect(center=button_rect.center)
                    
                    # Ensure text fits within button bounds
                    if label_rect.width > button_rect.width - 20:
                        # Use smaller font if text is too wide
                        smaller_font = pygame.font.SysFont("Arial", 28, bold=True)
                        label = smaller_font.render(button["text"], True, text_color)
                        label_rect = label.get_rect(center=button_rect.center)
                    
                    self.screen.blit(label, label_rect)

                # Holographic effect for disabled buttons
                if not button["enabled"]:
                    holo_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
                    for y in range(0, button_rect.height, 4):
                        alpha = int(abs(math.sin(self.time * 2 + y * 0.1)) * 40)
                        pygame.draw.line(holo_surface, (255, 255, 255, alpha), 
                                       (0, y), (button_rect.width, y), 1)
                    self.screen.blit(holo_surface, button_rect.topleft)

            # Draw corner decorations
            corner_size = 50
            corner_color = self.accent_color
            
            # Top-left corner
            pygame.draw.lines(self.screen, corner_color, False, 
                            [(20, 20 + corner_size), (20, 20), (20 + corner_size, 20)], 3)
            # Top-right corner  
            pygame.draw.lines(self.screen, corner_color, False,
                            [(WINDOW_WIDTH - 20 - corner_size, 20), (WINDOW_WIDTH - 20, 20), 
                             (WINDOW_WIDTH - 20, 20 + corner_size)], 3)
            # Bottom-left corner
            pygame.draw.lines(self.screen, corner_color, False,
                            [(20, WINDOW_HEIGHT - 20 - corner_size), (20, WINDOW_HEIGHT - 20), 
                             (20 + corner_size, WINDOW_HEIGHT - 20)], 3)
            # Bottom-right corner
            pygame.draw.lines(self.screen, corner_color, False,
                            [(WINDOW_WIDTH - 20 - corner_size, WINDOW_HEIGHT - 20), 
                             (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20), 
                             (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20 - corner_size)], 3)

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
                                self.fade_out()
                                return "local_host"
                            
                            elif button["text"] == "Quit":
                                pygame.quit()
                                sys.exit()
                                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

    def fade_out(self):
        # Enhanced color palette with more contrast
        neon_colors = [
            (255, 20, 147),   # Deep Pink
            (0, 255, 255),    # Cyan
            (255, 255, 0),    # Yellow  
            (50, 205, 50),    # Lime Green
            (255, 69, 0),     # Red Orange
            (138, 43, 226),   # Blue Violet
            (255, 215, 0),    # Gold
            (255, 105, 180),  # Hot Pink
        ]
        
        # Create surfaces with proper alpha support
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        distortion = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # Capture the original screen
        original_screen = self.screen.copy()
        
        total_frames = 90  # More controlled timing
        
        for frame in range(total_frames):
            # Progress from 0 to 1
            progress = frame / total_frames
            
            # Start with original screen
            self.screen.blit(original_screen, (0, 0))
            
            # === PHASE 1: DIGITAL NOISE (0-30%) ===
            if progress < 0.3:
                noise_intensity = progress / 0.3
                for _ in range(int(noise_intensity * 200)):
                    x = random.randint(0, WINDOW_WIDTH - 1)
                    y = random.randint(0, WINDOW_HEIGHT - 1)
                    color = random.choice(neon_colors)
                    size = random.randint(1, 3)
                    pygame.draw.circle(self.screen, color, (x, y), size)
            
            # === PHASE 2: GLITCH TEARS (20-60%) ===
            if 0.2 < progress < 0.6:
                glitch_intensity = (progress - 0.2) / 0.4
                
                # Horizontal tears
                for _ in range(int(glitch_intensity * 8)):
                    y_pos = random.randint(0, WINDOW_HEIGHT - 40)
                    height = random.randint(5, 20)
                    width = WINDOW_WIDTH
                    
                    # Create displaced section
                    if random.random() > 0.5:
                        # Shift right
                        shift = random.randint(10, 50)
                        source_rect = pygame.Rect(0, y_pos, width - shift, height)
                        dest_pos = (shift, y_pos)
                        self.screen.blit(original_screen, dest_pos, source_rect)
                        
                        # Fill gap with neon color
                        gap_rect = pygame.Rect(0, y_pos, shift, height)
                        pygame.draw.rect(self.screen, random.choice(neon_colors), gap_rect)
                    else:
                        # Shift left  
                        shift = random.randint(10, 50)
                        source_rect = pygame.Rect(shift, y_pos, width - shift, height)
                        dest_pos = (0, y_pos)
                        self.screen.blit(original_screen, dest_pos, source_rect)
                        
                        # Fill gap with neon color
                        gap_rect = pygame.Rect(width - shift, y_pos, shift, height)
                        pygame.draw.rect(self.screen, random.choice(neon_colors), gap_rect)
            
            # === PHASE 3: CHROMATIC ABERRATION (40-80%) ===
            if 0.4 < progress < 0.8:
                aberration_strength = ((progress - 0.4) / 0.4) * 8
                
                # Create RGB channel separation
                red_channel = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                blue_channel = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                
                # Copy original with offsets
                red_offset = int(aberration_strength)
                blue_offset = int(-aberration_strength)
                
                red_channel.blit(original_screen, (red_offset, 0))
                blue_channel.blit(original_screen, (blue_offset, 0))
                
                # Blend channels
                self.screen.blit(red_channel, (0, 0), special_flags=pygame.BLEND_MULT)
                self.screen.blit(blue_channel, (0, 0), special_flags=pygame.BLEND_ADD)
            
            # === PHASE 4: SPIRAL VORTEX (60-100%) ===
            if progress > 0.6:
                vortex_intensity = (progress - 0.6) / 0.4
                
                # Clear overlay
                overlay.fill((0, 0, 0, 0))
                
                center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
                max_radius = max(WINDOW_WIDTH, WINDOW_HEIGHT)
                
                # Create spiral pattern
                for radius in range(0, max_radius, 12):
                    for angle_step in range(0, 360, 15):
                        angle = math.radians(angle_step + frame * 8)  # Rotating spiral
                        
                        x = center_x + int(radius * math.cos(angle))
                        y = center_y + int(radius * math.sin(angle))
                        
                        if 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT:
                            # Color based on radius and time
                            color_index = int((radius + frame * 2) / 40) % len(neon_colors)
                            color = neon_colors[color_index]
                            
                            # Alpha based on vortex intensity and distance from center
                            distance_factor = 1 - (radius / max_radius)
                            alpha = int(vortex_intensity * distance_factor * 255)
                            
                            # Draw spiral arm
                            arm_color = (*color, min(255, alpha))
                            pygame.draw.circle(overlay, arm_color, (x, y), 3)
                
                # Apply vortex overlay
                self.screen.blit(overlay, (0, 0))
            
            # === PHASE 5: FINAL DISSOLUTION (80-100%) ===
            if progress > 0.8:
                dissolve_intensity = (progress - 0.8) / 0.2
                
                # Pixelation effect
                pixel_size = int(1 + dissolve_intensity * 15)
                if pixel_size > 1:
                    # Downscale and upscale for pixelation
                    small_surface = pygame.transform.scale(
                        self.screen, 
                        (WINDOW_WIDTH // pixel_size, WINDOW_HEIGHT // pixel_size)
                    )
                    pixelated = pygame.transform.scale(
                        small_surface, 
                        (WINDOW_WIDTH, WINDOW_HEIGHT)
                    )
                    self.screen.blit(pixelated, (0, 0))
                
                # Add final chaos particles
                for _ in range(int(dissolve_intensity * 300)):
                    x = random.randint(0, WINDOW_WIDTH)
                    y = random.randint(0, WINDOW_HEIGHT)
                    color = random.choice(neon_colors)
                    size = random.randint(1, 4)
                    alpha = int((1 - dissolve_intensity) * 255)
                    
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (*color, alpha), (size, size), size)
                    self.screen.blit(particle_surface, (x - size, y - size))
            
            # === SCREEN SHAKE (throughout) ===
            if progress > 0.3:
                shake_intensity = (progress - 0.3) * 10
                shake_x = random.randint(-int(shake_intensity), int(shake_intensity))
                shake_y = random.randint(-int(shake_intensity), int(shake_intensity))
                
                if shake_x != 0 or shake_y != 0:
                    temp_surface = self.screen.copy()
                    self.screen.fill((0, 0, 0))
                    self.screen.blit(temp_surface, (shake_x, shake_y))
            
            # === SCANLINES (final touch) ===
            if frame % 3 == 0:  # Every 3rd frame
                for y in range(0, WINDOW_HEIGHT, 3):
                    alpha = int(progress * 100)
                    line_color = (0, 0, 0, alpha)
                    line_surface = pygame.Surface((WINDOW_WIDTH, 1), pygame.SRCALPHA)
                    line_surface.fill(line_color)
                    self.screen.blit(line_surface, (0, y))
            
            pygame.display.flip()
            
            # Dynamic timing - faster in middle, slower at start/end
            if progress < 0.2 or progress > 0.8:
                pygame.time.delay(35)  # Slower for buildup/climax
            else:
                pygame.time.delay(20)  # Faster for chaos
        
        # === FINAL FLASH ===
        flash_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        flash_surface.fill((255, 255, 255))
        self.screen.blit(flash_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(80)