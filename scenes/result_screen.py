import pygame
import sys
import math
import random
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
import os

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-3, -1)
        self.life = 255
        self.color = color
        self.size = random.uniform(2, 5)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.life -= 2
        self.size = max(0, self.size - 0.02)
        
    def is_alive(self):
        return self.life > 0 and self.size > 0
        
    def draw(self, screen):
        if self.is_alive():
            alpha = max(0, min(255, self.life))
            color_with_alpha = (*self.color, alpha)
            # Create a surface for the particle with alpha
            particle_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color_with_alpha, 
                             (int(self.size), int(self.size)), int(self.size))
            screen.blit(particle_surf, (self.x - self.size, self.y - self.size))

class ResultScreen:
    def __init__(self, game, result_message):
        self.game = game
        self.screen = game.screen
        self.clock = pygame.time.Clock()
        self.result_message = result_message
        self.time = 0
        self.particles = []
        
        # Enhanced fonts with fallbacks
        try:
            self.title_font = pygame.font.Font(None, 72)
            self.button_font = pygame.font.Font(None, 36)
            self.subtitle_font = pygame.font.Font(None, 28)
        except:
            self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
            self.button_font = pygame.font.SysFont("Arial", 36, bold=True)
            self.subtitle_font = pygame.font.SysFont("Arial", 28)

        # Load and scale background with error handling
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
            # Fallback gradient background
            self.bg_image = None
            
        # Create animated gradient background
        self.create_gradient_background()
        
        # Enhanced overlay with animated opacity
        self.create_animated_overlay()

        # Button setup with animations
        self.buttons = []
        button_texts = ["Return to Main Menu", "Quit Game"]
        self.button_width = 350
        self.button_height = 70
        start_y = WINDOW_HEIGHT // 2 + 80

        for i, text in enumerate(button_texts):
            x = (WINDOW_WIDTH - self.button_width) // 2
            y = start_y + i * (self.button_height + 25)
            self.buttons.append({
                "text": text,
                "rect": pygame.Rect(x, y, self.button_width, self.button_height),
                "hover": False,
                "scale": 1.0,
                "pulse": 0,
                "glow": 0
            })
            
        # Animation states
        self.title_scale = 0.1
        self.title_alpha = 0
        self.button_appear_delay = [30, 45]  # frames delay for each button
        self.show_buttons = [False, False]
        
        # Determine result type for styling
        self.is_victory = "win" in result_message.lower() or "victory" in result_message.lower()
        self.result_color = (255, 215, 0) if self.is_victory else (255, 100, 100)
        
        # Star field for victory
        if self.is_victory:
            self.stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT), 
                          random.uniform(0.5, 2.0)) for _ in range(50)]
    
    def create_gradient_background(self):
        """Create an animated gradient background"""
        self.gradient_bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
    def create_animated_overlay(self):
        """Create animated overlay effects"""
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
    def update_particles(self):
        """Update and manage particle system"""
        # Add new particles occasionally
        if random.random() < 0.3:
            x = random.randint(0, WINDOW_WIDTH)
            y = WINDOW_HEIGHT + 10
            color = self.result_color if random.random() < 0.7 else (255, 255, 255)
            self.particles.append(Particle(x, y, color))
            
        # Update existing particles
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
    
    def draw_animated_background(self):
        """Draw the animated background"""
        if self.bg_image:
            # Apply subtle movement to background
            offset_x = math.sin(self.time * 0.01) * 5
            offset_y = math.cos(self.time * 0.015) * 3
            self.screen.blit(self.bg_image, (self.bg_x + offset_x, self.bg_y + offset_y))
        else:
            # Animated gradient fallback
            for y in range(WINDOW_HEIGHT):
                ratio = y / WINDOW_HEIGHT
                wave = math.sin(self.time * 0.02 + ratio * 4) * 0.3 + 0.7
                color = (
                    int(20 + 40 * wave),
                    int(10 + 30 * wave), 
                    int(40 + 60 * wave)
                )
                pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
        
        # Animated overlay
        overlay_alpha = int(50 + 30 * math.sin(self.time * 0.02))
        self.overlay.fill((0, 0, 0, 0))
        for y in range(0, WINDOW_HEIGHT, 4):
            alpha = int(overlay_alpha * (1 - y / WINDOW_HEIGHT))
            color = (10, 5, 20, alpha)
            pygame.draw.line(self.overlay, color, (0, y), (WINDOW_WIDTH, y), 4)
        self.screen.blit(self.overlay, (0, 0))
        
        # Draw victory stars
        if self.is_victory:
            for i, (x, y, size) in enumerate(self.stars):
                twinkle = math.sin(self.time * 0.1 + i) * 0.5 + 0.5
                alpha = int(100 + 155 * twinkle)
                star_color = (255, 255, 200, alpha)
                
                # Create star surface
                star_surf = pygame.Surface((int(size * 8), int(size * 8)), pygame.SRCALPHA)
                points = []
                for j in range(10):
                    angle = j * math.pi / 5
                    radius = size * 3 if j % 2 == 0 else size * 1.5
                    px = size * 4 + radius * math.cos(angle)
                    py = size * 4 + radius * math.sin(angle)
                    points.append((px, py))
                pygame.draw.polygon(star_surf, star_color, points)
                self.screen.blit(star_surf, (x - size * 4, y - size * 4))
    
    def draw_enhanced_title(self):
        """Draw the animated title with effects"""
        # Animate title appearance
        if self.title_scale < 1.0:
            self.title_scale = min(1.0, self.title_scale + 0.05)
        if self.title_alpha < 255:
            self.title_alpha = min(255, self.title_alpha + 8)
            
        # Create glowing effect for title
        glow_intensity = math.sin(self.time * 0.1) * 0.3 + 0.7
        
        # Draw glow layers
        for offset in range(8, 0, -2):
            glow_alpha = int(30 * glow_intensity * (8 - offset) / 8)
            glow_color = (*self.result_color, glow_alpha)
            
            # Create glow surface
            glow_surf = pygame.Surface((WINDOW_WIDTH, 200), pygame.SRCALPHA)
            scaled_font_size = int(72 * self.title_scale)
            try:
                glow_font = pygame.font.Font(None, scaled_font_size + offset)
            except:
                glow_font = pygame.font.SysFont("Arial", scaled_font_size + offset, bold=True)
                
            glow_text = glow_font.render(self.result_message, True, glow_color[:3])
            glow_rect = glow_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
            glow_surf.blit(glow_text, glow_rect)
            glow_surf.set_alpha(glow_alpha)
            self.screen.blit(glow_surf, (0, WINDOW_HEIGHT // 2 - 200))
        
        # Draw main title
        scaled_font_size = int(72 * self.title_scale)
        try:
            title_font = pygame.font.Font(None, scaled_font_size)
        except:
            title_font = pygame.font.SysFont("Arial", scaled_font_size, bold=True)
            
        title_surface = title_font.render(self.result_message, True, self.result_color)
        title_surface.set_alpha(self.title_alpha)
        
        # Add subtle movement
        y_offset = math.sin(self.time * 0.08) * 5
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100 + y_offset))
        self.screen.blit(title_surface, title_rect)
        
        # Add sparkle effects for victory
        if self.is_victory and self.title_alpha > 200:
            for _ in range(3):
                if random.random() < 0.1:
                    spark_x = title_rect.centerx + random.randint(-title_rect.width//2, title_rect.width//2)
                    spark_y = title_rect.centery + random.randint(-20, 20)
                    spark_color = (255, 255, 200)
                    self.particles.append(Particle(spark_x, spark_y, spark_color))
    
    def draw_enhanced_buttons(self):
        """Draw animated buttons with hover effects"""
        mouse_pos = pygame.mouse.get_pos()
        
        for i, button in enumerate(self.buttons):
            # Button appearance animation
            if self.time > self.button_appear_delay[i]:
                self.show_buttons[i] = True
                
            if not self.show_buttons[i]:
                continue
                
            # Update button animations
            button["hover"] = button["rect"].collidepoint(mouse_pos)
            
            # Scale animation
            target_scale = 1.1 if button["hover"] else 1.0
            button["scale"] += (target_scale - button["scale"]) * 0.15
            
            # Pulse animation
            button["pulse"] += 0.2
            pulse_offset = math.sin(button["pulse"]) * 3
            
            # Glow animation
            if button["hover"]:
                button["glow"] = min(1.0, button["glow"] + 0.1)
            else:
                button["glow"] = max(0.0, button["glow"] - 0.05)
            
            # Calculate button position and size
            scaled_width = int(self.button_width * button["scale"])
            scaled_height = int(self.button_height * button["scale"])
            button_x = button["rect"].centerx - scaled_width // 2
            button_y = button["rect"].centery - scaled_height // 2 + pulse_offset
            
            scaled_rect = pygame.Rect(button_x, button_y, scaled_width, scaled_height)
            
            # Draw glow effect
            if button["glow"] > 0:
                glow_size = int(10 * button["glow"])
                glow_rect = scaled_rect.inflate(glow_size * 2, glow_size * 2)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                
                glow_color = (0, 255, 255, int(50 * button["glow"]))
                pygame.draw.rect(glow_surf, glow_color, (0, 0, glow_rect.width, glow_rect.height), 
                               border_radius=20)
                self.screen.blit(glow_surf, glow_rect.topleft)
            
            # Draw button background with gradient
            button_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
            
            # Create gradient effect
            base_color = (0, 200, 200) if button["hover"] else (60, 60, 80)
            highlight_color = (0, 255, 255) if button["hover"] else (100, 100, 120)
            
            for y in range(scaled_height):
                ratio = y / scaled_height
                color = [
                    int(base_color[j] + (highlight_color[j] - base_color[j]) * (1 - ratio))
                    for j in range(3)
                ]
                pygame.draw.line(button_surf, color, (0, y), (scaled_width, y))
            
            # Add border
            border_color = (0, 255, 255) if button["hover"] else (120, 120, 140)
            pygame.draw.rect(button_surf, border_color, (0, 0, scaled_width, scaled_height), 
                           width=3, border_radius=15)
            
            self.screen.blit(button_surf, (button_x, button_y))
            
            # Draw button text with shadow
            text_color = (0, 0, 0) if button["hover"] else (200, 200, 200)
            shadow_color = (0, 0, 0, 100)
            
            # Shadow
            shadow_surf = self.button_font.render(button["text"], True, shadow_color[:3])
            shadow_rect = shadow_surf.get_rect(center=(scaled_rect.centerx + 2, scaled_rect.centery + 2))
            shadow_surf.set_alpha(shadow_color[3])
            self.screen.blit(shadow_surf, shadow_rect)
            
            # Main text
            text_surface = self.button_font.render(button["text"], True, text_color)
            text_rect = text_surface.get_rect(center=scaled_rect.center)
            self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.time += 1
            self.clock.tick(60)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if self.show_buttons[i] and button["rect"].collidepoint(event.pos):
                            # Button click animation
                            button["scale"] = 0.9
                            
                            if "Return to Main Menu" in button["text"]:
                                return "menu"
                            elif "Quit" in button["text"]:
                                pygame.quit()
                                sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            # Update animations
            self.update_particles()
            
            # Draw everything
            self.draw_animated_background()
            
            # Draw particles
            for particle in self.particles:
                particle.draw(self.screen)
            
            self.draw_enhanced_title()
            self.draw_enhanced_buttons()
            
            # Add screen flash effect for victory
            if self.is_victory and self.time < 30:
                flash_alpha = int(50 * (1 - self.time / 30))
                flash_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                flash_surf.fill((255, 255, 255, flash_alpha))
                self.screen.blit(flash_surf, (0, 0))

            pygame.display.flip()

        return "menu"