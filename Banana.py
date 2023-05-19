

class Banana:
    def __init__(self, position):
        self.position = position
        self.color = (255, 255, 0)

    def effect_on_snake(self, snake, game):
        game.snake_speed += 1