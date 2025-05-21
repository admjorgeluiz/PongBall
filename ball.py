import pygame
from random import randint

# Classe representando a bola
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.normal_color = pygame.Color(color)
        self.glow_color = pygame.Color(255, 255, 0)  # Cor de brilho (amarelo)
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill("black")
        self.image.set_colorkey("black")

        self.glow_timer = 0  # Duração do brilho (em frames)
        self.draw_ball(self.normal_color)

        self.rect = self.image.get_rect()
        self.velocity = [randint(3, 8), randint(-15, 15)]

    def draw_ball(self, color):
        self.image.fill("black")
        pygame.draw.circle(self.image, color, (self.width // 2, self.height // 2), self.width // 2)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.glow_timer > 0:
            self.glow_timer -= 1
            self.draw_ball(self.glow_color)
        else:
            self.draw_ball(self.normal_color)

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-15, 15)
        self.glow_timer = 10  # Brilho por 10 frames (~0.16s a 60 FPS)

    def change_color(self, color):
        self.normal_color = pygame.Color(color)
        self.draw_ball(self.normal_color)
