# 게임 내에서 게임의 규칙을 바꿔 목표를 이루는 게임
# 목표: YOU 속성의 객체가 WIN 속성의 객체와 겹쳐지면 이긴다.
# 예) BABA IS YOU, FLAG IS WIN 일 때 바바가 깃발에 닿으면 이긴다.
# 이 외에도 여러 가지 의 속성이 있다.
#

# player 클래스
# 이동, 공격, 충돌 감지, 렌더링, 상태 추적 등을 포함하여 플레이어와 관련된 거의 모든 것을 담당합니다.

"""
v1-1. 라이브러리 가져오기
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
v1-2. 사용할지 모르겠지만 스프라이트의 x, y좌표
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
# baba_image = p.image.load('./Baba is you Image/Baba_Object.png')
# baba_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(baba_image, text_size)}
# flag_image = p.image.load('./Baba is you Image/Flag_Object.png')
# flag_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(flag_image, text_size)}
# wall_image = p.image.load('./Baba is you Image/Wall_Object.png')
# wall_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(wall_image, text_size)}
# rock_image = p.image.load('./Baba is you Image/Rock_Object.png')
# rock_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(rock_image, text_size)}

# 텍스트
# baba_text_image = p.image.load('./Baba is you Image/Baba_Text.png')
# baba_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(baba_text_image, text_size)}
# flag_text_image = p.image.load('./Baba is you Image/Flag_Text.png')
# flag_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(flag_text_image, text_size)}
# wall_text_image = p.image.load('./Baba is you Image/Wall_Text.png')
# wall_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(wall_text_image, text_size)}
# rock_text_image = p.image.load('./Baba is you Image/Rock_Text.png')
# rock_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(rock_text_image, text_size)}
# you_text_image = p.image.load('./Baba is you Image/You_Text.png')
# you_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#             'image': p.transform.scale(you_text_image, text_size)}
# win_text_image = p.image.load('./Baba is you Image/Win_Text.png')
# win_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#             'image': p.transform.scale(win_text_image, text_size)}
# stop_text_image = p.image.load('./Baba is you Image/Stop_Text.png')
# stop_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(stop_text_image, text_size)}
# push_text_image = p.image.load('./Baba is you Image/Push_Text.png')
# push_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#              'image': p.transform.scale(push_text_image, text_size)}
# is_text_image = p.image.load('./Baba is you Image/Is_Text.png')
# is_text_rect = {'rect': p.Rect(width/2-50, height-90, 24, 24),
#            'image': p.transform.scale(is_text_image, text_size)}


character_x_position = width/2-50
character_y_position = height-90
to_x = 0
to_y = 0
character_speed = 0.1

"""
v1-3. 클래스 초기화
Player 클래스에는 Player Sprite에 대한 코드
Enemy 클래스에는 플레이어가 직면하게 될 적에 대한 코드
Background 및 Ground 클래스는 게임의 시각적 모양과 느낌 제어 코드
"""
class Background(p.sprite.Sprite):
    """
    v2-1 배경 코드 작성
    """
    def __init__(self):
        super().__init__()
        self.bgimage = p.image.load("Baba is you Image/Background.png")
        self.bgY = 0
        self.bgX = 0

    def render(self):
        screen.blit(self.bgimage, (self.bgX, self.bgY))

class Ground(p.sprite.Sprite):
    """
    v2-2 Ground class 코드 작성
    """
    def __init__(self):
        super().__init__()
        self.image = p.image.load("Baba is you Image/Ground.png")
        self.rect = self.image.get_rect(center=(width/2, height))

    def render(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(p.sprite.Sprite):
    """
    v3-1 player class 생성자 작성
    """
    def __init__(self):
        super().__init__()
        self.image = p.image.load("Baba is you Image/stone1.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0, 0) # 플레이어의 속도
        self.acc = vec(0, 0) # 플레이어의 가속도
        self.direction = "RIGHT" # 현재 방향

    """
    v3-2 나머지 기능 만들기
    """
    def move(self):
        pass

    def update(self):
        pass

    def attack(self):
        pass

    def jump(self):
        pass

class Enemy(p.sprite.Sprite):
    def __init__(self):
        super().__init__()

"""
v2-3 객체 생성
"""
background = Background()
ground = Ground()
"""
v3-3 player 객체 생성
"""
player = Player()

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

    """
    v2-4 background, ground 객체의 render 함수 호출
    """
    background.render()
    ground.render()
    """
    v3-4 player 렌더링
    """
    screen.blit(player.image, player.rect)

    screen.blit(baba_rect['image'], baba_rect['rect']) # baba_rect['rect']
    # screen.blit(baba_rect['image'], (character_x_position, character_y_position))  # baba_rect['rect']
    character_x_position += to_x * df
    character_y_position += to_y * df
    # screen.blit(flag_rect['image'], flag_rect['rect'])
    # screen.blit(wall_rect['image'], wall_rect['rect'])
    # screen.blit(rock_rect['image'], rock_rect['rect'])
    # screen.blit(baba_text_rect['image'], baba_text_rect['rect'])
    # screen.blit(flag_text_rect['image'], flag_text_rect['rect'])
    # screen.blit(wall_text_rect['image'], wall_text_rect['rect'])
    # screen.blit(rock_text_rect['image'], rock_text_rect['rect'])
    # screen.blit(you_text_rect['image'], you_text_rect['rect'])
    # screen.blit(win_text_rect['image'], win_text_rect['rect'])
    # screen.blit(stop_text_rect['image'], stop_text_rect['rect'])
    # screen.blit(push_text_rect['image'], push_text_rect['rect'])
    # screen.blit(is_text_rect['image'], is_text_rect['rect'])
    p.display.update()
