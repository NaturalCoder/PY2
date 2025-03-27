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
       for i in range(1, len(self.body)):
           if self.body[0] == self.body[i]:
               return True
       return False


# Food Class
class Food:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, GRID_SIZE, GRID_SIZE))

    def generate_new_position(self, snake_body):
        while True:
            self.x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            self.y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            if (self.x, self.y) not in snake_body:
                break

# Initialize
snake = Snake()
food = Food()

# Game Loop
running = True
score = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.direction = (-1, 0)
    elif keys[pygame.K_RIGHT]:
        snake.direction = (1, 0)
    elif keys[pygame.K_UP]:
        snake.direction = (0, -1)
    elif keys[pygame.K_DOWN]:
        snake.direction = (0, 1)

    # Check for Collision
    if snake.check_collision():
        running = False

    # Check if Snake Collies with Food
    if snake.body[0] == (food.x, food.y):
        score += 1
        food.generate_new_position(snake.body)
        snake.body.insert(0, (food.x, food.y))  # Grow the snake

    else:
        snake.move() # move snake, removing the tail if no food is eaten

    # Drawing
    screen.fill(BLACK)
    food.draw(screen)

    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    # Display Score
    score_text = pygame.font.Font(None, 0).render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (5, 5))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()