import sys

from AsteroidManager import AsteroidManager
from GameObjects import *
import os


# Функция для установки позиции окна в левый верхний угол
def set_window_position(x, y):
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

# Button class to handle the buttons in the menu
class Button:
    def __init__(self, text, position, size=(200, 50), font_size=36):
        self.text = text
        self.position = position
        self.size = size
        self.font = pygame.font.SysFont(None, font_size)
        self.color = (255, 255, 255)
        self.hover_color = (200, 200, 200)
        self.button_rect = pygame.Rect(position, size)

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.button_rect.collidepoint(mouse_pos) else self.color

        pygame.draw.rect(window, color, self.button_rect)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        window.blit(text_surf, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


# Main Menu class to display the menu and handle button interactions
class MainMenu:
    def __init__(self, window, program):
        self.window = window
        self.program = program
        self.start_button = Button("Start Game", (300, 200))
        self.settings_button = Button("Settings", (300, 300))
        self.quit_button = Button("Quit Game", (300, 400))

    def run(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check for button clicks
            if self.start_button.is_clicked():
                menu_running = False
                self.program.start_game()
            if self.settings_button.is_clicked():
                menu_running = False
                self.program.open_settings()
            if self.quit_button.is_clicked():
                pygame.quit()
                sys.exit()

            self.draw()
            pygame.display.update()

    def draw(self):
        self.window.fill((50, 50, 50))  # Menu background color
        self.start_button.draw(self.window)
        self.settings_button.draw(self.window)
        self.quit_button.draw(self.window)


# Settings Menu class to change screen resolution
class SettingsMenu:
    def __init__(self, window, program):
        self.window = window
        self.program = program
        self.resolution_buttons = [
            Button("800x600", (300, 200)),
            Button("1024x768", (300, 300)),
            Button("1280x720", (300, 400)),
        ]
        self.back_button = Button("Back", (300, 500))

    def run(self):
        settings_running = True
        while settings_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check for resolution changes
            if self.resolution_buttons[0].is_clicked():
                self.program.set_resolution((800, 600))
            if self.resolution_buttons[1].is_clicked():
                self.program.set_resolution((1024, 768))
            if self.resolution_buttons[2].is_clicked():
                self.program.set_resolution((1280, 720))

            # Back to main menu
            if self.back_button.is_clicked():
                settings_running = False
                self.program.open_menu()

            self.draw()
            pygame.display.update()

    def draw(self):
        self.window.fill((50, 50, 50))  # Settings background color
        for button in self.resolution_buttons:
            button.draw(self.window)
        self.back_button.draw(self.window)


# Main Program class that manages the game, menu, and settings
class MainProgram:
    def __init__(self):
        set_window_position(0, 0)
        pygame.init()
        self.winsize = (800, 600)
        self.window = pygame.display.set_mode(self.winsize, pygame.RESIZABLE)

        # Initialize menus
        self.menu = MainMenu(self.window, self)
        self.settings_menu = SettingsMenu(self.window, self)
        self.game = MainGame(self.window)

        # Initially open the main menu
        self.menu.run()

    def open_menu(self):
        self.menu.run()

    def open_settings(self):
        self.settings_menu.run()

    def start_game(self):
        self.game.run()

    def set_resolution(self, resolution):
        self.winsize = resolution
        self.window = pygame.display.set_mode(self.winsize)


class MainGame:
    def __init__(self, window):
        self.window = window
        self.score = 0
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.keys = None

        self.player = Player("Images/Player.png")
        self.player_s = pygame.sprite.Group()
        self.player_s.add(self.player)

        self.asteroids = AsteroidManager(self)

        self.textlayer = TextLayer("Hello", position=(0, 0))

    def update(self):
        self.player.update(self.keys, self.dt)
        self.asteroids.update(self.dt)
        self.check_collisions()
        self.textlayer.update_text(str(self.score))

    def check_collisions(self):
        if self.player.check_collision(self.asteroids.get_asteroid_group()):
            self.asteroids.stop()
            self.player.stop()
        for b in self.player.get_bullets_group():
            b.check_collision(self.asteroids.get_asteroid_group())

    def draw(self):
        self.window.fill((10, 10, 25))
        self.player_s.draw(self.window)
        self.player.bullets.draw(self.window)
        self.asteroids.draw(self.window)
        self.textlayer.draw(self.window)
        pygame.display.update()

    def run(self):
        while True:
            self.keys = pygame.key.get_pressed()
            self.dt = self.clock.tick(FPS) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.update()
            self.draw()
            if pygame.key.get_pressed()[pygame.K_r]:
                self.restart()

    def restart(self):
        self.score = 0
        self.player = Player("Images/Player.png")

        self.player_s = pygame.sprite.Group()
        self.player_s.add(self.player)

        self.asteroids = AsteroidManager(self)


if __name__ == "__main__":
    prog = MainProgram()
