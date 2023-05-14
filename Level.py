import pygame

class Level:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.obstacles = []

    def generate_obstacles(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for y, line in enumerate(lines):
                for x, char in enumerate(line):
                    if char == '#':
                        obstacle_position = (y, x)
                        self.obstacles.append(obstacle_position)

    def render_obstacles(self, screen):
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (128, 128, 128), (obstacle[1] * self.cell_size, obstacle[0] * self.cell_size, self.cell_size, self.cell_size))

    def is_obstacle(self, position):
        return position in self.obstacles
