import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake Class
class Snake:
   def __init__(self):
       self.body = [
           (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),  # Starting position
           (SCREEN_WIDTH // 2 - GRID_SIZE, SCREEN_HEIGHT // 2)
       ]
       self.direction = (1, 0)  # Initial direction: right
       self.color = GREEN

   def move(self):
       head_x, head_y = self.body[0]
       new_head = (head_x + self.direction[0] * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE)
       self.body.insert(0, new_head)
       self.body.pop()  # Remove tail

   def check_collision(self):
       # Check for collisions with walls and self
       head = self.body[0]
       if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
           return True
       for i in range(1, len(self.body)):  # Don't check collision with itself
           if head == self.body[i]:
               return True
       return False


# Food Class
class Food:
    def __init__(self, screen_width, screen_height, grid_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.x = int(random.randrange(0, screen_width, grid_size))
        self.y = int(random.randrange(0, screen_height, grid_size))

    def generate_new_position(self, snake_body):
        while True:
            self.x = int(random.randrange(0, self.screen_width, self.grid_size))
            self.y = int(random.randrange(0, self.screen_height, self.grid_size))
            if (self.x, self.y) not in snake_body:
                break

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.grid_size, self.grid_size))


# Initialize Game
snake = Snake()
food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)

score = 0
font = pygame.font.Font(None, 24) # Default font, size 24

running = True
clock = pygame.time.Clock()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Key Press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if snake.direction != (1, 0):  # Prevent reversing directly
            snake.direction = (-1, 0)
    elif keys[pygame.K_RIGHT]:
        if snake.direction != (-1, 0):
            snake.direction = (1, 0)
    elif keys[pygame.K_UP]:
        if snake.direction != (0, 1):
            snake.direction = (0, -1)
    elif keys[pygame.K_DOWN]:
        if snake.direction != (0, -1):
            snake.direction = (0, 1)

    # Game Logic
    if snake.check_collision():
        running = False

    snake.move()

    # Check if Snake eats Food
    if snake.body[0] == (food.x, food.y):
        food.generate_new_position(snake.body)
        score += 1

    # Drawing
    screen.fill(BLACK)
    food.draw(screen)
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    # Display Score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (5, 5))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()