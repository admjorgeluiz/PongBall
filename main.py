import sys

try:
    import pygame
    import random
    from ball import Ball
    from paddle import Paddle
except ModuleNotFoundError as e:
    print(f"Erro: Uma dependência essencial não foi encontrada: {e.name}")
    print("Por favor, instale as dependências executando:\n")
    print("pip install -r requirements.txt")
    sys.exit(1)

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)

# Sons
hit_sound = pygame.mixer.Sound("assets/Pong!.mp3")
hit_sound.set_volume(0.2)
score_sound = pygame.mixer.Sound("assets/game_point.mp3")
score_sound.set_volume(0.2)
victory_sound = pygame.mixer.Sound("assets/winner.mp3")
victory_sound.set_volume(0.2)

# Configurações
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Ball")

font_name = "arial"
if font_name.lower() not in pygame.font.get_fonts():
    font_name = pygame.font.get_default_font()

main_font = pygame.font.SysFont(font_name, 65)
small_font = pygame.font.SysFont(font_name, 24)

clock = pygame.time.Clock()


# Aplica um efeito de fade (transição gradual) na tela, podendo ser fade-in ou fade-out.
def fade(
    screen,
    width,
    height,
    fade_in=True,
    speed=3,
    text=None,
    font=None,
    color=(255, 255, 255),
):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))

    if fade_in:
        alpha_range = range(255, -1, -speed)
    else:
        alpha_range = range(0, 256, speed)

    for alpha in alpha_range:
        screen.fill("black")
        if text and font:
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)

        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)


# Desenha a rede no centro da tela do jogo.
def draw_net(surface, color=(255, 255, 255), width=4, height=15, gap=20):
    x = SCREEN_WIDTH // 2 - width // 2
    for y in range(0, SCREEN_HEIGHT, height + gap):
        pygame.draw.rect(surface, color, (x, y, width, height))


