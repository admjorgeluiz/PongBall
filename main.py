import pygame
from ball import Ball
from paddle import Paddle

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, -16, 1, 512)

# Configurações
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Ball")

font_name = 'hooge 05_53'
if font_name.lower() not in pygame.font.get_fonts():
    font_name = pygame.font.get_default_font()

main_font = pygame.font.SysFont(font_name, 65)
small_font = pygame.font.SysFont(font_name, 24)

clock = pygame.time.Clock()


def draw_net(surface, color=(255, 255, 255), width=4, height=15, gap=20):
    x = SCREEN_WIDTH // 2 - width // 2
    for y in range(0, SCREEN_HEIGHT, height + gap):
        pygame.draw.rect(surface, color, (x, y, width, height))


def draw_text_center(text, font, color, surface, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(SCREEN_WIDTH // 2, y))
    surface.blit(text_obj, text_rect)


def show_start_screen():
    screen.fill("black")
    draw_text_center("Pong Ball", main_font, (255, 255, 255), screen, 150)
    draw_text_center("Pressione ESPAÇO para jogar", small_font, (255, 255, 255), screen, 250)
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


def run_game():
    # Sprites
    paddle_a = Paddle("white", 10, 100)
    paddle_a.rect.x = 0
    paddle_a.rect.y = 200

    paddle_b = Paddle("white", 10, 100)
    paddle_b.rect.x = SCREEN_WIDTH - 10
    paddle_b.rect.y = 200

    ball = Ball("red", 20, 20)
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                paddle_a.move_up(5)
            if keys[pygame.K_s]:
                paddle_a.move_down(5, SCREEN_HEIGHT)
            if keys[pygame.K_UP]:
                paddle_b.move_up(5)
            if keys[pygame.K_DOWN]:
                paddle_b.move_down(5, SCREEN_HEIGHT)

            all_sprites.update()

            if ball.rect.y <= 0 or ball.rect.y >= SCREEN_HEIGHT - ball.rect.height:
                ball.velocity[1] = -ball.velocity[1]

            if ball.rect.x <= 0:
                score_b += 1
                ball.rect.x = SCREEN_WIDTH // 2
                ball.rect.y = SCREEN_HEIGHT // 2
                ball.velocity[0] = -ball.velocity[0]

            if ball.rect.x >= SCREEN_WIDTH - ball.rect.width:
                score_a += 1
                ball.rect.x = SCREEN_WIDTH // 2
                ball.rect.y = SCREEN_HEIGHT // 2
                ball.velocity[0] = -ball.velocity[0]

            if pygame.sprite.collide_mask(ball, paddle_a) or pygame.sprite.collide_mask(ball, paddle_b):
                ball.bounce()

            screen.fill("black")
            draw_net(screen)
            all_sprites.draw(screen)

            score_text = main_font.render(f"{score_a}   {score_b}", True, (255, 255, 255))
            screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 20))

        else:
            draw_text_center("PAUSADO", main_font, (255, 255, 0), screen, SCREEN_HEIGHT // 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Execução do jogo
show_start_screen()
run_game()
