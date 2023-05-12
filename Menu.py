import pygame
import sys
from Game import Game
import shelve

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 46)
        self.options = ['Play', 'Highscores', 'Settings', 'Quit']

        self.selected_option = 0
        self.name = ''

    def draw(self):
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
        while True:
            action = self.process_input()
            if action:
                return action
            self.draw()

def show_settings(screen):
    font = pygame.font.Font(None, 46)
    settings_options = ['Easy', 'Medium', 'Hard']
    selected_option = 0
    done = False

    while not done:
        screen.fill((0, 0, 0))

        for i, option in enumerate(settings_options):
            color = (255, 255, 255) if i == selected_option else (128, 128, 128)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(640 // 2, 150 + i * 50))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(settings_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(settings_options)
                elif event.key == pygame.K_RETURN:
                    return settings_options[selected_option]
                elif event.key == pygame.K_ESCAPE:
                    done = True


def show_highscores(screen):
    font = pygame.font.Font(None, 35)
    done = False

    while not done:
        screen.fill((0, 0, 0))
        with shelve.open('highscores.db', 'r') as db:
            highscores = db.get('highscores', [])
            if not highscores:
                text = font.render('No highscores yet!', True, (255, 255, 255))
                text_rect = text.get_rect(center=(640 // 2, 50))
                screen.blit(text, text_rect)
            else:
                for i, (name, score) in enumerate(highscores):
                    text = font.render(f'{i + 1}. {name}: {score}', True, (255, 255, 255))
                    text_rect = text.get_rect(center=(640 // 2, 50 + i * 35))
                    screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Snake Game')
    menu = Menu(screen)
    flag = True
    difficulty = 'Easy'
    while True:
        action = menu.run()
        if action == 'Play':
            game = Game(menu.name, difficulty)
            game.run()
        elif action == 'Highscores':
            show_highscores(screen)
        elif action == 'Settings':
            difficulty = show_settings(screen)
        else:
            pygame.quit()
            sys.exit()

