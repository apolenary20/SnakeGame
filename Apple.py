
class Apple:

    def __init__(self, position):
        self.position = position
        self.color = (255, 0, 0)

    def effect_on_snake(self, snake, game):
        snake.grow()