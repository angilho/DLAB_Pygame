# 게임 내에서 게임의 규칙을 바꿔 목표를 이루는 게임
# 목표: YOU 속성의 객체가 WIN 속성의 객체와 겹쳐지면 이긴다.
# 예) BABA IS YOU, FLAG IS WIN 일 때 바바가 깃발에 닿으면 이긴다.
# 이 외에도 여러 가지 의 속성이 있다.
#

# player 클래스
# 이동, 공격, 충돌 감지, 렌더링, 상태 추적 등을 포함하여 플레이어와 관련된 거의 모든 것을 담당합니다.
# 실행했을 때, 왔다갔다거리는 버그가 있음 이후 해결함

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

p.init()

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

p.display.set_caption("RPG")

"""
9-1 캐릭터와 충돌시 한 번만 충돌할 수 있도록 하는 이벤트
FPS가 60일 경우 최대 1초에 60번 충돌을 기록할 수 있음. 
플레이어가 다시 공격을 받기 전에 1초의 무적 기간
"""
hit_cooldown = p.USEREVENT + 1

"""
6-2 캐릭터 움직임 이미지 리스트
"""
# Run animation for the RIGHT
run_ani_R = [p.image.load("Movement_Animations/Player_Sprite_R.png"), p.image.load("Movement_Animations/Player_Sprite2_R.png"),
             p.image.load("Movement_Animations/Player_Sprite3_R.png"), p.image.load("Movement_Animations/Player_Sprite4_R.png"),
             p.image.load("Movement_Animations/Player_Sprite5_R.png"), p.image.load("Movement_Animations/Player_Sprite6_R.png"),
             p.image.load("Movement_Animations/Player_Sprite_R.png")]

# Run animation for the LEFT * flip을 이용해서 변경하는 것도 해보기
run_ani_L = [p.image.load("Movement_Animations/Player_Sprite_L.png"), p.image.load("Movement_Animations/Player_Sprite2_L.png"),
             p.image.load("Movement_Animations/Player_Sprite3_L.png"), p.image.load("Movement_Animations/Player_Sprite4_L.png"),
             p.image.load("Movement_Animations/Player_Sprite5_L.png"), p.image.load("Movement_Animations/Player_Sprite6_L.png"),
             p.image.load("Movement_Animations/Player_Sprite_L.png")]

"""
7-1 캐릭터 공격 이미지 목록
일부 이미지는 복제됨. 공격 프레임이 충분하지 않아 너무 빨리 끝나 제대로 볼 수 없음.
예를 들어 프레임이 10개 이고 초당 60프레임으로 실행되면
1/6초 종료 / 부드럽고 유동적인 공격을 위해 약 15~20프레임이 있어야 함
"""

# Attack animation for the RIGHT
attack_ani_R = [p.image.load("Movement_Animations/Player_Sprite_R.png"), p.image.load("Attack_Animations/Player_Attack_R.png"),
                p.image.load("Attack_Animations/Player_Attack2_R.png"),p.image.load("Attack_Animations/Player_Attack2_R.png"),
                p.image.load("Attack_Animations/Player_Attack3_R.png"),p.image.load("Attack_Animations/Player_Attack3_R.png"),
                p.image.load("Attack_Animations/Player_Attack4_R.png"),p.image.load("Attack_Animations/Player_Attack4_R.png"),
                p.image.load("Attack_Animations/Player_Attack5_R.png"),p.image.load("Attack_Animations/Player_Attack5_R.png"),
                p.image.load("Movement_Animations/Player_Sprite_R.png")]

# Attack animation for the LEFT
attack_ani_L = [p.image.load("Movement_Animations/Player_Sprite_L.png"), p.image.load("Attack_Animations/Player_Attack_L.png"),
                p.image.load("Attack_Animations/Player_Attack2_L.png"),p.image.load("Attack_Animations/Player_Attack2_L.png"),
                p.image.load("Attack_Animations/Player_Attack3_L.png"),p.image.load("Attack_Animations/Player_Attack3_L.png"),
                p.image.load("Attack_Animations/Player_Attack4_L.png"),p.image.load("Attack_Animations/Player_Attack4_L.png"),
                p.image.load("Attack_Animations/Player_Attack5_L.png"),p.image.load("Attack_Animations/Player_Attack5_L.png"),
                p.image.load("Movement_Animations/Player_Sprite_L.png")]


