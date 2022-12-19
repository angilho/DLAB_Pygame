# 게임 내에서 게임의 규칙을 바꿔 목표를 이루는 게임
# 목표: YOU 속성의 객체가 WIN 속성의 객체와 겹쳐지면 이긴다.
# 예) BABA IS YOU, FLAG IS WIN 일 때 바바가 깃발에 닿으면 이긴다.
# 이 외에도 여러 가지 의 속성이 있다.
#

# 선언부

"""
1. 라이브러리 가져오기
random, tkinter
"""
import pygame as p, sys as s, random as r
from pygame.locals import *
from tkinter import *
from tkinter import filedialog

width = 600
height = 385
text_size = (24, 24)
j_step = 0

p.init()

move_speed = 24

FPS = 60
clock = p.time.Clock()
"""
2. 사용할지 모르겠지만 스프라이트의 x, y좌표
가속도, 마찰 물리 변수
"""
vec = p.math.Vector2
ACC = 0.3
FRIC = -0.10

screen = p.display.set_mode((width, height))

p.display.set_caption("Baba is you")

# 개체
baba_image = p.image.load('Baba is you Image/stone1.png')
baba_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
             'image': p.transform.scale(baba_image, text_size)}


character_x_position = width/2-50
character_y_position = height-90
to_x = 0
to_y = 0
character_speed = 0.1

"""
3. 클래스 초기화
Player 클래스에는 Player Sprite에 대한 코드
Enemy 클래스에는 플레이어가 직면하게 될 적에 대한 코드
Background 및 Ground 클래스는 게임의 시각적 모양과 느낌 제어 코드
"""
class Background(p.sprite.Sprite):
    def __init__(self):
        super().__init__()

class Ground(p.sprite.Sprite):
    def __init__(self):
        super().__init__()

class Player(p.sprite.Sprite):
    def __init__(self):
        super().__init__()

class Enemy(p.sprite.Sprite):
    def __init__(self):
        super().__init__()



while True:
    df = clock.tick(FPS)
    for event in p.event.get():
        if event.type == QUIT:
            p.quit()
            s.exit()
    # 키 이벤트
    keyInput = p.key.get_pressed()
    # 위치 이동
    # 왼쪽
    if keyInput[K_a] and baba_rect['rect'].left > 0: # baba_rect['rect'].left
        baba_rect['rect'].left -= move_speed
        # to_x -= character_speed

    # 오른쪽
    if keyInput[K_d] and baba_rect['rect'].right < width: # baba_rect['rect'].right
        baba_rect['rect'].right += move_speed
        # to_x += character_speed

    # 위쪽
    if keyInput[K_w] and baba_rect['rect'].top > 0: # baba_rect['rect'].top
        baba_rect['rect'].top -= move_speed
        # to_y -= character_speed

    # 아래쪽
    if keyInput[K_s] and baba_rect['rect'].bottom < height: # baba_rect['rect'].bottom
        baba_rect['rect'].bottom += move_speed
        # to_y += character_speed

    screen.fill((0, 0, 0))
    screen.blit(baba_rect['image'], baba_rect['rect']) # baba_rect['rect']
    # screen.blit(baba_rect['image'], (character_x_position, character_y_position))  # baba_rect['rect']
    character_x_position += to_x * df
    character_y_position += to_y * df
    p.display.update()
