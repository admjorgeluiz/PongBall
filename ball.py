import pygame
from random import randint
import numpy as np
import cv2


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

        self.glow_timer = 0 
        self.draw_ball(self.normal_color)

        self.rect = self.image.get_rect()
        self.velocity = [randint(3, 8), randint(-15, 15)]

    def draw_ball(self, color):
        """Desenha a bola base com uma cor sólida."""
        self.image.fill("black")
        pygame.draw.circle(self.image, color, (self.width // 2, self.height // 2), self.width // 2)

    def apply_contour(self):
        """Aplica contorno usando OpenCV (Canny)."""
        raw_str = pygame.image.tostring(self.image, "RGB", False)
        img_array = np.frombuffer(raw_str, dtype=np.uint8).reshape((self.height, self.width, 3))

        
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Aplicar detecção de borda (Canny)
        edges = cv2.Canny(gray, 50, 150)

        # Converter borda para BGR e destacar em vermelho
        contour_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        contour_bgr[np.where((contour_bgr != [0, 0, 0]).all(axis=2))] = [255, 0, 0]  # Vermelho

        
        contour_surface = pygame.image.frombuffer(contour_bgr.tobytes(), (self.width, self.height), "RGB")
        self.image.blit(contour_surface, (0, 0))

    def update(self):
        """Atualiza a posição e o estado visual da bola."""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.glow_timer > 0:
            self.glow_timer -= 1
            self.draw_ball(self.glow_color)
        else:
            self.draw_ball(self.normal_color)

        # Adiciona o contorno sobre a bola
        self.apply_contour()

    def bounce(self):
        """Inverte direção e ativa efeito de brilho."""
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-15, 15)
        self.glow_timer = 10  # Brilho por 10 frames (~0.16s a 60 FPS)

    def change_color(self, color):
        """Muda a cor da bola permanentemente."""
        self.normal_color = pygame.Color(color)
        self.draw_ball(self.normal_color)

