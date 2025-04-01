import pygame
import random
import "../../
import time

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")



# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake and food settings
snake_block = 20
food_size = snake_block
snake_speed = 15

# Initialize clock
clock = pygame.time.Clock()


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, GREEN, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    font_style = pygame.font.SysFont(None, 50)
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [width/6, height/3])

# Main game loop
game_over = False
game_close = False

while not game_over:
    while not game_close:
        # Game logic here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = True

        # Snake movement and collision detection
        x1 = 0  # Start position (you can modify these)
        y1 = 0  # Start position (you can modify these)

        # Move the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1 -= snake_block
            elif event.key == pygame.K_RIGHT:
                x1 += snake_block
            elif event.key == pygame.K_UP:
                y1 -= snake_block
            elif event.key == pygame.K_DOWN:
                y1 += snake_block

        # Check if food is eaten
        foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

        window.fill(BLACK)
        pygame.draw.rect(window, RED, [foodx, foody, food_size, food_size])

        # Draw the snake
        pygame.draw.rect(window, GREEN, [x1, y1, snake_block, snake_block])
        pygame.display.update()

        # Check if snake hits itself or walls
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

    # Game over message
    while game_close:
        window.fill(BLACK)
        message("You Lost! Press C to Play Again", RED)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game_over = False
                    game_close = False

# Close the game
pygame.quit()