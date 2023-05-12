import pygame
import sys
from Snake import Snake
from random import randint
import shelve

class Game:
    def __init__(self, name, difficulty='Easy'):
        self.name = name
        self.difficulty = difficulty

        if self.difficulty == 'Easy':
            self.snake_speed = 5
        elif self.difficulty == 'Medium':
            self.snake_speed = 10
        elif self.difficulty == 'Hard':
            self.snake_speed = 15

        pygame.init()
        self.width, self.height = 640, 480
        self.cell_size = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.snake = Snake((self.height // 2 // self.cell_size, self.width // 4 // self.cell_size), (0, 1))
        self.running = True
        self.bonus = self.generate_bonus()

    def generate_bonus(self):
        while True:
            bonus_position = (randint(0, self.height // self.cell_size - 1), randint(0, self.width // self.cell_size - 1))
            if bonus_position not in self.snake.get_segments():
                return bonus_position

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and self.snake.direction != (-1, 0):
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_UP and self.snake.direction != (1, 0):
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_LEFT and self.snake.direction != (0, 1):
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_RIGHT and self.snake.direction != (0, -1):
                    self.snake.change_direction((0, 1))

    def update(self):
        self.snake.move()

        if self.snake.get_head() == self.bonus:
            self.snake.grow()
            self.bonus = self.generate_bonus()

        if self.check_collision():
            self.running = False

    def check_collision(self):
        head = self.snake.get_head()
        return (
            head[0] < 0 or head[0] * self.cell_size >= self.height or
            head[1] < 0 or head[1] * self.cell_size >= self.width or
            self.snake.is_collision()
        )

    def render(self):
        self.screen.fill((0, 0, 0))

        for segment in self.snake.get_segments():
            pygame.draw.rect(self.screen, (255, 255, 255), (segment[1] * self.cell_size, segment[0] * self.cell_size, self.cell_size, self.cell_size))

        pygame.draw.rect(self.screen, (255, 0, 0), (self.bonus[1] * self.cell_size, self.bonus[0] * self.cell_size, self.cell_size, self.cell_size))

        pygame.display.flip()

    def get_score(self):
        return self.snake.get_length()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(self.snake_speed)

        self.save_highscore()
        pygame.quit()
        sys.exit()

    def save_highscore(self):
        with shelve.open('highscores.db', 'c') as db:
            highscores = db.get('highscores', [])
            highscores.append((self.name, self.get_score()))
            highscores.sort(key=lambda x: x[1], reverse=True)
            db['highscores'] = highscores[:10]
