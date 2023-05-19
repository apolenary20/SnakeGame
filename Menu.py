import pygame
import sys
from Game import Game
import shelve

class Menu:
    '''
    Класс Menu представляет меню в игре "Snake Game".
    Он предоставляет интерфейс для ввода имени игрока и выбора различных опций, таких как игра, рекорды, настройки и выход.
    '''
    def __init__(self, screen):
        '''
        Инициализация нового объекта Menu.

        Args:
            screen (Surface): Объект Surface из pygame, на котором будет отображаться меню.
        '''
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 46)
        self.options = ['Play', 'Highscores', 'Settings', 'Quit']

        self.selected_option = 0
        self.name = ''

    def draw(self):
        '''
        Отрисовка меню на экране.
        '''
        self.screen.fill((0, 0, 0))

        text = self.font.render("Enter name: " + self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(text, text_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width // 2, 150 + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()


    def process_input(self):
        '''
        Обработка пользовательского ввода в меню.
        Позволяет перемещаться между опциями и выбирать их.

        Returns:
            str: Выбранная опция меню или None, если опция не выбрана.
        '''
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
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif 'a' <= pygame.key.name(event.key) <= 'z' and len(pygame.key.name(event.key)) == 1:
                    self.name += pygame.key.name(event.key)

    def run(self):
        '''
        Запускает цикл меню, который ожидает ввода от пользователя и отрисовывает меню.

        Returns:
            str: Выбранная опция меню.
        '''
        while True:
            action = self.process_input()
            if action:
                return action
            self.draw()

