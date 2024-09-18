import random
import pygame
from GameObjects import Big_Asteroid


class AsteroidManager:
    def __init__(self, game):
        self.asteroids_s = pygame.sprite.Group()

        self.spawn_points = [
            pygame.Vector2(0, -100), pygame.Vector2(100, -100),
            pygame.Vector2(300, -100), pygame.Vector2(200, -100),
            pygame.Vector2(400, -100), pygame.Vector2(500, -100),
            pygame.Vector2(600, -100)
        ]

        self.time = 0
        self.spawn_time = 5
        self.game = game

    def get_random_spawn_point(self):
        return random.choice(self.spawn_points)

    def spawn_new_asteroid(self):
        new_asteroid = Big_Asteroid("Images/Big_Asteroid.png", self.get_asteroid_group(), self.game)
        new_asteroid.setPos(self.get_random_spawn_point().copy())
        self.asteroids_s.add(new_asteroid)

    def get_asteroid_group(self):
        return self.asteroids_s

    def update(self, dt):
        self.time += dt
        if self.time >= self.spawn_time:
            self.spawn_new_asteroid()
            self.time = 0
        self.asteroids_s.update(dt)

    def draw(self, window):
        self.asteroids_s.draw(window)

    def stop(self):
        self.spawn_time = 100000
        for a in self.asteroids_s:
            a.velocity *= 0
            a.rot_angle = 0
