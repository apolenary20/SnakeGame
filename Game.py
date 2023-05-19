import pygame
import sys
from Snake import Snake
from random import randint
import shelve
from Level import Level
from Apple import Apple
from Banana import Banana

class Game:
    '''
    Основной класс игры "Snake Game". Он контролирует все основные механики игры, включая обработку ввода,
    обновление состояния игры, отображение объектов на экране и сохранение рекордов.
    '''
    def __init__(self, name, difficulty='Easy'):
        '''
        Инициализация нового объекта Game.

        Args:
            name (str): Имя игрока.
            difficulty (str, optional): Уровень сложности игры. Может быть 'Easy', 'Medium' или 'Hard'. По умолчанию 'Easy'.
        '''
        self.name = name
        self.difficulty = difficulty
        pygame.init()
        self.width, self.height = 640, 480
        self.cell_size = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.snake = Snake((self.height // 2 // self.cell_size, self.width // 4 // self.cell_size), (0, 1))
        self.running = True
        self.level = Level(self.width, self.height, self.cell_size)


        if self.difficulty == 'Easy':
            self.snake_speed = 5
            self.level.generate_obstacles('level1.txt')
        elif self.difficulty == 'Medium':
            self.snake_speed = 10
            self.level.generate_obstacles('level2.txt')
        elif self.difficulty == 'Hard':
            self.snake_speed = 15
            self.level.generate_obstacles('level3.txt')
        self.generate_bonus()

    def generate_bonus(self):
        '''
        Генерация бонусного предмета (яблока или банана) в случайной позиции на игровом поле.
        '''
        if randint(0,1) == 0:
            bonus_class = Apple
        else:
            bonus_class = Banana
        while True:
            self.bonus = bonus_class((randint(0, self.height // self.cell_size - 1), randint(0, self.width // self.cell_size - 1)))
            if self.bonus.position not in self.snake.get_segments() and self.bonus.position not in self.level.obstacles:
                break

    def process_input(self):
        '''
        Обработка ввода с клавиатуры. Реагирует на клавиши вверх, вниз, влево и вправо для управления змейкой,
        а также на событие выхода из игры.
        '''
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
        '''
        Обновление состояния игры, включая перемещение змейки, проверку на столкновение с бонусами и проверку на столкновения.
        '''
        self.snake.move(next_position=self.get_next_snake_position())

        if self.snake.get_head() == self.bonus.position:
            self.bonus.effect_on_snake(self.snake, self)
            self.generate_bonus()

        if self.check_collision():
            self.running = False

    def check_collision(self):
        '''
        Проверка столкновения головы змейки с ее телом или препятствиями на игровом поле.

        Returns:
            bool: True, если произошло столкновение, иначе False.
        '''
        head = self.snake.get_head()
        return (
                self.snake.is_collision() or
                self.level.is_obstacle(head)
        )

    def render(self):
        '''
        Отрисовка всех объектов на игровом поле, включая змейку, бонусы и препятствия.
        '''
        self.screen.fill((0, 0, 0))

        for segment in self.snake.get_segments():
            pygame.draw.rect(self.screen, (255, 255, 255), (segment[1] * self.cell_size, segment[0] * self.cell_size, self.cell_size, self.cell_size))

        pygame.draw.rect(self.screen, self.bonus.color, (self.bonus.position[1] * self.cell_size, self.bonus.position[0] * self.cell_size, self.cell_size, self.cell_size))
        self.level.render_obstacles(self.screen)

        pygame.display.flip()

    def get_score(self):
        '''
        Получение текущего счета игрока, который равен длине змейки.

        Returns:
            int: Длина змейки.
        '''
        return self.snake.get_length()

    def run(self):
        '''
        Запуск основного игрового цикла, который обрабатывает ввод, обновляет состояние игры и отрисовывает объекты на экране.
        '''
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(self.snake_speed)

        self.save_highscore()
        pygame.quit()
        sys.exit()

    def save_highscore(self):
        '''
        Сохранение текущего рекорда игрока в таблицу рекордов, которая хранит топ-10 рекордов.
        '''
        with shelve.open('highscores.db', 'c') as db:
            highscores = db.get('highscores', [])
            highscores.append((self.name, self.get_score()))
            highscores.sort(key=lambda x: x[1], reverse=True)
            db['highscores'] = highscores[:10]

    def get_next_snake_position(self):
        '''
        Вычисление следующей позиции змейки на основе текущего направления ее движения.

        Returns:
            tuple: Следующая позиция змейки в формате (y, x).
        '''
        self.snake.block_direction = False
        next_y = self.snake.segments[0][0] + self.snake.direction[0]
        next_x = self.snake.segments[0][1] + self.snake.direction[1]
        if next_y > self.height // self.cell_size:
            next_y = 0
        elif next_y < 0:
            next_y = self.height // self.cell_size

        if next_x > self.width // self.cell_size:
            next_x = 0
        elif next_x < 0:
            next_x = self.width // self.cell_size

        next_position = (next_y, next_x)
        return next_position
