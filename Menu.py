import pygame
import sys
from Snake import Snake
from random import randint
from Game import Game

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 46)
        self.options = ['Play', 'Highscores', 'Quit']
        self.selected_option = 0

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2, 150 + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]

    def run(self):
        while True:
            action = self.process_input()
            if action:
                return action
            self.draw()

# (Класс Game остается без изменений)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Snake Game')
    menu = Menu(screen)
    while True:
        action = menu.run()
        if action == 'Play':
            game = Game()
            game.run()
        elif action == 'Highscores':
            # Здесь можно отобразить экран с рекордами
            pass
        else:
            pygame.quit()
            sys.exit()
