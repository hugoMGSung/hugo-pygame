import pygame
import os
import sys
import random

# 게임 스크린 크기
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# 색 정의
WHITE = (255, 255, 255)
SEA = (80, 180, 220)
GROUND = (140, 120, 40)
DARK_GROUND = (70, 60, 20)

FPS = 60

# 물고기 객체
class Fish():
    def __init__(self):
        self.image = pygame.image.load(resource_path('./resource/fish.png'))
        self.sound = pygame.mixer.Sound(resource_path('./resource/swim.wav'))
        self.rect = self.image.get_rect()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.reset()

    # 위치 초기화
    def reset(self):
        self.rect.x = 250
        self.rect.y = 250
        self.dx = 0
        self.dy = 0

    # 헤엄치기
    def swim(self):
        self.dy = -10
        self.sound.play()

    # 물고기 업데이트
    def update(self):
        self.dy += 0.5
        self.rect.y += self.dy
        # 물고기가 게임 화면 위로 넘어갈 때
        if self.rect.y <= 0:
            self.rect.y = 0
        # 물고기가 게임 화면 아래로 넘어갈 때
        if self.rect.y + self.height > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.height
            self.dy = 0
        # 물고기의 y축 방향값이 20을 초과할 때
        if self.dy > 20:
            self.dy = 20

    # 물고기 그리기
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 파이프 객체
class Pipe():
    def __init__(self):
        self.lpipe = pygame.image.load(resource_path('./resource/pipe01.png'))
        self.lpipe_rect = self.lpipe.get_rect()
        self.lpipe_width = self.lpipe.get_rect().width
        self.lpipe_height = self.lpipe.get_rect().height

        pipes = ('./resource/pipe02.png', './resource/pipe03.png', \
                 './resource/pipe04.png', './resource/pipe05.png', './resource/pipe06.png')
        self.spipe = pygame.image.load(resource_path(random.choice(pipes)))
        self.spipe_rect = self.spipe.get_rect()
        self.spipe_width = self.spipe.get_rect().width
        self.spipe_height = self.spipe.get_rect().height

        self.set_pos()

    # 파이프 위치 설정
    def set_pos(self):
        # 1인 경우 긴 파이프를 위에 위치
        if random.randint(0, 1):
            self.lpipe_rect.x = SCREEN_WIDTH
            self.lpipe_rect.y = -2
            self.spipe_rect.x = SCREEN_WIDTH
            self.spipe_rect.y = SCREEN_HEIGHT - self.spipe_height + 2
        # 0인 경우 긴 파이프를 아래에 위치
        else:
            self.spipe_rect.x = SCREEN_WIDTH
            self.spipe_rect.y = -2
            self.lpipe_rect.x = SCREEN_WIDTH
            self.lpipe_rect.y = SCREEN_HEIGHT - self.lpipe_height + 2

    # 파이프 업데이트
    def update(self):
        self.lpipe_rect.x -= 4
        self.spipe_rect.x -= 4

    # 파이프가 게임 화면을 벗어난 유무 체크
    def out_of_screen(self):
        if self.spipe_rect.x + self.spipe_width <= 0:
            return True
        return False

    # 물고기가 파이프에 충돌한 여부 체크
    def check_crash(self, fish):
        # 긴 파이프에 충돌한 경우
        if (self.lpipe_rect.x + self.lpipe_width > fish.rect.x) and \
            (self.lpipe_rect.x < fish.rect.x + fish.width) and \
            (self.lpipe_rect.y < fish.rect.y + fish.height) and \
            (self.lpipe_rect.y + self.lpipe_height > fish.rect.y):
            return True
        # 짧은 파이프에 충돌한 경우
        elif (self.spipe_rect.x + self.spipe_width > fish.rect.x) and \
            (self.spipe_rect.x < fish.rect.x + fish.width) and \
            (self.spipe_rect.y < fish.rect.y + fish.height) and \
            (self.spipe_rect.y + self.spipe_height > fish.rect.y):
            return True
        else:
            return False

    # 파이프 그리기
    def draw(self, screen):
        screen.blit(self.lpipe, self.lpipe_rect)
        screen.blit(self.spipe, self.spipe_rect)

# 게임 객체
class Game():
    def __init__(self):
        # 게임 리소스 로드
        font_path = resource_path('./resource/NanumGothic-Regular.ttf')
        self.font = pygame.font.Font(font_path, 34)
        pygame.mixer.music.load(resource_path('./resource/bgm.mp3'))

        self.fish = Fish()
        self.pipes = []
        self.pipes.append(Pipe())
        self.pipe_pos = 100
        # 게임 점수
        self.score = 0
        # 게임 메뉴 On/Off
        self.menu_on = True

    # 게임 이벤트 처리 및 조작
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # 메뉴 화면 이벤트 처리
            if self.menu_on:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.play(-1)
                        self.score = 0
                        self.menu_on = False
                        self.fish.reset()
                        self.pipes = []
                        self.pipes.append(Pipe())
            # 게임 화면 이벤트 처리
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.fish.swim()
        return False

    # 게임 로직 수행
    def run_logic(self, screen):
        for pipe in self.pipes:
            # 파이프의 위치가 지정된 위치가 되면 새로운 파이프 추가
            if pipe.spipe_rect.x == self.pipe_pos:
                self.pipes.append(Pipe())
                self.score += 1
            # 파이프가 게임 화면에서 벗어나면 벗어난 파이프 제거
            if pipe.out_of_screen():
                del self.pipes[0]
                self.pipe_pos = random.randrange(200, 300, 4)
            # 파이프에 물고기가 충돌한 경우
            if pipe.check_crash(self.fish):
                pygame.mixer_music.stop()
                self.menu_on = True

    # 텍스트 그리기
    def draw_text(self, screen, text, font, x, y, main_color):
        text_obj = font.render(text, True, main_color)
        text_rect = text_obj.get_rect()
        text_rect.center = x, y
        screen.blit(text_obj, text_rect)

    # 메뉴 출력
    def display_menu(self, screen):
        center_x = (SCREEN_WIDTH / 2)
        center_y = (SCREEN_HEIGHT / 2)
        rect = (center_x - 220, center_y - 50, 440, 100)
        pygame.draw.rect(screen, GROUND, rect)
        pygame.draw.rect(screen, DARK_GROUND, rect, 4)
        self.draw_text(screen, "Press Space Key to Play",
                       self.font, center_x, center_y, DARK_GROUND)

    # 게임 프레임 출력
    def display_frame(self, screen):
        screen.fill(SEA)
        pygame.draw.rect(screen, GROUND,
                         (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.line(screen, DARK_GROUND,
                         (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 4)
        self.fish.update()
        self.fish.draw(screen)
        for pipe in self.pipes:
            pipe.update()
            pipe.draw(screen)
        self.draw_text(screen, "Score: " + str(self.score), self.font, 100, 50, WHITE)


# 게임 리소스 경로
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    # 게임 설정
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fish Game")
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        if game.menu_on:    # 게임 메뉴 처리
            game.display_menu(screen)
        else:       # 게임 화면 처리
            game.run_logic(screen)
            game.display_frame(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()