# character_x_position = width/2-50
# character_y_position = height-90
# to_x = 0
# to_y = 0
# character_speed = 0.1

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
        """
        v4-5 player 이미지 바꾸기
        """
        self.image = p.image.load("Movement_Animations/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0, 0) # 플레이어의 속도
        self.acc = vec(0, 0) # 플레이어의 가속도
        self.direction = "RIGHT" # 현재 방향

        # 5-2 점프 상태 확인
        self.jumping = False

        # 6-1 캐릭터 현재 움직임(Movement)프레임 추적 변수
        self.running = False
        self.move_frame = 0

        # 7-2 상태 확인 및 프레임 확인 변수
        self.attacking = False
        self.attack_frame = 0
        # 9-4 쿨다운 추적 변수
        self.cooldown = False

    """
    v3-2 나머지 기능 만들기
    """
    def move(self):
        # 5-1 중력 추가(수직 가속도)
        self.acc = vec(0, 0.5)
        """
        v4-1 자연스러운 움직임(가속도)
        """
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        """
        v4-2 키 눌림
        """
        key_input = p.key.get_pressed()

        # 가속도를 높일지 여부 결정
        if key_input[K_a]:
            self.acc.x = -ACC
        if key_input[K_d]:
            self.acc.x = ACC

        # 가속도와 속도를 기반으로 계산
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # player가 가장자리로 가면 뒤틀기
        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos

    def update(self):
        # 6-3 이미지는 주기당 하나의 프레임만 업데이트
        # pass

        # 6개의 프레임을 넘기면 0으로 재설정
        if self.move_frame > 6:
            self.move_frame = 0
            return

        # 플레이어가 정지해 있을 때 업데이트 되지 않도록 함
        # 점프가 아니거나, 달리는 중에 업데이트 됨
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        # 플레이어가 (거의) 가만히 있지만 잘못된 움직임이 표시되는 경우 원래 서 있는 위치로 되돌림
        # 아래 코드를 제거 했을 때, 정지해 있는 동안 도중에 달리는 자세에서 올바른 멈춤 현상이 발생할 수 있음
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]

    def attack(self):
        # 7-3 공격 기능 구현
        # pass
        # 모든 공격 프레임이 실행되었는지 확인 후 원래 위치로 재설정
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

        # 방향에 따라 이미지 설정
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]

        # 이미지 업데이트
        self.attack_frame += 1

    # 7-4 보정 함수
    def correction(self):
        # (약) 20픽셀 오류를 상쇄하기 위해 왼쪽 공격 시 Player의 위치를 20픽셀 조정
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20

    def jump(self):
        # 5-5 점프메카닉
        # pass
        """
        만약 플레이어가 지면에 닿고 점프하지 않으면 jumping = True / 그렇지 않으면 -12 (설정 가능)
        """
        self.rect.x += 1

        # Check to see if payer is in contact with the ground
        hits = p.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

        # 5-4 중력 체크 함수
    def gravity_check(self):
        # 플레이어와 지면 사이의 충돌 기록
        hits = p.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    #9-5 적군이 player를 적중했을 때.
    def player_hit(self):
        if not self.cooldown:
            self.cooldown = True
            p.time.set_timer(hit_cooldown, 1000)
            print("hit")


class Enemy(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 8-1 적 클래스 초기화
        self.image = p.image.load("Enemy_Image/Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.direction = r.randint(0, 1) # 방향
        self.vel.x = r.randint(1,3) # x 속도 랜덤
        # 방향에 따른 스폰 위치 설정
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = height-85
        if self.direction == 1:
            self.pos.x = width
            self.pos.y = height-85

    # 8-2 움직임
    def move(self):
        # 적이 화면 끝에 도달하면 방향을 바꾸는 역할
        if self.pos.x >= (width - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0

        # 속도를 빼거나 적의 방향에 따라 위치 "x"에 추가
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect

    # 8-3 그리기
    def render(self):
        screen.blit(self.image, (self.pos.x, self.pos.y))

    # 9-2 충돌체크 업데이트 함수
    def update(self):
        # Player랑 충돌 체크
        hits = p.sprite.spritecollide(self, Playergroup, False)

        #충돌 + 공격 중이면?
        if hits and player.attacking:
            #공격!
            self.kill()
            # 11-8
            print("적 제거!!")
        #충돌 + 공격 중이 아니라면
        elif hits and not player.attacking:
            #피해
            player.player_hit()


# 10-4 Castle class 만들기
class Castle(p.sprite.Sprite):
    def __init__(self):
        super(Castle, self).__init__()
        self.hide = False
        self.image = p.image.load("Castle_Image/castle.png")

    def update(self):
        if not self.hide:
            screen.blit(self.image, (350, 145))

# 10-5 이벤트 핸들러 만들기
class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = p.USEREVENT + 1
        # 11-0
        self.stage = 1

        # 11-1 스테이지 단계 만들기
        # 레벨당 생성될 적의 수를 계산
        # [1, 3, 5, 9, 13, 19, 25, 33, 41, 51, 61, 73, 85, 99, 113, 129, 145, 163, 181, 201]
        self.stage_enemies = []
        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 // 2) + 1))

    # 11-2 n 또는 시간이 지났을 때, 다음 스테이지 호출
    def next_stage(self):  # Code for when the next stage is clicked
        self.stage += 1
        self.enemy_count = 0
        print("Stage: " + str(self.stage))
        p.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))

    # window 선택 창 만들기
    def stage_handler(self):
        self.root = Tk()
        self.root.geometry('200x170')

        button1 = Button(self.root, text="Twilight Dungeon", command=self.world1)
        button2 = Button(self.root, text="Skyward Dungeon", command=self.world2)
        button3 = Button(self.root, text="hell Dungeon", command=self.world3)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)

        self.root.mainloop()

    def world1(self):
        self.root.destroy()
        p.time.set_timer(self.enemy_generation, 2000)
        castle.hide = True
        self.battle = True

    def world2(self):
        self.battle = True

    def world3(self):
        self.battle = True
