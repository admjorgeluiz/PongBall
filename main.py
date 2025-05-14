import pygame
import math

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((360, 720))
clock = pygame.time.Clock()
running = True
pygame.mouse.set_visible(False)
dt = 0

circle_pos = pygame.Vector2(180, 100)  # Posição inicial do círculo
circle_vel = pygame.Vector2(0, 0)  # Agora é um vetor
circle_rad = 10
gravity = pygame.Vector2(2, 7 * 100)  # Gravidade como vetor (só no eixo Y)

rect_pos = pygame.Vector2(180, 700)  # Posição ajustada para ficar visível
rect_size = pygame.Vector2(50, 25)  # Largura e altura do retângulo

# Física
elasticity = 1.0  # Coeficiente de restituição

# Loop principal
rodando = True
while rodando:
    dt = clock.tick(60) / 1000  # DeltaTime mais consistente em 60 FPS

    # Processa eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Controla o retângulo com o mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rect_pos.x = mouse_x - rect_size.x / 2  # Centraliza no mouse

    # Limita o retângulo na tela
    rect_pos.x = max(0, min(rect_pos.x, screen.get_width() - rect_size.x))

    # Aplica gravidade
    circle_vel += gravity * dt
    circle_pos += circle_vel * dt

    # Detecção de colisão
    rect_rect = pygame.Rect(rect_pos.x, rect_pos.y, rect_size.x, rect_size.y)
    circle_rect = pygame.Rect(circle_pos.x - circle_rad, circle_pos.y - circle_rad,
                              circle_rad * 2, circle_rad * 2)

    if circle_rect.colliderect(rect_rect):
        # Verifica colisão no topo do retângulo
        if circle_pos.y + circle_rad <= rect_pos.y + 10:
            # Quique vertical
            circle_vel.y = -circle_vel.y * elasticity
            circle_pos.y = rect_pos.y - circle_rad
        else:
            # Colisão lateral
            relative_intersect_x = (circle_pos.x - (rect_pos.x + rect_size.x / 2))
            normalized_relative_intersect_x = relative_intersect_x / (rect_size.x / 2)
            bounce_angle = normalized_relative_intersect_x * (math.pi / 3)  # Limita a 60 graus

            speed = math.sqrt(circle_vel.x ** 2 + circle_vel.y ** 2) * elasticity
            circle_vel.x = speed * math.sin(bounce_angle)
            circle_vel.y = -speed * math.cos(bounce_angle)

    # Colisão com paredes
    if circle_pos.x - circle_rad <= 0:
        circle_pos.x = circle_rad
        circle_vel.x = -circle_vel.x * elasticity
    elif circle_pos.x + circle_rad >= screen.get_width():
        circle_pos.x = screen.get_width() - circle_rad
        circle_vel.x = -circle_vel.x * elasticity

    # Colisão com o chão
    if circle_pos.y + circle_rad >= screen.get_height():
        circle_pos.y = screen.get_height() - circle_rad
        circle_vel.y = -circle_vel.y * elasticity

    # Desenho
    screen.fill("white")
    pygame.draw.rect(screen, "blue", rect_rect)
    pygame.draw.circle(screen, "black", (int(circle_pos.x), int(circle_pos.y)), circle_rad)

    pygame.display.flip()

pygame.quit()