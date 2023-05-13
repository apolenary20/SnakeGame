import pygame
from random import randint

class Level:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.obstacles = []

    def generate_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            obstacle_position = (randint(0, self.height // self.cell_size - 1), randint(0, self.width // self.cell_size - 1))
            self.obstacles.append(obstacle_position)

    def render_obstacles(self, screen):
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (128, 128, 128), (obstacle[1] * self.cell_size, obstacle[0] * self.cell_size, self.cell_size, self.cell_size))

    def is_obstacle(self, position):
        return position in self.obstacles