"""
v2-3 객체 생성
"""
background = Background()
ground = Ground()

"""
5-3 스프라이트 그룹 생성
충돌 감지를 위한 Sprite 그룹은 매개변수가 필요(?)
"""
ground_group = p.sprite.Group()
ground_group.add(ground)

"""
v3-3 player 객체 생성
"""
player = Player()

"""
9-3 스프라이트 그룹 만들기
나중에 player가 더 있을 수 있음.
"""
Playergroup = p.sprite.Group()
Playergroup.add(player)

# 8-4 적 객체 생성
enemy = Enemy()

# 10-6 castle, handler 객체 생성
castle = Castle()
handler = EventHandler()

# 11-7 적 그룹 만들기
Enemies = p.sprite.Group()

while True:
    # 5-6 중력 체크 호출
    player.gravity_check()

    df = clock.tick(FPS)
    for event in p.event.get():
        if event.type == QUIT:
            p.quit()
            s.exit()

        # 5-7 점프 버튼
        if event.type == p.KEYDOWN:
            if event.key == p.K_SPACE:
                player.jump()

            # 7-5 공격 여부 확인 / 첫 번째 공격이 끝날 때까지 다른 공격 막기
            if event.key == p.K_RETURN:
                if player.attacking == False:
                    # player.attack()
                    player.attacking = True

            # 10-7 Handler 호출 이벤트 구현
            if event.key == K_e and 380 < player.rect.x < 480:
                handler.stage_handler()

            # 11-4
            # next_stage()기능을 활성화하는 코드
            # 던전에 있고 현재 존재하는 적이 더 이상 없을 때만 활성화되는 키 누르기 "n"을 할당
            if event.key == p.K_n:
                if handler.battle == True and len(Enemies) == 0:
                    handler.next_stage()

        #11-3 적 생성 타이머가 트리거될 때마다(2초마다) 적 생성
        if event.type == handler.enemy_generation:
            # 핸들러의 stage_enemies 변수가 해당 단계의 최대 제한으로 정의한 것보다 더 많은 적을 생성하지 않습니다.
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1

                # 9-6 타이머 비활성화
        if event.type == hit_cooldown:
            player.cooldown = False
            p.time.set_timer(hit_cooldown, 0)

    # 10-1 테스트 코드 주석(이후 삭제)
    # 9-7 update 호출
    # enemy.update()

    # 7-6 공격 적용
    if player.attacking:
        player.attack()

    """
    v4-4 class 이동코드 적용 
    """
    player.move()


    # 10-2 테스트 코드 주석(이후 삭제)
    # 8-5 적 움직임
    # enemy.move()

    """
    v2-4 background, ground 객체의 render 함수 호출
    """
    background.render()
    ground.render()
    # 10-3 테스트 코드 주석(이후 삭제)
    # 8-6 움직임 그리기
    # enemy.render()
    # 10-8 update 호출
    castle.update()
    """
    v3-4 player 렌더링
    """
    screen.blit(player.image, player.rect)

    # 11-5 Enemies 그룹 움직이고 그리기
    for entity in Enemies:
        entity.update()
        entity.move()
        entity.render()

    """
    6-4 캐릭터 업데이트 적용 
    """
    player.update()
    p.display.update()
