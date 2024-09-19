import sys
import array
import moderngl
import pygame

from config import FPS

from GameObjects import *
from AsteroidManager import AsteroidManager

W, H = 800, 600


class MainGame:
    def __init__(self):
        pygame.init()

        self.score = 0
        self.dt = 0
        self.keys = []

        self.clock = pygame.time.Clock()

        self.window = pygame.display.set_mode((W, H), pygame.FULLSCREEN)

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
    game = MainGame()
    game.run()
