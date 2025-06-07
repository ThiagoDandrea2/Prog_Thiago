import pygame
import sys
import random
import json
import os

pygame.init()

# Constants for styling and dimensions
WIDTH, HEIGHT = 1000, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap Bird - Single Phase")

# Colors
WHITE = (255, 255, 255)
GRAY = (107, 114, 128)  # #6b7280 neutral gray
BLACK = (17, 24, 39)    # #111827 dark for text and bird
LIGHT_SHADOW = (220, 220, 220)
SKY_BLUE = (200, 225, 255)
MOUNTAIN_DARK = (120, 140, 180)
MOUNTAIN_LIGHT = (180, 200, 220)
BIRD_BODY = (30, 30, 30)
SMALL_BIRD_COLOR = (80, 80, 80)

# Fonts (using system fonts similar to Inter for simplicity)
TITLE_FONT = pygame.font.SysFont("Segoe UI", 48, bold=True)
TEXT_FONT = pygame.font.SysFont("Segoe UI", 24)
BUTTON_FONT = pygame.font.SysFont("Segoe UI", 28, bold=True)
INPUT_FONT = pygame.font.SysFont("Segoe UI", 20)

# Game settings for difficulty modes
DIFFICULTY_SETTINGS = {
    "Easy": {
        "gravity": 0.3,
        "jump_strength": -6.5,
        "pipe_speed": 2,
        "pipe_gap": 180,
        "pipe_frequency": 1500,
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

BIRD_RADIUS = 18
PIPE_WIDTH = 70
FPS = 60
clock = pygame.time.Clock()

SCORES_FILE = "flap_bird_scores.json"


class SmallBirdFlock:
    def __init__(self):
        self.y = random.randint(50, HEIGHT // 2)
        self.x = random.randint(0, WIDTH)
        self.speed = random.uniform(0.8, 1.5)
        self.size = random.randint(7, 12)
        self.direction = random.choice([-1, 1])
        self.wing_up = True
        self.wing_counter = 0

    def update(self):
        self.x += self.speed * self.direction
        if self.x > WIDTH + 20:
            self.x = -20
        elif self.x < -20:
            self.x = WIDTH + 20
        self.wing_counter += 1
        if self.wing_counter > 15:
            self.wing_up = not self.wing_up
            self.wing_counter = 0

    def draw(self, surface):
        points = []
        center = (int(self.x), int(self.y))
        wing_offset = 6 if self.wing_up else 3
        if self.direction > 0:
            points = [
                (center[0] - self.size, center[1]),
                (center[0], center[1] - wing_offset),
                (center[0] + self.size, center[1]),
                (center[0], center[1] + wing_offset),
            ]
        else:
            points = [
                (center[0] + self.size, center[1]),
                (center[0], center[1] - wing_offset),
                (center[0] - self.size, center[1]),
                (center[0], center[1] + wing_offset),
            ]
        pygame.draw.lines(surface, SMALL_BIRD_COLOR, False, points, 2)


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
        shadow_pos = (self.x + 3, int(self.y) + 3)
        pygame.draw.circle(surface, LIGHT_SHADOW, shadow_pos, BIRD_RADIUS)
        pygame.draw.circle(surface, BIRD_BODY, (self.x, int(self.y)), BIRD_RADIUS)
        eye_center = (self.x + 6, int(self.y) - 5)
        pygame.draw.circle(surface, WHITE, eye_center, 6)
        pygame.draw.circle(surface, BLACK, eye_center, 3)


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
        pipe_color = BIRD_BODY
        radius = 10
        pygame.draw.rect(surface, pipe_color, self.top_rect)
        pygame.draw.circle(surface, pipe_color, (self.top_rect.right, self.top_rect.bottom), radius)
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
        color_bg = BIRD_BODY if self.hovered else GRAY
        color_text = WHITE if self.hovered else BLACK
        radius = 12
        pygame.draw.rect(surface, color_bg, self.rect, border_radius=radius)
        text_surf = BUTTON_FONT.render(self.text, True, color_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class TextInput:
    def __init__(self, rect, font, surface):
        self.rect = pygame.Rect(rect)
        self.color_inactive = GRAY
        self.color_active = BLACK
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.surface = surface
        self.active = False
        self.txt_surface = self.font.render(self.text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 15 and event.unicode.isprintable():
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)
        return False

    def draw(self):
        pygame.draw.rect(self.surface, WHITE, self.rect)
        pygame.draw.rect(self.surface, self.color, self.rect, 2, border_radius=8)
        self.surface.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 6))

    def get_text(self):
        return self.text.strip()


def draw_text_center(surface, text, font, color, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
    surface.blit(text_surf, text_rect)


def draw_mountains(surface):
    base_y = HEIGHT - 80
    mountain_points_1 = [(0, base_y + 60), (60, base_y - 40), (120, base_y + 60), (180, base_y - 10),
                         (240, base_y + 70), (300, base_y + 10), (360, base_y + 80),
                         (WIDTH, base_y + 80), (WIDTH, HEIGHT), (0, HEIGHT)]
    mountain_points_2 = [(0, base_y + 100), (70, base_y + 20), (140, base_y + 90), (210, base_y),
                         (280, base_y + 60), (350, base_y + 30),
                         (WIDTH, base_y + 90), (WIDTH, HEIGHT), (0, HEIGHT)]
    mountain_points_3 = [(0, base_y + 140), (80, base_y + 70), (160, base_y + 130), (240, base_y + 50),
                         (320, base_y + 100), (WIDTH, base_y + 130), (WIDTH, HEIGHT), (0, HEIGHT)]

    pygame.draw.polygon(surface, MOUNTAIN_LIGHT, mountain_points_3)
    pygame.draw.polygon(surface, MOUNTAIN_DARK, mountain_points_2)
    pygame.draw.polygon(surface, BLACK, mountain_points_1)


def main():
    running = True

    # Game variables
    bird = None
    pipes = []
    spawn_pipe_event = pygame.USEREVENT + 1
    score = 0
    game_active = False

    # Small background birds
    small_birds = [SmallBirdFlock() for _ in range(6)]

    # Input and buttons states and UI components
    player_name_input = TextInput((WIDTH // 2 - 100, HEIGHT // 3 + 10, 200, 40), INPUT_FONT, SCREEN)
    submit_name_btn = Button((WIDTH // 2 - 80, HEIGHT // 3 + 70, 160, 50), "Submit")

    difficulty_buttons = []
    difficulties = ["Easy", "Medium", "Hard"]
    button_width = 140
    button_height = 60
    spacing = 30
    total_width = 3 * button_width + 2 * spacing
    start_x = (WIDTH - total_width) // 2
    for i, diff in enumerate(difficulties):
        rect = (start_x + i * (button_width + spacing), HEIGHT // 2, button_width, button_height)
        difficulty_buttons.append((Button(rect, diff), diff))

    leaderboard = []

    # Load leaderboard data
    def load_scores():
        nonlocal leaderboard
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, "r") as f:
                    leaderboard = json.load(f)
            except Exception:
                leaderboard = []
        else:
            leaderboard = []

    def save_scores():
        with open(SCORES_FILE, "w") as f:
            json.dump(leaderboard, f, indent=4)

    def add_score(name, score_val):
        nonlocal leaderboard
        text_name = name if name else "Anonymous"
        leaderboard.append({"name": text_name, "score": score_val})
        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
        save_scores()

    def draw_leaderboard(surface):
        x = WIDTH // 2
        y = HEIGHT // 2 + 180
        title = "Leaderboard"
        title_surf = TEXT_FONT.render(title, True, BLACK)
        surface.blit(title_surf, title_surf.get_rect(center=(x, y - 30)))
        for i, entry in enumerate(leaderboard):
            entry_text = f"{i + 1}. {entry['name']} — {entry['score']}"
            entry_surf = INPUT_FONT.render(entry_text, True, GRAY)
            surface.blit(entry_surf, entry_surf.get_rect(center=(x, y + i * 30)))

    load_scores()

    # States tracking flow:
    # "enter_name" -> player input name
    # "select_difficulty" -> difficulty selection
    # "playing" -> game active
    # "game_over" -> game ended waiting for restart
    state = "enter_name"
    player_name = ""
    difficulty = None

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "enter_name":
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    enter_pressed = player_name_input.handle_event(event)
                    if enter_pressed:
                        player_name = player_name_input.get_text()
                        if not player_name:
                            player_name = "Anonymous"
                        state = "select_difficulty"
            elif state == "select_difficulty":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn, diff in difficulty_buttons:
                        if btn.is_hovered(mouse_pos):
                            difficulty = diff
                            settings = DIFFICULTY_SETTINGS[difficulty]
                            bird = Bird(80, HEIGHT // 2, settings["gravity"], settings["jump_strength"])
                            pipes = []
                            score = 0
                            game_active = True
                            pygame.time.set_timer(spawn_pipe_event, settings["pipe_frequency"])
                            state = "playing"
            elif state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        bird.jump()
                if event.type == spawn_pipe_event:
                    new_pipe_height = random.randint(80, HEIGHT - DIFFICULTY_SETTINGS[difficulty]["pipe_gap"] - 80)
                    new_pipe = Pipe(WIDTH + 10, new_pipe_height, DIFFICULTY_SETTINGS[difficulty]["pipe_gap"],
                                    DIFFICULTY_SETTINGS[difficulty]["pipe_speed"])
                    pipes.append(new_pipe)
            elif state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart: back to difficulty select, keep name
                        state = "select_difficulty"
                    elif event.key == pygame.K_RETURN:
                        # Restart from enter name screen to enter new name
                        # optional: clear previous name
                        player_name_input.text = ""
                        player_name_input.txt_surface = player_name_input.font.render("", True,
                                                                                      player_name_input.color)
                        player_name = ""
                        state = "enter_name"

        SCREEN.fill(SKY_BLUE)
        draw_mountains(SCREEN)
        for sb in small_birds:
            sb.update()
            sb.draw(SCREEN)

        if state == "enter_name":
            draw_text_center(SCREEN, "Enter your name", TITLE_FONT, BLACK, HEIGHT // 4)
            player_name_input.draw()
            submit_name_btn.hovered = submit_name_btn.is_hovered(mouse_pos)
            submit_name_btn.draw(SCREEN)
            # Submit button click
            if pygame.mouse.get_pressed()[0] and submit_name_btn.is_hovered(mouse_pos):
                player_name = player_name_input.get_text()
                if not player_name:
                    player_name = "Anonymous"
                state = "select_difficulty"
        elif state == "select_difficulty":
            draw_text_center(SCREEN, f"Hello, {player_name}!", TITLE_FONT, BLACK, HEIGHT // 4)
            draw_text_center(SCREEN, "Select difficulty:", TEXT_FONT, GRAY, HEIGHT // 3 + 20)
            for btn, _ in difficulty_buttons:
                btn.hovered = btn.is_hovered(mouse_pos)
                btn.draw(SCREEN)
        elif state == "playing":
            for pipe in pipes:
                pipe.draw(SCREEN)
            bird.update()
            bird.draw(SCREEN)
            for pipe in pipes[:]:
                pipe.update()
                if pipe.off_screen():
                    pipes.remove(pipe)
                    score += 1

            bird_rect = bird.rect
            collided = False
            if bird.y - BIRD_RADIUS <= 0 or bird.y + BIRD_RADIUS >= HEIGHT:
                collided = True
            for pipe in pipes:
                if pipe.collide(bird_rect):
                    collided = True
                    break

            draw_text_center(SCREEN, f"Score: {score}", TEXT_FONT, BLACK, 40)

            if collided:
                game_active = False
                pygame.time.set_timer(spawn_pipe_event, 0)
                state = "game_over"
                add_score(player_name, score)
        elif state == "game_over":
            draw_text_center(SCREEN, "Game Over!", TITLE_FONT, BLACK, HEIGHT // 2 - 80)
            draw_text_center(SCREEN, f"Your score: {score}", TEXT_FONT, GRAY, HEIGHT // 2 - 30)
            draw_text_center(SCREEN, "Press SPACE to select difficulty", TEXT_FONT, GRAY, HEIGHT // 2 + 20)
            draw_text_center(SCREEN, "Press ENTER to enter name", TEXT_FONT, GRAY, HEIGHT // 2 + 60)
            draw_leaderboard(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
