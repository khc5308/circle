import pygame
import sys
import main as result
import os
import random
import math
import time
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Pygame 그림판")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
font = pygame.font.Font("Pretendard-Black.otf", 72)


def visual(text: str, time_duration):
    start_time = time.time()
    font = pygame.font.Font("Pretendard-Black.otf", 56)  # 기존 코드에서 정의된 폰트 사용

    while time.time() - start_time < time_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)  # 화면을 검은색으로 채움 (기존 코드와 일관성 유지)

        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    # 함수 종료 후 화면을 다시 흰색으로 채움 (그리기 모드로 돌아가기 위해)
    screen.fill(WHITE)
    pygame.display.flip()


def init_drawing():
    global drawing, erasing, last_pos, color, thickness
    drawing = False
    erasing = False
    last_pos = None
    color = BLACK
    thickness = 2
    screen.fill(WHITE)

def save_screenshot():
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    filename = f"screenshots/drawing.png"
    pygame.image.save(screen, filename)
    print(f"스크린샷이 저장되었습니다: {filename}")
init_drawing()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                erasing = False
                last_pos = event.pos
            elif event.button == 3:
                erasing = True
                drawing = False
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            erasing = False
            save_screenshot()
            screen.fill(BLACK)
            answer = result.process_image("screenshots/drawing.png")
            if answer == -1:
                visual("이건 원이 아닌거 같아요", 3)
            else:
                visual(f"{answer:.2f}%", 3)

        if event.type == pygame.MOUSEMOTION:
            if drawing or erasing:
                current_pos = event.pos
                if last_pos:
                    # if erasing:
                    #     pygame.draw.line(screen, WHITE, last_pos, current_pos, thickness + 2)
                    # else:
                    pygame.draw.line(screen, color, last_pos, current_pos, thickness)
                last_pos = current_pos


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                color = WHITE
            elif event.key == pygame.K_c:
                screen.fill(WHITE)
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                thickness = min(thickness + 1, 10)
            elif event.key == pygame.K_MINUS:
                thickness = max(thickness - 1, 1)
            elif event.key == pygame.K_n:
                init_drawing()



    pygame.display.flip()

pygame.quit()