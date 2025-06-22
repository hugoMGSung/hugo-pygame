import pygame
import random

# 초기화
pygame.init()

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 화면 크기
WIDTH = 800
HEIGHT = 600
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("핑퐁 게임")

# 속도
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
PADDLE_SPEED = 5

# 패들 크기
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# 패들 좌표
paddle_left_rect = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right_rect = pygame.Rect(WIDTH-40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# 공 좌표
ball_rect = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)

# 속도 변수
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

# 시계
clock = pygame.time.Clock()

# 게임 루프
running = True
while running:
    dis.fill(BLACK)

    # 이벤트 체크
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_left_rect.top > 0:
        paddle_left_rect.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle_left_rect.bottom < HEIGHT:
        paddle_left_rect.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle_right_rect.top > 0:
        paddle_right_rect.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_right_rect.bottom < HEIGHT:
        paddle_right_rect.y += PADDLE_SPEED

    # 공 이동
    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    # 위, 아래 벽 충돌
    if ball_rect.top <= 0 or ball_rect.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # 패들 충돌
    if ball_rect.colliderect(paddle_left_rect) or ball_rect.colliderect(paddle_right_rect):
        ball_speed_x = -ball_speed_x

    # 왼쪽, 오른쪽 경계 체크 (득점)
    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        # 중앙으로 공 리셋
        ball_rect.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    # 패들, 공 그리기
    pygame.draw.rect(dis, WHITE, paddle_left_rect)
    pygame.draw.rect(dis, WHITE, paddle_right_rect)
    pygame.draw.ellipse(dis, WHITE, ball_rect)

    # 디스플레이 갱신
    pygame.display.flip()
    clock.tick(60)

# 종료
pygame.quit()
