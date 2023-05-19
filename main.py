import pygame
import sys
from Game import Game
import shelve
from Menu import Menu


def show_settings(screen):
    '''
    Отображает экран настроек, где пользователь может выбрать уровень сложности.

    Args:
        screen (Surface): Объект Surface из pygame, на котором отображаются настройки.

    Returns:
        str: Выбранный уровень сложности.
    '''
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
    '''
    Отображает экран с высокими счетами.

    Args:
        screen (Surface): Объект Surface из pygame, на котором отображаются высокие счеты.
    '''
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
    '''
    Главная точка входа в приложение.
    Инициализирует pygame, создает экран и объект меню, а затем входит в основной цикл игры.
    '''
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
