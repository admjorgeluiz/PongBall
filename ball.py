import pygame
from random import randint
import numpy as np
import cv2


class Ball(pygame.sprite.Sprite):
    # Inicializa a bola, definindo sua cor, dimensões, imagem e velocidade inicial.
    def __init__(self, color, width, height):
        super().__init__()
        self.normal_color = pygame.Color(color)
        self.glow_color = pygame.Color(255, 0, 0) # Cor para o efeito de brilho
        self.width = width
        self.height = height

        # Cria uma superfície transparente para a imagem da bola
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)

        self.glow_timer = 0  # Temporizador para o efeito de brilho
        self.draw_ball(self.normal_color) # Desenha a bola com a cor normal inicialmente

        self.rect = self.image.get_rect() # Obtém o retângulo da imagem para posicionamento
        # Define uma velocidade aleatória inicial para a bola nos eixos x e y
        self.velocity = [randint(4, 8), randint(-8, 18)] # [velocidade_x, velocidade_y]

    # Desenha a forma circular da bola na sua superfície ('self.image') com a cor especificada.
    def draw_ball(self, color):
        # Limpa a superfície (torna transparente) antes de desenhar para evitar sobreposição de cores
        self.image.fill((0, 0, 0, 0))
        # Desenha um círculo preenchendo a superfície da bola
        pygame.draw.circle(self.image, color, (self.width // 2, self.height // 2), self.width // 2)

    # Aplica um efeito de contorno vermelho à imagem da bola usando OpenCV para detecção de bordas.
    def apply_contour(self):
        # Converte a superfície Pygame da bola para um array NumPy para processamento com OpenCV
        raw_str = pygame.image.tostring(self.image, "RGB", False)
        img_array = np.frombuffer(raw_str, dtype=np.uint8).reshape((self.height, self.width, 3))
        
        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Aplica o algoritmo Canny para detectar bordas
        edges = cv2.Canny(gray, 50, 150)

        # Converte as bordas de volta para o formato BGR e colore as bordas detectadas de vermelho
        contour_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        contour_bgr[np.where((contour_bgr != [0, 0, 0]).all(axis=2))] = [255, 0, 0]  # Vermelho

        # Converte o array NumPy com o contorno de volta para uma superfície Pygame
        contour_surface = pygame.image.frombuffer(contour_bgr.tobytes(), (self.width, self.height), "RGB")
        contour_surface.set_colorkey((0, 0, 0))  # Define o preto como cor transparente, deixando apenas o contorno vermelho
        # Desenha o contorno sobre a imagem original da bola
        self.image.blit(contour_surface, (0, 0))

    # Atualiza a posição da bola e seu estado visual (cor/brilho e contorno) a cada frame.
    def update(self):
        # Move a bola de acordo com sua velocidade
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Gerencia o efeito de brilho
        if self.glow_timer > 0:
            self.glow_timer -= 1
            self.draw_ball(self.glow_color) # Desenha a bola com a cor de brilho
        else:
            self.draw_ball(self.normal_color) # Desenha a bola com a cor normal

        # Adiciona o contorno sobre a bola (após definir a cor base)
        self.apply_contour()

    # Inverte a direção horizontal da bola, ajusta sua direção vertical aleatoriamente e ativa o efeito de brilho.
    def bounce(self):
        self.velocity[0] = -self.velocity[0] # Inverte a direção no eixo x
        self.velocity[1] = randint(-8, 8)   # Define uma nova velocidade aleatória no eixo y
        self.glow_timer = 10                # Ativa o temporizador para o efeito de brilho

    # Altera a cor base (normal) da bola e a redesenha imediatamente com a nova cor.
    def change_color(self, color):
        self.normal_color = pygame.Color(color) # Atualiza a cor normal da bola
        self.draw_ball(self.normal_color)       # Redesenha a bola com a nova cor
        self.apply_contour() # Reaplica contorno desejado imediatamente após mudança de cor