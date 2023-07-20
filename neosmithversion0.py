import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Neo vs Smiths")

# ... (rest of the previous code remains the same) ...
# Load background image
background = pygame.image.load("matrix_city.jpg")
background = pygame.transform.scale(background, (width, height))

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

score = 0
game_over = False
game_won = False
retry_delay = 2  # 2 seconds retry delay
font = pygame.font.Font(None, 36)
start_time = time.time()
game_duration = 120  # 2 minutes in seconds

neo_image = pygame.image.load("neo.png").convert_alpha()
smith_image = pygame.image.load("smith.png").convert_alpha()

class Neo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(neo_image, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self):
        # Move Neo with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.rect.move_ip(0, 5)
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.move_ip(5, 0)

class Smith(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(smith_image, (60, 90))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.speed = random.randint(2, 4)

    def update(self):
        # Smith actively chases Neo
        dx = neo.rect.x - self.rect.x
        dy = neo.rect.y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Function for the home screen
def home_screen():
    global current_screen, game_active
    window.fill(WHITE)

    # Draw buttons
    play_button = pygame.Rect(250, 200, 300, 100)
    high_scores_button = pygame.Rect(250, 350, 300, 100)
    pygame.draw.rect(window, GREEN, play_button)
    pygame.draw.rect(window, GREEN, high_scores_button)

    # Draw text on buttons
    font = pygame.font.Font(None, 48)
    play_text = font.render("Play", True, WHITE)
    high_scores_text = font.render("High Scores", True, WHITE)
    window.blit(play_text, (350, 235))
    window.blit(high_scores_text, (275, 385))

    pygame.display.flip()

    while current_screen == "home":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                current_screen = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    game_screen()
                elif high_scores_button.collidepoint(mouse_pos):
                    high_scores_screen()

# Function for the game screen
def game_screen():
    global current_screen, game_active, score, game_over, game_won, start_time, all_sprites, smiths, neo
    all_sprites.empty()
    smiths.empty()
    score = 0
    game_over = False
    game_won = False
    start_time = time.time()
    neo = Neo()
    all_sprites.add(neo)

    while not game_over:
        # ... (rest of the game loop remains the same) ...

    # Game over screen
    if game_won:
        # ... (rest of the code remains the same) ...
        while not retry_button_clicked and not exit_button_clicked:
            for event in pygame.event.get():
                # ... (rest of the event handling remains the same) ...

        if retry_button_clicked:
            game_screen()
        elif exit_button_clicked:
            current_screen = "home"

    else:
        # ... (rest of the code remains the same) ...
        while not retry_button_clicked and not exit_button_clicked:
            for event in pygame.event.get():
                # ... (rest of the event handling remains the same) ...

        if retry_button_clicked:
            game_screen()
        elif exit_button_clicked:
            current_screen = "home"

# Function for the high scores screen
def high_scores_screen():
    global current_screen
    window.fill(WHITE)

    # ... (implement displaying high scores here) ...

    # Return to the home screen when the user clicks the Exit button
    current_screen = "home"

    pygame.display.flip()

# Game variables for managing game states
current_screen = "home"
game_active = True

# Main game loop
while game_active:
    if current_screen == "home":
        home_screen()
    elif current_screen == "game":
        game_screen()

# Quit the game
pygame.quit()
