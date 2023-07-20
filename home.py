import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Neo vs Smiths - Home Page")

# Load background image
background = pygame.image.load("neoandsmith.jpg")
background = pygame.transform.scale(background, (width, height))

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Home page loop
def home_page():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    return True

        window.blit(background, (0, 0))

        # Draw the play button
        play_button_text = font.render("Play", True, GREEN)
        play_button_rect = play_button_text.get_rect(center=(width // 2, height // 2))
        window.blit(play_button_text, play_button_rect)

        pygame.display.flip()

# Call the home page loop
if home_page():
    # Run the game
    import neosmith
