import pygame
import sys
import random

pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap Bird - Single Phase")

# Colors (following Default inspiration guidelines - light and elegant)
WHITE = (255, 255, 255)
GRAY = (107, 114, 128)  # #6b7280 neutral gray for text
BLACK = (17, 24, 39) # #111827 dark for contrast
LIGHT_SHADOW = (220, 220, 220)

# Fonts
TITLE_FONT = pygame.font.SysFont("Inter", 48, bold=True)
TEXT_FONT = pygame.font.SysFont("Inter", 24)
BUTTON_FONT = pygame.font.SysFont("Inter", 28, bold=True)

# Game settings for difficulty modes
DIFFICULTY_SETTINGS = {
    "Easy": {
        "gravity": 0.3,
        "jump_strength": -6.5,
        "pipe_speed": 2,
        "pipe_gap": 180,
        "pipe_frequency": 1500,  # milliseconds
    },
    "Medium": {
        "gravity": 0.4,
        "jump_strength": -7,
        "pipe_speed": 3,
        "pipe_gap": 150,
        "pipe_frequency": 1300,
    },
    "Hard": {
        "gravity": 0.5,
        "jump_strength": -8,
        "pipe_speed": 4,
        "pipe_gap": 120,
        "pipe_frequency": 1000,
    },
}

# Load bird image (simple circle used instead for minimal design)
BIRD_RADIUS = 18

# Pipe settings
PIPE_WIDTH = 70

# Frame rate
FPS = 60
clock = pygame.time.Clock()


class Bird:
    def __init__(self, x, y, gravity, jump_strength):
        self.x = x
        self.y = y
        self.gravity = gravity
        self.jump_strength = jump_strength
        self.movement = 0
        self.rect = pygame.Rect(x - BIRD_RADIUS, y - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)

    def update(self):
        self.movement += self.gravity
        self.y += self.movement
        self.rect.y = int(self.y) - BIRD_RADIUS

    def jump(self):
        self.movement = self.jump_strength

    def draw(self, surface):
        # Draw bird circle with subtle shadow
        shadow_pos = (self.x + 3, int(self.y) + 3)
        pygame.draw.circle(surface, LIGHT_SHADOW, shadow_pos, BIRD_RADIUS)
        pygame.draw.circle(surface, BLACK, (self.x, int(self.y)), BIRD_RADIUS)


class Pipe:
    def __init__(self, x, height, gap, speed):
        self.x = x
        self.height = height
        self.gap = gap
        self.speed = speed
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + self.gap, PIPE_WIDTH, HEIGHT - (self.height + self.gap))

    def update(self):
        self.x -= self.speed
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, surface):
        # Draw pipe with rounded corners - simulate with rects and circles
        pipe_color = BLACK
        radius = 10
        # Top pipe
        pygame.draw.rect(surface, pipe_color, self.top_rect)
        pygame.draw.circle(surface, pipe_color, (self.top_rect.right, self.top_rect.bottom), radius)
        # Bottom pipe
        pygame.draw.rect(surface, pipe_color, self.bottom_rect)
        pygame.draw.circle(surface, pipe_color, (self.bottom_rect.right, self.bottom_rect.top), radius)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collide(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.hovered = False

    def draw(self, surface):
        color_bg = BLACK if self.hovered else GRAY
        color_text = WHITE if self.hovered else BLACK
        radius = 12
        # Draw rounded rect background
        pygame.draw.rect(surface, color_bg, self.rect, border_radius=radius)
        # Draw text centered
        text_surf = BUTTON_FONT.render(self.text, True, color_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        pass


def draw_text_center(surface, text, font, color, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surf, text_rect)


def main():
    running = True
    show_menu = True
    difficulty = None

    # For game
    bird = None
    pipes = []
    spawn_pipe_event = pygame.USEREVENT + 1

    score = 0
    game_active = False

    # Buttons for difficulty selection
    button_width = 140
    button_height = 60
    spacing = 30
    total_width = 3 * button_width + 2 * spacing
    start_x = (WIDTH - total_width) // 2
    buttons = []
    difficulties = ["Easy", "Medium", "Hard"]
    for i, diff in enumerate(difficulties):
        rect = (start_x + i * (button_width + spacing), HEIGHT // 2, button_width, button_height)
        btn = Button(rect, diff)
        buttons.append(btn)

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if show_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn.is_hovered(mouse_pos):
                            difficulty = btn.text
                            # Setup game with difficulty
                            settings = DIFFICULTY_SETTINGS[difficulty]
                            bird = Bird(80, HEIGHT // 2, settings["gravity"], settings["jump_strength"])
                            pipes = []
                            score = 0
                            game_active = True
                            pygame.time.set_timer(spawn_pipe_event, settings["pipe_frequency"])
                            show_menu = False
            else:
                if game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            bird.jump()
                    if event.type == spawn_pipe_event:
                        new_pipe_height = random.randint(80, HEIGHT - DIFFICULTY_SETTINGS[difficulty]["pipe_gap"] - 80)
                        new_pipe = Pipe(WIDTH + 10, new_pipe_height, DIFFICULTY_SETTINGS[difficulty]["pipe_gap"], DIFFICULTY_SETTINGS[difficulty]["pipe_speed"])
                        pipes.append(new_pipe)

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Restart game, back to menu
                        show_menu = True
                        difficulty = None

        SCREEN.fill(WHITE)

        if show_menu:
            # Draw title
            draw_text_center(SCREEN, "Flap Bird", TITLE_FONT, BLACK, HEIGHT // 4)
            draw_text_center(SCREEN, "Select difficulty:", TEXT_FONT, GRAY, HEIGHT // 3 + 20)

            # Draw buttons
            for btn in buttons:
                btn.hovered = btn.is_hovered(mouse_pos)
                btn.draw(SCREEN)

        else:
            # Game play

            # Draw pipes
            for pipe in pipes:
                pipe.draw(SCREEN)

            # Update bird and draw
            bird.update()
            bird.draw(SCREEN)

            # Update pipes
            for pipe in pipes[:]:
                pipe.update()
                if pipe.off_screen():
                    pipes.remove(pipe)
                    score += 1

            # Check collisions
            bird_rect = bird.rect
            collided = False
            if bird.y - BIRD_RADIUS <= 0 or bird.y + BIRD_RADIUS >= HEIGHT:
                collided = True

            for pipe in pipes:
                if pipe.collide(bird_rect):
                    collided = True
                    break

            # Continuous game or crash?
            if collided:
                game_active = False
                pygame.time.set_timer(spawn_pipe_event, 0)  # stop pipe spawning

            # Draw score top middle
            draw_text_center(SCREEN, f"Score: {score}", TEXT_FONT, BLACK, 40)

            if not game_active:
                draw_text_center(SCREEN, "Game Over!", TITLE_FONT, BLACK, HEIGHT // 2 - 40)
                draw_text_center(SCREEN, "Press SPACE to return to menu", TEXT_FONT, GRAY, HEIGHT // 2 + 20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