# Desenha um texto centralizado horizontalmente em uma determinada altura (y) na tela.
def draw_text_center(text, font, color, surface, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(SCREEN_WIDTH // 2, y))
    surface.blit(text_obj, text_rect)


# Desenha a raquete (paddle) com efeitos visuais opcionais como halo e tremor.
def draw_paddle_with_effects(
    surface, paddle, base_color, halo_color, halo=True, tremor=False
):
    # Tremor
    tremor_x = random.randint(-3, 3) if tremor else 0
    tremor_y = random.randint(-3, 3) if tremor else 0

    # Halo
    if halo:
        for i in range(12, 0, -3):
            halo_surface = pygame.Surface(
                (paddle.rect.width + i, paddle.rect.height + i), pygame.SRCALPHA
            )
            alpha = max(20, 255 // (i + 1))
            pygame.draw.rect(
                halo_surface,
                (*halo_color, alpha),
                (0, 0, paddle.rect.width + i, paddle.rect.height + i),
            )
            surface.blit(halo_surface, (paddle.rect.x - i // 2, paddle.rect.y - i // 2))

    # Desenha a raquete original por cima
    pygame.draw.rect(
        surface,
        base_color,
        (
            paddle.rect.x + tremor_x,
            paddle.rect.y + tremor_y,
            paddle.rect.width,
            paddle.rect.height,
        ),
    )


# Exibe a tela inicial do jogo com instruções.
def show_start_screen():
    screen.fill("black")
    draw_text_center("Pong Ball", main_font, (255, 255, 255), screen, 150)
    draw_text_center(
        "Pressione ESPAÇO para jogar", small_font, (255, 255, 255), screen, 250
    )
    draw_text_center("P para pausar/resumir", small_font, (180, 180, 180), screen, 300)
    draw_text_center("W/S e ↑/↓ para mover", small_font, (180, 180, 180), screen, 340)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


# Executa o loop principal do jogo Pong.
def run_game():
    # Sprites
    paddle_a = Paddle("white", 10, 100)
    paddle_a.rect.x = 0
    paddle_a.rect.y = 200

    paddle_b = Paddle("white", 10, 100)
    paddle_b.rect.x = SCREEN_WIDTH - 10
    paddle_b.rect.y = 200

    ball = Ball("blue", 20, 20)
    ball.rect.x = SCREEN_WIDTH // 2
    ball.rect.y = SCREEN_HEIGHT // 2

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle_a)
    all_sprites.add(paddle_b)
    all_sprites.add(ball)

    score_a = 0
    score_b = 0
    paused = False
    running = True
    ball.glow_timer = 0

    # Timers para tremor
    tremor_a_timer = 0
    tremor_b_timer = 0

    fade(
        screen,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        fade_in=True,
        text="Vamos lá!",
        font=small_font,
    )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused
                fade(
                    screen,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    fade_in=False,
                    text="Pausado",
                    font=small_font,
                )  # Efeito de fade ao pausar

                if paused:  # Se o jogo está entrando em pausa
                    fade(
                        screen,
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT,
                        fade_in=False,
                        text="Pausado",
                        font=small_font,
                    )

                    # Ajuste a posição dos textos para caberem as novas opções
                    draw_text_center(
                        "PAUSADO",
                        main_font,
                        (255, 255, 0),
                        screen,
                        SCREEN_HEIGHT // 2 - 40,
                    )  # Y um pouco mais para cima
                    draw_text_center(
                        "Pressione R para Reiniciar",
                        small_font,
                        (200, 200, 200),
                        screen,
                        SCREEN_HEIGHT // 2 + 20,
                    )

                    pygame.display.flip()

                    temp_paused = True
                    while temp_paused:
                        for sub_event in pygame.event.get():
                            if sub_event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()  # Use sys.exit() aqui como no seu código original
                            if sub_event.type == pygame.KEYDOWN:
                                if sub_event.key == pygame.K_p:
                                    paused = not paused
                                    temp_paused = False
                                elif (
                                    sub_event.key == pygame.K_r
                                ):  # NOVA OPÇÃO: Reiniciar
                                    fade(
                                        screen,
                                        SCREEN_WIDTH,
                                        SCREEN_HEIGHT,
                                        fade_in=False,
                                        text="Reiniciando...",
                                        font=small_font,
                                    )
                                    run_game()  # Chama run_game() para reiniciar
                                    return  # Sai da instância atual de run_game()
                        clock.tick(30)
                fade(
                    screen,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    fade_in=True,
                    text="Continuando...",
                    font=small_font,
                )  # Efeito de fade ao resumir

        if not paused:
            keys = pygame.key.get_pressed()
            # Movimentação do paddle A (esquerda)
            if keys[pygame.K_w]:
                paddle_a.move_up(5)
            if keys[pygame.K_s]:
                paddle_a.move_down(5, SCREEN_HEIGHT)
            # Movimentação do paddle B (direita)
            if keys[pygame.K_UP]:
                paddle_b.move_up(5)
            if keys[pygame.K_DOWN]:
                paddle_b.move_down(5, SCREEN_HEIGHT)

            all_sprites.update()  # Atualiza todos os sprites do jogo (bola, raquetes)

            # Verifica colisão da bola com as bordas superior e inferior da tela
            if ball.rect.y <= 0 or ball.rect.y >= SCREEN_HEIGHT - ball.rect.height:
                ball.velocity[1] = -ball.velocity[
                    1
                ]  # Inverte a direção vertical da bola

            # Verifica se a bola saiu pela esquerda (ponto para jogador B)
            if ball.rect.x <= 0:
                score_b += 1
                score_sound.play()
                ball.rect.x = SCREEN_WIDTH // 2
                ball.rect.y = SCREEN_HEIGHT // 2
                ball.velocity[0] = -ball.velocity[
                    0
                ]  # Inverte a direção horizontal da bola
                # 'glow_timer' é usado para um efeito visual na bola após o ponto
                if hasattr(
                    ball, "glow_timer"
                ):  # Verifica se ball tem o atributo glow_timer
                    ball.glow_timer = 10

            # Verifica se a bola saiu pela direita (ponto para jogador A)
            if ball.rect.x >= SCREEN_WIDTH - ball.rect.width:
                score_a += 1
                score_sound.play()
                ball.rect.x = SCREEN_WIDTH // 2
                ball.rect.y = SCREEN_HEIGHT // 2
                ball.velocity[0] = -ball.velocity[0]
                if hasattr(ball, "glow_timer"):
                    ball.glow_timer = 10

            # Verifica colisão da bola com a raquete A
            if pygame.sprite.collide_mask(ball, paddle_a):
                ball.bounce()  # Presumo que 'bounce' seja um método da classe Ball para tratar a colisão
                hit_sound.play()
                tremor_a_timer = 10  # Ativa o tremor para a raquete A

            # Verifica colisão da bola com a raquete B
            if pygame.sprite.collide_mask(ball, paddle_b):
                ball.bounce()
                hit_sound.play()
                tremor_b_timer = 10  # Ativa o tremor para a raquete B

            # Verifica condição de vitória
            if score_a >= 10 or score_b >= 10:
                for i in range(3):  # Efeito de piscar a tela
                    color = (0, 255, 0) if i % 2 == 0 else (0, 0, 0)
                    screen.fill(color)
                    pygame.display.flip()
                    victory_sound.play()
                    pygame.time.delay(400)
                winner = "Jogador A" if score_a >= 10 else "Jogador B"
                screen.fill("black")
                draw_text_center(
                    f"{winner} venceu!",
                    main_font,
                    (0, 255, 0),
                    screen,
                    SCREEN_HEIGHT // 2,
                )
                pygame.display.flip()
                pygame.time.delay(4000)  # Tempo para exibir a mensagem de vitória

                fade(
                    screen,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    fade_in=False,
                    text="Fim de jogo, JOVEM",
                    font=small_font,
                )

                show_start_screen()  # Volta para a tela inicial

                fade(
                    screen,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    fade_in=True,
                    text="Novo jogo!",
                    font=small_font,
                )

                # Reinicia o jogo recursivamente.
                run_game()
                return

            screen.fill("gray")  # Limpa a tela com a cor cinza

            draw_net(screen)  # Desenha a rede

            # Desenha raquetes com halo e tremor
            draw_paddle_with_effects(
                screen,
                paddle_a,
                (255, 255, 255),
                (0, 0, 255),
                halo=True,
                tremor=(tremor_a_timer > 0),
            )  # Azul
            draw_paddle_with_effects(
                screen,
                paddle_b,
                (255, 255, 255),
                (255, 0, 0),
                halo=True,
                tremor=(tremor_b_timer > 0),
            )  # Vermelho

            # Desenha a bola
            all_sprites.draw(screen)  # Desenha todos os sprites na tela

            # Exibe o placar
            score_text = main_font.render(
                f"{score_a}   {score_b}", True, (255, 255, 255)
            )
            screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 20))

            # Decrementa timers de tremor
            if tremor_a_timer > 0:
                tremor_a_timer -= 1
            if tremor_b_timer > 0:
                tremor_b_timer -= 1

        pygame.display.flip()  # Atualiza o conteúdo da tela inteira
        clock.tick(60)  # Limita o jogo a 60 frames por segundo

    pygame.quit()  # Desinicializa todos os módulos do Pygame


# Inicia o jogo exibindo a tela inicial.
show_start_screen()
# Após a tela inicial, executa o loop principal do jogo.
run_game()
