import pygame
import sys
import random

pygame.init()

# Window
WIDTH, HEIGHT = 500, 600
PLAY_WIDTH, PLAY_HEIGHT = 400, 400
PLAY_AREA_POS = ((WIDTH - PLAY_WIDTH) // 2, 150)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elegant Snake Game")

# Colors (Default Design)
WHITE = (255, 255, 255)
BLACK = (17, 24, 39)  # for snake and text
GRAY = (107, 114, 128)  # neutral gray for secondary text
LIGHT_GRAY = (230, 230, 230)  # for subtle backgrounds / card
RED = (220, 38, 38)  # red accent for food and buttons

# Fonts
TITLE_FONT = pygame.font.SysFont("Segoe UI", 48, bold=True)
SCORE_FONT = pygame.font.SysFont("Segoe UI", 28, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("Segoe UI", 40, bold=True)
BUTTON_FONT = pygame.font.SysFont("Segoe UI", 26, bold=True)

# Game variables
CELL_SIZE = 20  # Size of each grid cell
COLS = PLAY_WIDTH // CELL_SIZE
ROWS = PLAY_HEIGHT // CELL_SIZE
FPS = 10

clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        # Start at center
        self.positions = [(COLS // 2, ROWS // 2)]
        self.direction = (0, 0)  # Init stationary
        self.grow_pending = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, dir):
        # Prevent reverse direction
        opposites = {(1,0):(-1,0), (-1,0):(1,0), (0,1):(0,-1), (0,-1):(0,1)}
        if self.direction == opposites.get(dir, None):
            return
        self.direction = dir

    def move(self):
        if self.direction == (0,0):
            return
        cur = self.get_head_position()
        new = ((cur[0] + self.direction[0]) % COLS, (cur[1] + self.direction[1]) % ROWS)
        if new in self.positions:
            # Collision with self, handled elsewhere
            self.positions.insert(0, new)
        else:
            self.positions.insert(0, new)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()

    def grow(self):
        self.grow_pending += 1

    def collided(self):
        head = self.get_head_position()
        return self.positions.count(head) > 1

    def draw(self, surface):
        for pos in self.positions:
            x, y = pos
            rect = pygame.Rect(
                PLAY_AREA_POS[0] + x * CELL_SIZE,
                PLAY_AREA_POS[1] + y * CELL_SIZE,
                CELL_SIZE, CELL_SIZE,
            )
            pygame.draw.rect(surface, BLACK, rect, border_radius=5)


class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        positions = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake_positions]
        return random.choice(positions)

    def draw(self, surface):
        x, y = self.position
        center = (PLAY_AREA_POS[0] + x * CELL_SIZE + CELL_SIZE // 2,
                  PLAY_AREA_POS[1] + y * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(surface, RED, center, radius)


def draw_grid(surface):
    for x in range(COLS + 1):
        start_pos = (PLAY_AREA_POS[0] + x * CELL_SIZE, PLAY_AREA_POS[1])
        end_pos = (PLAY_AREA_POS[0] + x * CELL_SIZE, PLAY_AREA_POS[1] + PLAY_HEIGHT)
        pygame.draw.line(surface, LIGHT_GRAY, start_pos, end_pos, 1)
    for y in range(ROWS + 1):
        start_pos = (PLAY_AREA_POS[0], PLAY_AREA_POS[1] + y * CELL_SIZE)
        end_pos = (PLAY_AREA_POS[0] + PLAY_WIDTH, PLAY_AREA_POS[1] + y * CELL_SIZE)
        pygame.draw.line(surface, LIGHT_GRAY, start_pos, end_pos, 1)


def draw_text(surface, text, font, color, center):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=center)
    surface.blit(text_surf, text_rect)


def draw_button(surface, rect, text, hovered):
    radius = 12
    bg_color = RED if hovered else BLACK
    text_color = WHITE
    pygame.draw.rect(surface, bg_color, rect, border_radius=radius)
    text_surf = BUTTON_FONT.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def main():
    snake = Snake()
    food = Food(snake.positions)
    score = 0
    running = True
    game_over = False

    # Restart button rect
    button_width = 180
    button_height = 50
    button_rect = pygame.Rect((WIDTH - button_width) // 2, PLAY_AREA_POS[1] + PLAY_HEIGHT + 60, button_width, button_height)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and button_hovered:
                    # Restart game
                    snake = Snake()
                    food = Food(snake.positions)
                    score = 0
                    game_over = False

        if not game_over:
            snake.move()
            # Check eating food
            if snake.get_head_position() == food.position:
                snake.grow()
                score += 1
                food = Food(snake.positions)

            # Check collision with self
            if snake.collided():
                game_over = True

        # Draw background
        SCREEN.fill(WHITE)

        # Draw Title
        draw_text(SCREEN, "Elegant Snake Game", TITLE_FONT, BLACK, (WIDTH // 2, 50))

        # Draw score
        draw_text(SCREEN, f"Score: {score}", SCORE_FONT, GRAY, (WIDTH // 2, 110))

        # Draw play area background card with subtle shadow
        play_area_rect = pygame.Rect(PLAY_AREA_POS, (PLAY_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(SCREEN, LIGHT_GRAY, play_area_rect, border_radius=12)

        # Draw grid lines
        draw_grid(SCREEN)

        # Draw snake and food
        snake.draw(SCREEN)
        food.draw(SCREEN)

        if game_over:
            # Draw translucent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 220))
            SCREEN.blit(overlay, (0, 0))

            # Draw Game Over card with subtle shadow
            card_width, card_height = 350, 180
            card_x = (WIDTH - card_width) // 2
            card_y = (HEIGHT - card_height) // 2
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)

            pygame.draw.rect(SCREEN, WHITE, card_rect, border_radius=12)
            pygame.draw.rect(SCREEN, LIGHT_GRAY, card_rect, 1, border_radius=12)

            draw_text(SCREEN, "Game Over!", GAME_OVER_FONT, BLACK, (WIDTH // 2, card_y + 50))
            draw_text(SCREEN, f"Final Score: {score}", SCORE_FONT, GRAY, (WIDTH // 2, card_y + 100))

            # Draw restart button with hover effect
            draw_button(SCREEN, button_rect, "Restart", button_hovered)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
