import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont('Arial', 25)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 50)

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = [1, 0]
        self.grow = False

    def move(self):
        new_head = (self.body[0][0] + self.direction[0], 
                   self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def check_collision(self):
        head = self.body[0]
        return (head in self.body[1:] or 
                head[0] < 0 or head[0] >= GRID_COUNT or 
                head[1] < 0 or head[1] >= GRID_COUNT)

def main():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = Snake()
    food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
    score = 0
    game_over = False
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    snake = Snake()
                    food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
                    score = 0
                    game_over = False
                if not paused and not game_over:
                    if event.key == pygame.K_UP and snake.direction != [0, 1]:
                        snake.direction = [0, -1]
                    if event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                        snake.direction = [0, 1]
                    if event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                        snake.direction = [-1, 0]
                    if event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                        snake.direction = [1, 0]

        screen.fill(BLACK)

        if not game_over and not paused:
            snake.move()
            
            if snake.check_collision():
                game_over = True

            if snake.body[0] == food:
                snake.grow = True
                score += 1
                while food in snake.body:
                    food = (random.randint(0, GRID_COUNT-1), 
                           random.randint(0, GRID_COUNT-1))

        # Draw food
        pygame.draw.rect(screen, RED, 
                        (food[0]*GRID_SIZE, food[1]*GRID_SIZE, 
                         GRID_SIZE-1, GRID_SIZE-1))
        
        # Draw snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN,
                           (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE,
                            GRID_SIZE-1, GRID_SIZE-1))

        # Display score
        score_text = FONT.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = GAME_OVER_FONT.render('GAME OVER!', True, WHITE)
            restart_text = FONT.render('Press R to Restart', True, WHITE)
            screen.blit(game_over_text, 
                       (WINDOW_SIZE//2 - game_over_text.get_width()//2, 
                        WINDOW_SIZE//2 - 50))
            screen.blit(restart_text,
                       (WINDOW_SIZE//2 - restart_text.get_width()//2,
                        WINDOW_SIZE//2 + 10))

        if paused:
            pause_text = GAME_OVER_FONT.render('PAUSED', True, WHITE)
            screen.blit(pause_text,
                       (WINDOW_SIZE//2 - pause_text.get_width()//2,
                        WINDOW_SIZE//2))

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()


