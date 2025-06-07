import pygame
import sys
import random

pygame.init()

# Window dimensions and position for play area
WIDTH, HEIGHT = 500, 600
PLAY_WIDTH, PLAY_HEIGHT = 400, 400
PLAY_AREA_POS = ((WIDTH - PLAY_WIDTH) // 2, 150)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elegant Snake Game with Terrain")

# Colors consistent with Default Design Guidelines
WHITE = (255, 255, 255)
BLACK = (17, 24, 39)  # snake & text
GRAY = (107, 114, 128)  # neutral gray for grid and secondary text
LIGHT_GRAY = (230, 230, 230)  # background card color
EARTH_GREEN = (152, 185, 130)
EARTH_BROWN = (181, 148, 107)
TERRAIN_PATCHES = [EARTH_GREEN, EARTH_BROWN]
RED = (220, 38, 38)  # food
SHADOW = (200, 200, 200, 60)  # shadow for card edges (translucent)

# Fonts with strong hierarchy
TITLE_FONT = pygame.font.SysFont("Segoe UI", 48, bold=True)
SCORE_FONT = pygame.font.SysFont("Segoe UI", 28, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("Segoe UI", 40, bold=True)
BUTTON_FONT = pygame.font.SysFont("Segoe UI", 26, bold=True)

CELL_SIZE = 20
COLS = PLAY_WIDTH // CELL_SIZE
ROWS = PLAY_HEIGHT // CELL_SIZE
FPS = 10
clock = pygame.time.Clock()

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.positions = [(COLS // 2, ROWS // 2)]
        self.direction = (0, 0)
        self.grow_pending = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, new_dir):
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if self.direction == opposites.get(new_dir):
            return
        self.direction = new_dir

    def move(self):
        if self.direction == (0, 0):
            return  # stationary at start

        cur_x, cur_y = self.get_head_position()
        dx, dy = self.direction
        new_x = cur_x + dx
        new_y = cur_y + dy

        # Border collision: do not allow going out of bounds
        bounced = False
        if new_x < 0 or new_x >= COLS:
            # Horizontal goes off limit - ignore move (snake can’t cross border sideways)
            return
        if new_y < 0 or new_y >= ROWS:
            # Vertical border collision: bounce vertically randomly
            bounced = True
            self.direction = random.choice([UP, DOWN])
            dx, dy = self.direction
            new_x = cur_x + dx
            new_y = cur_y + dy
            # Check if bounce still inside boundary, else reverse direction again
            if new_y < 0:
                self.direction = DOWN
                new_y = cur_y + 1
            elif new_y >= ROWS:
                self.direction = UP
                new_y = cur_y - 1

        new_pos = (new_x, new_y)
        if new_pos in self.positions:
            # Collided with self will be handled in game_over check
            self.positions.insert(0, new_pos)
        else:
            self.positions.insert(0, new_pos)

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
                CELL_SIZE,
                CELL_SIZE,
            )
            # Rounded rect for snake body
            pygame.draw.rect(surface, BLACK, rect, border_radius=5)


class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        valid_positions = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake_positions]
        return random.choice(valid_positions)

    def draw(self, surface):
        x, y = self.position
        center = (
            PLAY_AREA_POS[0] + x * CELL_SIZE + CELL_SIZE // 2,
            PLAY_AREA_POS[1] + y * CELL_SIZE + CELL_SIZE // 2,
        )
        radius = CELL_SIZE // 2 - 3
        pygame.draw.circle(surface, RED, center, radius)


def draw_grid(surface):
    # Draw slightly transparent grid lines for elegance
    for x in range(COLS + 1):
        start = (PLAY_AREA_POS[0] + x * CELL_SIZE, PLAY_AREA_POS[1])
        end = (PLAY_AREA_POS[0] + x * CELL_SIZE, PLAY_AREA_POS[1] + PLAY_HEIGHT)
        pygame.draw.line(surface, GRAY, start, end, 1)
    for y in range(ROWS + 1):
        start = (PLAY_AREA_POS[0], PLAY_AREA_POS[1] + y * CELL_SIZE)
        end = (PLAY_AREA_POS[0] + PLAY_WIDTH, PLAY_AREA_POS[1] + y * CELL_SIZE)
        pygame.draw.line(surface, GRAY, start, end, 1)


def draw_terrain(surface):
    # Draw small squares in terrain patches to simulate earth background under play area

    # Terrain grid smaller than play area grid for subtle effect
    terrain_cols = COLS * 2
    terrain_rows = ROWS * 2
    terrain_cell_w = PLAY_WIDTH / terrain_cols
    terrain_cell_h = PLAY_HEIGHT / terrain_rows

    for i in range(terrain_cols):
        for j in range(terrain_rows):
            color = random.choices(TERRAIN_PATCHES, weights=[0.65, 0.35])[0]
            # Randomize opacity subtly with alpha blending for depth effect
            alpha = random.randint(40, 70)
            patch_surf = pygame.Surface((terrain_cell_w, terrain_cell_h), pygame.SRCALPHA)
            patch_surf.fill((*color, alpha))
            x = PLAY_AREA_POS[0] + i * terrain_cell_w
            y = PLAY_AREA_POS[1] + j * terrain_cell_h
            surface.blit(patch_surf, (x, y))


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

    # Restart button rect below play area
    button_width = 180
    button_height = 50
    button_rect = pygame.Rect((WIDTH - button_width) // 2, PLAY_AREA_POS[1] + PLAY_HEIGHT + 60, button_width, button_height)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and button_hovered:
                    # Restart game
                    snake = Snake()
                    food = Food(snake.positions)
                    score = 0
                    game_over = False

        if not game_over:
            snake.move()
            if snake.get_head_position() == food.position:
                snake.grow()
                score += 1
                food = Food(snake.positions)

            if snake.collided():
                game_over = True

        # Draw background
        SCREEN.fill(WHITE)

        # Draw title and score
        draw_text(SCREEN, "Elegant Snake Game", TITLE_FONT, BLACK, (WIDTH // 2, 50))
        draw_text(SCREEN, f"Score: {score}", SCORE_FONT, GRAY, (WIDTH // 2, 110))

        # Draw play area card with subtle shadow
        play_area_rect = pygame.Rect(PLAY_AREA_POS, (PLAY_WIDTH, PLAY_HEIGHT))
        shadow_surface = pygame.Surface((PLAY_WIDTH + 12, PLAY_HEIGHT + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, SHADOW, shadow_surface.get_rect(), border_radius=15)
        SCREEN.blit(shadow_surface, (PLAY_AREA_POS[0] - 6, PLAY_AREA_POS[1] - 6))

        pygame.draw.rect(SCREEN, LIGHT_GRAY, play_area_rect, border_radius=15)

        # Draw subtle terrain background
        draw_terrain(SCREEN)

        # Draw grid lines
        draw_grid(SCREEN)

        # Draw snake and food
        snake.draw(SCREEN)
        food.draw(SCREEN)

        if game_over:
            # Overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 230))
            SCREEN.blit(overlay, (0, 0))

            # Game over card
            card_width, card_height = 360, 180
            card_x = (WIDTH - card_width) // 2
            card_y = (HEIGHT - card_height) // 2
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            pygame.draw.rect(SCREEN, WHITE, card_rect, border_radius=15)
            pygame.draw.rect(SCREEN, LIGHT_GRAY, card_rect, 1, border_radius=15)

            draw_text(SCREEN, "Game Over!", GAME_OVER_FONT, BLACK, (WIDTH // 2, card_y + 50))
            draw_text(SCREEN, f"Final Score: {score}", SCORE_FONT, GRAY, (WIDTH // 2, card_y + 110))

            # Restart button
            draw_button(SCREEN, button_rect, "Restart", button_hovered)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
