import pygame

class Level:
    '''
    Класс Level представляет уровень в игре "Snake Game". Он содержит информацию о препятствиях на игровом поле.
    '''
    def __init__(self, width, height, cell_size):
        '''
        Инициализация нового объекта Level.

        Args:
            width (int): Ширина игрового поля.
            height (int): Высота игрового поля.
            cell_size (int): Размер ячейки на игровом поле.
        '''
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.obstacles = []

    def generate_obstacles(self, filename):
        '''
        Генерация препятствий на основе текстового файла. Символ '#' в файле обозначает препятствие.

        Args:
            filename (str): Имя текстового файла, из которого загружаются препятствия.
        '''
        with open(filename, 'r') as file:
            lines = file.readlines()
            for y, line in enumerate(lines):
                for x, char in enumerate(line):
                    if char == '#':
                        obstacle_position = (y, x)
                        self.obstacles.append(obstacle_position)

    def render_obstacles(self, screen):
        '''
        Отрисовка препятствий на игровом поле.

        Args:
            screen (Surface): Объект Surface из pygame, на котором отрисовываются препятствия.
        '''
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (128, 128, 128), (obstacle[1] * self.cell_size, obstacle[0] * self.cell_size, self.cell_size, self.cell_size))

    def is_obstacle(self, position):
        '''
        Проверка, является ли заданная позиция препятствием.

        Args:
            position (tuple): Координаты позиции на игровом поле.

        Returns:
            bool: True, если позиция является препятствием, иначе False.
        '''
        return position in self.obstacles
