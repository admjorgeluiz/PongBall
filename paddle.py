import pygame


class Paddle(pygame.sprite.Sprite):
    # Inicializa a raquete, definindo sua cor, dimensões e imagem.
    def __init__(self, color, width, height):
        super().__init__() # Chama o construtor da classe pai (Sprite)

        # Cria a superfície da imagem da raquete
        self.image = pygame.Surface([width, height])
        self.image.fill("black") # Preenche o fundo com preto (para ser usado como colorkey)
        self.image.set_colorkey("black") # Define o preto como cor transparente

        # Desenha o retângulo da raquete na cor especificada
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        # Obtém o objeto rect da imagem, usado para posicionamento e detecção de colisão
        self.rect = self.image.get_rect()

    # Move a raquete para cima, um número específico de pixels, com limite na borda superior da tela.
    def move_up(self, pixels):
        self.rect.y -= pixels # Decrementa a coordenada Y para mover para cima
        # Impede que a raquete saia da tela por cima
        if self.rect.y < 0:
            self.rect.y = 0

    # Move a raquete para baixo, um número específico de pixels, com limite na borda inferior da tela.
    def move_down(self, pixels, screen_height):
        self.rect.y += pixels # Incrementa a coordenada Y para mover para baixo
        # Impede que a raquete saia da tela por baixo
        if self.rect.y > screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height