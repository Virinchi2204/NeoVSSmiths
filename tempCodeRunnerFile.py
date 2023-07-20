import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Neo vs Smiths")

# Load background image
background = pygame.image.load("matrix_city.jpg")
background = pygame.transform.scale(background, (width, height))

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Game variables
score = 0
game_over = False
retry_delay = 2  # 2 seconds retry delay
font = pygame.font.Font(None, 36)
start_time = time.time()
game_duration = 120  # 2 minutes in seconds
spawn_delay = 3  # Delay between each new Smith spawn
max_smiths = 20  # Maximum number of Smiths on the screen
max_smith_speed = 4  # Maximum speed of Smiths
smith_speed_increase = 0.2  # Speed increase per second
smith_spawn_increase = 5  # Number of Smiths increase per second

neo_image = pygame.image.load("neo.png").convert_alpha()
smith_image = pygame.image.load("smith.png").convert_alpha()

# Neo and Smith class definitions
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
        self.speed = random.randint(2, max_smith_speed)
        self.direction = random.choice(["up", "down", "left", "right"])

    def update(self):
        if self.direction == "up":
            if self.rect.top > 0:
                self.rect.move_ip(0, -self.speed)
            else:
                self.direction = random.choice(["down", "left", "right"])
        elif self.direction == "down":
            if self.rect.bottom < height:
                self.rect.move_ip(0, self.speed)
            else:
                self.direction = random.choice(["up", "left", "right"])
        elif self.direction == "left":
            if self.rect.left > 0:
                self.rect.move_ip(-self.speed, 0)
            else:
                self.direction = random.choice(["up", "down", "right"])
        elif self.direction == "right":
            if self.rect.right < width:
                self.rect.move_ip(self.speed, 0)
            else:
                self.direction = random.choice(["up", "down", "left"])

# Create Neo and Smiths sprite groups
all_sprites = pygame.sprite.Group()
smiths = pygame.sprite.Group()
neo = Neo()
all_sprites.add(neo)

# Game loop
clock = pygame.time.Clock()
last_spawn_time = 0
last_speed_increase_time = 0
while not game_over:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                # Check collision between Neo and Smiths
                smith_hit = pygame.sprite.spritecollide(neo, smiths, True)
                if smith_hit:
                    score += 1

    # Update sprites
    all_sprites.update()

    # Check game duration
    elapsed_time = time.time() - start_time
    if elapsed_time > game_duration:
        game_over = True

    # Increase Smith speed and number of Smiths over time
    if time.time() - last_speed_increase_time >= 1:
        last_speed_increase_time = time.time()
        for smith in smiths:
            smith.speed += smith_speed_increase

    if time.time() - last_spawn_time >= 1:
        last_spawn_time = time.time()
        for _ in range(int(elapsed_time * smith_spawn_increase)):
            if len(smiths) < max_smiths:
                smith = Smith()
                all_sprites.add(smith)
                smiths.add(smith)

    # Render the game
    window.blit(background, (0, 0))
    all_sprites.draw(window)

    # Display the score and time
    score_text = font.render("Score: " + str(score), True, GREEN)
    time_text = font.render(
        "Time: " + str(int(game_duration - elapsed_time)), True, GREEN
    )
    window.blit(score_text, (10, 10))
    window.blit(time_text, (width - time_text.get_width() - 10, 10))

    # Update the game display
    pygame.display.flip()

    # Control the game speed
    clock.tick(60)

# Game over screen
game_over_text = font.render("Game Over", True, GREEN)
game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
window.blit(game_over_text, game_over_rect)

score_text = font.render("Score: " + str(score), True, GREEN)
score_rect = score_text.get_rect(center=(width // 2, height // 2 + 40))
window.blit(score_text, score_rect)

play_again_text = font.render("Play Again", True, GREEN)
play_again_rect = play_again_text.get_rect(center=(width // 2, height // 2 + 100))
window.blit(play_again_text, play_again_rect)

exit_text = font.render("Exit", True, GREEN)
exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 160))
window.blit(exit_text, exit_rect)

pygame.display.flip()

retry_button_clicked = False
exit_button_clicked = False

while not retry_button_clicked and not exit_button_clicked:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            retry_button_clicked = True
            exit_button_clicked = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_rect.collidepoint(mouse_pos):
                retry_button_clicked = True
            elif exit_rect.collidepoint(mouse_pos):
                exit_button_clicked = True
if retry_button_clicked:
    # Reset game variables for a retry
    score = 0
    game_over = False
    start_time = time.time()
    all_sprites.empty()
    smiths.empty()

    # Create Neo and Smiths sprite groups for the retry
    all_sprites.add(neo)
elif exit_button_clicked:
    game_over = True

# Quit the game
pygame.quit()

