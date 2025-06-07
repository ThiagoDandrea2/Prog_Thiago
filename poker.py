import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1200, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Texas Hold'em Poker - Minimal Elegant UI")

# Colors (Default Design)
WHITE = (255, 255, 255)
BG_COLOR = WHITE
BLACK = (17, 24, 39)          # #111827
GRAY = (107, 114, 128)        # #6b7280
LIGHT_GRAY = (243, 244, 246)  # #f3f4f6 for cards background
SHADOW = (220, 220, 220, 80)

# Fonts
TITLE_FONT = pygame.font.SysFont("Segoe UI", 54, bold=True)
SUBTITLE_FONT = pygame.font.SysFont("Segoe UI", 20)
TEXT_FONT = pygame.font.SysFont("Segoe UI", 18)
BUTTON_FONT = pygame.font.SysFont("Segoe UI", 24, bold=True)
SMALL_FONT = pygame.font.SysFont("Segoe UI", 14)

FPS = 60
clock = pygame.time.Clock()

# Poker Constants
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_WIDTH, CARD_HEIGHT = 80, 120
CARD_RADIUS = 12

BET_AMOUNTS = {'Fold': 0, 'Call': 10, 'Raise': 20}

# Helper: Draw rounded rectangle
def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Button class with hover effect
class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.base_color = BLACK
        self.hover_color = GRAY

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.base_color
        draw_rounded_rect(surface, self.rect, color, 10)
        txt_surf = BUTTON_FONT.render(self.text, True, WHITE)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.callback:
            self.callback()

# Card class to represent a playing card
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = RANKS.index(rank) + 2  # 2 to 14

    def draw(self, surface, x, y, face_up=True):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        draw_rounded_rect(surface, rect, LIGHT_GRAY, CARD_RADIUS)
        pygame.draw.rect(surface, BLACK, rect, 2, border_radius=CARD_RADIUS)
        if face_up:
            # Rank top-left
            txt_rank = TEXT_FONT.render(self.rank, True, BLACK)
            surface.blit(txt_rank, (x + 6, y + 6))
            # Suit bottom-right
            txt_suit = TEXT_FONT.render(self.suit, True, BLACK)
            surface.blit(txt_suit, (x + CARD_WIDTH - 22, y + CARD_HEIGHT - 26))
        else:
            # Back of card (blue pattern)
            pygame.draw.rect(surface, (30, 70, 140), rect.inflate(-8, -8), border_radius=CARD_RADIUS)
            # Simple pattern lines
            for i in range(5, CARD_WIDTH, 12):
                pygame.draw.line(surface, (255, 255, 255, 80), (x + i, y+5), (x + i - 10, y + CARD_HEIGHT-5), 2)

# Deck of cards
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

# Hand evaluation simplified
def hand_rank(cards):
    # Returns a tuple (rank_level, high_cards list) for comparison
    # rank_level from high to low: (9 Royal Flush, 8 Straight Flush ... 1 High Card)
    # For simplicity, we check pairs, trips, straights, flushes only, no full house or two pairs here; can be extended

    values = [c.value for c in cards]
    suits = [c.suit for c in cards]
    values_sorted = sorted(values, reverse=True)
    unique_vals = set(values)

    # Check flush
    flush = False
    for s in SUITS:
        if suits.count(s) >= 5:
            flush = True
            flush_suit = s
            break

    # Straight check
    vals = list(set(values))
    vals.sort()
    straight_high = None
    for i in range(len(vals) - 4):
        if vals[i+4] - vals[i] == 4:
            straight_high = vals[i+4]

    # Also check wheel straight A-2-3-4-5
    if set([14, 2, 3, 4, 5]).issubset(unique_vals):
        straight_high = 5

    # Straight flush
    if flush and straight_high is not None:
        # Check if 5 cards in same flush suit are in sequence (simplified by filtering cards)
        flush_cards = [c for c in cards if c.suit == flush_suit]
        flush_values = sorted(set([c.value for c in flush_cards]))
        for i in range(len(flush_values) - 4):
            if flush_values[i+4] - flush_values[i] == 4:
                return (8, flush_values[i+4])  # Straight flush rank level 8
        if set([14, 2, 3, 4, 5]).issubset(set(flush_values)):
            return (8, 5)

    # Four of a kind and full house and three/four/ pairs evaluation simplified
    val_counts = {v: values.count(v) for v in unique_vals}
    four = [v for v, c in val_counts.items() if c == 4]
    three = [v for v, c in val_counts.items() if c == 3]
    pairs = [v for v, c in val_counts.items() if c == 2]

    if four:
        return (7, max(four))
    if three and pairs:
        return (6, max(three))
    if flush:
        max_flush = max([c.value for c in cards if c.suit == flush_suit])
        return (5, max_flush)
    if straight_high:
        return (4, straight_high)
    if three:
        return (3, max(three))
    if len(pairs) >= 2:
        return (2, max(pairs))
    if len(pairs) == 1:
        return (1, pairs[0])
    # High card
    return (0, max(values_sorted))

