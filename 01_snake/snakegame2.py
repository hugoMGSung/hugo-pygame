import pygame
import time
import random

# 초기화
pygame.init()

# 색 정의
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# 화면 크기
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 10
SPEED = 15

# 디스플레이 설정
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('스네이크 게임')
clock = pygame.time.Clock()

# 한글 폰트 로드
font_style = pygame.font.Font("NanumGothic-Regular.ttf", 25)

# 소리 파일 로드
eat_sound = pygame.mixer.Sound("./resource/eat.wav")           # 과일 먹었을 때
gameover_sound = pygame.mixer.Sound("./resource/bomb.wav") # 벽 충돌 시

def message(msg, color):
    """화면에 메시지를 표시하는 함수"""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def gameLoop():
    """게임 메인 루프"""
    game_over = False
    game_close = False

    # 스네이크 최초 좌표
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    # 스네이크 몸과 크기
    snake_List = []
    Length_of_snake = 1

    # 음식 최초 좌표
    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(BLUE)
            message("게임 종료! C-다시하기 / Q-종료", RED)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # 경계 체크
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            gameover_sound.play()  # 벽 충돌 소리
            game_close = True

        # 좌표 변경
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        # 음식 그리기
        pygame.draw.rect(dis, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        # 스네이크 증가
        snake_head = [x1, y1]
        snake_List.append(snake_head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 스네이크 몸통과 충돌 체크
        for x in snake_List[:-1]:
            if x == snake_head:
                gameover_sound.play()
                game_close = True

        # 스네이크 그리기
        for x in snake_List:
            pygame.draw.rect(dis, WHITE, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

        pygame.display.update()

        # 음식 먹었을 때
        if x1 == foodx and y1 == foody:
            eat_sound.play()  # 과일 먹었을 때 소리
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(SPEED)

    pygame.quit()
    quit()


# 게임 실행
gameLoop()
