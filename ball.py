import pygame
from random import randint


# Classe representando a bola
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill("black")
        self.image.set_colorkey("black")

        pygame.draw.circle(self.image, color, (width // 2, height // 2), width // 2)
        self.rect = self.image.get_rect()
        self.velocity = [randint(3, 8), randint(-15, 15)]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.change_color((0, 255, 0))
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-15, 15)

    def change_color(self, color):
        width = self.image.get_width()
        height = self.image.get_height()
        self.image.fill("black")
        pygame.draw.circle(self.image, color, (width // 2, height // 2), width // 2)