# Compare two hands, returns 1 if hand1 wins, 2 if hand2 wins, 0 tie
def compare_hands(hand1, hand2):
    rank1 = hand_rank(hand1)
    rank2 = hand_rank(hand2)
    if rank1 > rank2:
        return 1
    elif rank2 > rank1:
        return 2
    else:
        return 0

# Player class
class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.bet = 0
        self.folded = False

    def reset_hand(self):
        self.hand = []
        self.bet = 0
        self.folded = False

# Main game class
class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("You"), Player("Computer")]
        self.community = []
        self.pot = 0
        self.stage = 0 # 0 pre-flop, 1 flop, 2 turn, 3 river, 4 showdown
        self.current_bet = 0
        self.turn_index = 0
        self.message = "Place your bet or Fold"

    def start_round(self):
        self.deck = Deck()
        self.community = []
        self.pot = 0
        self.stage = 0
        self.current_bet = 0
        self.turn_index = 0
        for p in self.players:
            p.reset_hand()
            p.hand = [self.deck.draw(), self.deck.draw()]

    def next_stage(self):
        if self.stage == 0:  # flop
            self.community = [self.deck.draw(), self.deck.draw(), self.deck.draw()]
            self.stage = 1
            self.message = "Flop dealt."
        elif self.stage == 1: # turn
            self.community.append(self.deck.draw())
            self.stage = 2
            self.message = "Turn dealt."
        elif self.stage == 2: # river
            self.community.append(self.deck.draw())
            self.stage = 3
            self.message = "River dealt."
        elif self.stage == 3:
            self.stage = 4  # showdown

    def handle_bet(self, player, amount):
        if amount == 'fold':
            player.folded = True
            self.message = f"{player.name} folded."
        else:
            amount = int(amount)
            bet_diff = amount - player.bet
            if bet_diff > player.chips:
                bet_diff = player.chips
            player.chips -= bet_diff
            player.bet += bet_diff
            self.pot += bet_diff
            if player.bet > self.current_bet:
                self.current_bet = player.bet
            self.message = f"{player.name} bets ${amount}."
        # For simplicity, move turn to next or stage forward if all matched or fold
        self.advance_turn_or_stage()

    def advance_turn_or_stage(self):
        self.turn_index = (self.turn_index + 1) % len(self.players)
        # If all have matched bets or folded, proceed stage or showdown
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) == 1:
            # Hand over early
            self.stage = 4
        else:
            bets = [p.bet for p in active_players]
            if len(set(bets)) == 1:
                # bets matched, progress stage
                if self.stage < 4:
                    self.next_stage()
                    for p in self.players:
                        p.bet = 0
                    self.current_bet = 0
                    self.turn_index = 0

    def get_active_player(self):
        if self.turn_index < len(self.players):
            return self.players[self.turn_index]
        return None

    def winner(self):
        # Determine the winner among players who didn't fold using hand ranking
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) == 1:
            return active_players[0]
        else:
            best_hand = None
            winner = None
            for p in active_players:
                combined = p.hand + self.community
                if best_hand is None or compare_hands(combined, best_hand) == 1:
                    best_hand = combined
                    winner = p
            return winner

    def showdown_text(self):
        w = self.winner()
        if w is None:
            return "No winner - tie"
        elif w.name == "You":
            return "You win the pot!"
        else:
            return f"{w.name} wins the pot."


###########################
# MAIN APP LOOP AND DRAWING
###########################

def draw_card(surface, card, x, y):
    card.draw(surface, x, y)

