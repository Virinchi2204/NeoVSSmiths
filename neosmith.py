import pygame
import random
import time
import math
import sys


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
game_won = False
retry_delay = 2  # 2 seconds retry delay
font = pygame.font.Font(None, 36)
start_time = time.time()
game_duration = 60  # 2 minutes in seconds

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

# Create Neo and Smiths sprite groups
all_sprites = pygame.sprite.Group()
smiths = pygame.sprite.Group()
neo = Neo()
all_sprites.add(neo)

# Game loop
clock = pygame.time.Clock()
while not game_over:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                # Check collision between Neo and Smiths
                smith_hit = pygame.sprite.spritecollide(neo, smiths, True)
                score += len(smith_hit)

    # Update sprites
    all_sprites.update()

    # Check game duration
    elapsed_time = time.time() - start_time
    if elapsed_time > game_duration:
        game_over = True
    # Increase maximum number of Smiths over time
    if elapsed_time < 10:  # Increase to 30 seconds, adjust as needed
        max_smiths = 10
    elif elapsed_time < 20:  # Increase to 60 seconds, adjust as needed
        max_smiths = 20
    elif elapsed_time < 30:  # Increase to 90 seconds, adjust as needed
        max_smiths = 40
    else:
        max_smiths = 80

    while len(smiths) < max_smiths:
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up":
            smith = Smith()
            smith.rect.x = random.randint(0, width - smith.rect.width)
            smith.rect.y = -smith.rect.height
            all_sprites.add(smith)
            smiths.add(smith)
        elif direction == "down":
            smith = Smith()
            smith.rect.x = random.randint(0, width - smith.rect.width)
            smith.rect.y = height
            all_sprites.add(smith)
            smiths.add(smith)
        elif direction == "left":
            smith = Smith()
            smith.rect.x = -smith.rect.width
            smith.rect.y = random.randint(0, height - smith.rect.height)
            all_sprites.add(smith)
            smiths.add(smith)
        elif direction == "right":
            smith = Smith()
            smith.rect.x = width
            smith.rect.y = random.randint(0, height - smith.rect.height)
            all_sprites.add(smith)
            smiths.add(smith)
    
    

    # Check if Neo is covered by 5 or more Smiths
    # if len(smiths) >= 5 and all(sprite.rect.colliderect(neo.rect) for sprite in smiths):
    #     game_over = True
    #     game_won=False
    if len(pygame.sprite.spritecollide(neo, smiths, False)) >= max_smiths//2:
        game_over = True
        game_won = False
    if elapsed_time >= game_duration:
        game_won = True

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
def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_won and play_again_rect.collidepoint(mouse_pos):
                    return True
                elif not game_won and retry_rect.collidepoint(mouse_pos):
                    return True
                elif exit_rect.collidepoint(mouse_pos):
                    return False

        window.blit(background, (0, 0))

        if game_won:
            game_over_text = font.render("You won, The One", True, GREEN)
        else:
            game_over_text = font.render("You lose Mr. Anderson", True, GREEN)

        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        window.blit(game_over_text, game_over_rect)

        score_text = font.render("Your score is: " + str(score), True, GREEN)
        score_rect = score_text.get_rect(center=(width // 2, height // 2 + 40))
        window.blit(score_text, score_rect)

        if game_won:
            play_again_text = font.render("Play Again", True, GREEN)
            play_again_rect = play_again_text.get_rect(center=(width // 2, height // 2 + 100))
            window.blit(play_again_text, play_again_rect)
        else:
            retry_text = font.render("Retry", True, GREEN)
            retry_rect = retry_text.get_rect(center=(width // 2, height // 2 + 100))
            window.blit(retry_text, retry_rect)

        exit_text = font.render("Exit", True, GREEN)
        exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 160))
        window.blit(exit_text, exit_rect)

        pygame.display.flip()

# Call the game over screen
if game_over_screen():
    # Restart the game
    import neosmith
else:
    # Return to the home page
    import home