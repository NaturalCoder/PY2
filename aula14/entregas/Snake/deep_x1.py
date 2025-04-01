import pygame
import random
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

x1 = width / 2
y1 = height / 2

snake_list = []
length_of_snake = 4

foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

x1_change = 0
y1_change = 0
direction = "right"

while not game_over:
    while game_close:
        window.fill(BLACK)
        message("You Lost! Score: " + str(length_of_snake - 4), RED)
        message("Play Again!", GREEN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:
                    # Reset the game
                    x1 = width / 2
                    y1 = height / 2
                    snake_list = []
                    length_of_snake = 4
                    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
                    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
                    x1_change = 0
                    y1_change = 0
                    direction = "right"
                    game_over = False
                    game_close = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != "right":
                x1_change = -snake_block
                y1_change = 0
                direction = "left"
            elif event.key == pygame.K_RIGHT and direction != "left":
                x1_change = snake_block
                y1_change = 0
                direction = "right"
            elif event.key == pygame.K_UP and direction != "down":
                y1_change = -snake_block
                x1_change = 0
                direction = "up"
            elif event.key == pygame.K_DOWN and direction != "up":
                y1_change = snake_block
                x1_change = 0
                direction = "down"

    if game_over:
        break

    # Update snake position
    x1 += x1_change
    y1 += y1_change
    snake_Head = []
    snake_Head.append(x1)
    snake_Head.append(y1)
    snake_list.append(snake_Head)

    # Check if food is eaten
    if x1 == foodx and y1 == foody:
        foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
    else:
        snake_list.pop()

    # Check for collisions
    for x in snake_list[:-1]:
        if x == snake_Head:
            game_close = True

    window.fill(BLACK)
    pygame.draw.rect(window, RED, [foodx, foody, food_size, food_size])
    our_snake(snake_block, snake_list)
    pygame.display.update()

    # Set the speed of the game
    clock.tick(snake_speed)

# Close the game
pygame.quit()