def draw_faded_card_back(surface, x, y):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(surface, LIGHT_GRAY, rect, border_radius=CARD_RADIUS)
    pygame.draw.rect(surface, GRAY, rect, 2, border_radius=CARD_RADIUS)

def draw_text_center(surface, text, font, color, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH//2, y))
    surface.blit(text_surf, text_rect)

def draw_section_card(surface, rect, title, subtitle="", content_lines=[]):
    # White card with shadow and rounded corners
    shadow_surf = pygame.Surface((rect.w + 12, rect.h + 12), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (220,220,220, 80), shadow_surf.get_rect(), border_radius=18)
    surface.blit(shadow_surf, (rect.x - 6, rect.y - 6))

    pygame.draw.rect(surface, WHITE, rect, border_radius=18)
    # Title
    t_surf = TITLE_FONT.render(title, True, BLACK)
    surface.blit(t_surf, (rect.x + 24, rect.y + 16))
    # Subtitle
    if subtitle:
        st_surf = SUBTITLE_FONT.render(subtitle, True, GRAY)
        surface.blit(st_surf, (rect.x + 26, rect.y + 76))

    # Content lines (e.g. chip counts, messages) below subtitle
    for i, line in enumerate(content_lines):
        c_surf = TEXT_FONT.render(line, True, BLACK)
        surface.blit(c_surf, (rect.x + 26, rect.y + 110 + i * 24))

def draw_button(surface, rect, text, hovered):
    radius = 14
    bg_color = BLACK if not hovered else GRAY
    txt_color = WHITE
    pygame.draw.rect(surface, bg_color, rect, border_radius=radius)
    txt_surf = BUTTON_FONT.render(text, True, txt_color)
    txt_rect = txt_surf.get_rect(center=rect.center)
    surface.blit(txt_surf, txt_rect)

def main():
    game = PokerGame()
    game.start_round()

    # Buttons for player controls
    button_texts = ["Fold", "Call $10", "Raise $20"]
    BUTTON_WIDTH = 140
    BUTTON_HEIGHT = 60
    BUTTON_SPACING = 40
    buttons = []
    button_start_x = (WIDTH - (BUTTON_WIDTH*3 + BUTTON_SPACING*2)) // 2
    button_y = HEIGHT - 100
    for i, text in enumerate(button_texts):
        rect = pygame.Rect(button_start_x + i*(BUTTON_WIDTH+BUTTON_SPACING), button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append(Button(rect.x, rect.y, rect.w, rect.h, text, None))

    running = True
    winner_announced = False

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.stage == 4 and not winner_announced:
                    # Show winner, disable input
                    winner_announced = True
                elif game.stage < 4 and game.get_active_player() == game.players[0] and not game.players[0].folded:
                    for btn, action_text in zip(buttons, button_texts):
                        if btn.rect.collidepoint(event.pos):
                            if action_text == "Fold":
                                game.handle_bet(game.players[0], 'fold')
                            elif action_text.startswith("Call"):
                                game.handle_bet(game.players[0], BET_AMOUNTS['Call'])
                            elif action_text.startswith("Raise"):
                                game.handle_bet(game.players[0], BET_AMOUNTS['Raise'])
                            winner_announced = False

        # Simple AI for computer player
        comp = game.players[1]
        if not comp.folded and game.get_active_player() == comp and game.stage < 4:
            # AI logic simple: always call if can afford, else fold
            if comp.chips >= game.current_bet - comp.bet:
                game.handle_bet(comp, game.current_bet)
            else:
                game.handle_bet(comp, 'fold')

        SCREEN.fill(BG_COLOR)

        # Draw table card with subtle shadow
        TABLE_RECT = pygame.Rect(100, 100, WIDTH-200, HEIGHT-250)
        shadow_surface = pygame.Surface((TABLE_RECT.w+20, TABLE_RECT.h+20), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (220,220,220,80), shadow_surface.get_rect(), border_radius=20)
        SCREEN.blit(shadow_surface, (TABLE_RECT.x-10, TABLE_RECT.y-10))
        pygame.draw.rect(SCREEN, WHITE, TABLE_RECT, border_radius=20)

        # Draw Title
        draw_text_center(SCREEN, "Texas Hold'em Poker", TITLE_FONT, BLACK, 50)

        # Player info card left bottom
        p1_rect = pygame.Rect(50, HEIGHT - 140, 280, 120)
        p1_lines = [
            f"Chips: ${game.players[0].chips}",
            f"Current Bet: ${game.players[0].bet}",
            f"{'Folded' if game.players[0].folded else 'Active'}"
        ]
        draw_section_card(SCREEN, p1_rect, game.players[0].name, "You", p1_lines)

        # Computer info card right bottom
        comp_rect = pygame.Rect(WIDTH - 350, HEIGHT - 140, 280, 120)
        comp_lines = [
            f"Chips: ${game.players[1].chips}",
            f"Current Bet: ${game.players[1].bet}",
            f"{'Folded' if game.players[1].folded else 'Active'}"
        ]
        draw_section_card(SCREEN, comp_rect, game.players[1].name, "Computer AI", comp_lines)

        # Pot info card top center
        pot_rect = pygame.Rect((WIDTH - 280)//2, 90, 280, 100)
        pot_lines = [f"Pot: ${game.pot}", f"Stage: {['Pre-Flop', 'Flop', 'Turn', 'River', 'Showdown'][game.stage]}"]
        draw_section_card(SCREEN, pot_rect, "Pot & Stage", "", pot_lines)

        # Draw Community Cards centered top-middle
        comm_x_start = WIDTH // 2 - ((CARD_WIDTH + 12) * max(5, len(game.community)))//2
        comm_y = 250
        for i, card in enumerate(game.community):
            card.draw(SCREEN, comm_x_start + i*(CARD_WIDTH + 12), comm_y)

        # Draw players' hole cards
        # Player (bottom left)
        p1_x_start = p1_rect.x + 20
        p1_y = p1_rect.y - CARD_HEIGHT - 20
        for i, card in enumerate(game.players[0].hand):
            card.draw(SCREEN, p1_x_start + i*(CARD_WIDTH + 10), p1_y)

        # Computer (top right), face down if stage <4
        comp_x_start = comp_rect.x + 20
        comp_y = comp_rect.y - CARD_HEIGHT - 20
        for i, card in enumerate(game.players[1].hand):
            if game.stage == 4:
                card.draw(SCREEN, comp_x_start + i*(CARD_WIDTH + 10), comp_y)
            else:
                draw_faded_card_back(SCREEN, comp_x_start + i*(CARD_WIDTH + 10), comp_y)

        # Draw message text below pot card
        msg_y = pot_rect.y + pot_rect.height + 10
        msg_surf = TEXT_FONT.render(game.message, True, GRAY)
        msg_rect = msg_surf.get_rect(center=(WIDTH//2, msg_y))
        SCREEN.blit(msg_surf, msg_rect)

        # Buttons for player if active turn and not folded and stage < showdown
        if game.get_active_player() == game.players[0] and not game.players[0].folded and game.stage < 4:
            for btn in buttons:
                btn.draw(SCREEN)

        # Show showdown messages
        if game.stage == 4:
            winner = game.winner()
            if winner:
                txt = ""
                if winner == game.players[0]:
                    txt = "You win the pot!"
                elif winner == game.players[1]:
                    txt = "Computer wins the pot."
                else:
                    txt = "Tie."
                draw_text_center(SCREEN, "Showdown", TITLE_FONT, BLACK, 550)
                draw_text_center(SCREEN, txt, SUBTITLE_FONT, GRAY, 595)
                draw_text_center(SCREEN, "Press R to restart", SUBTITLE_FONT, GRAY, 630)

        pygame.display.flip()
        clock.tick(FPS)

        keys = pygame.key.get_pressed()
        if game.stage == 4:
            if keys[pygame.K_r]:
                game.start_round()

    pygame.quit()
    sys.exit()


def draw_faded_card_back(surface, x, y):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(surface, LIGHT_GRAY, rect, border_radius=CARD_RADIUS)
    pygame.draw.rect(surface, GRAY, rect, 2, border_radius=CARD_RADIUS)
    # Simple diagonal lines pattern for back
    spacing = 8
    for i in range(-CARD_HEIGHT, CARD_WIDTH, spacing):
        pygame.draw.line(surface, GRAY, (x + i, y), (x + i + CARD_HEIGHT, y + CARD_HEIGHT), 2)


if __name__ == "__main__":
    main()

