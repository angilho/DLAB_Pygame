import time as t
# 티킨터 임폴트
from tkinter import *
# 티킨터 임폴트
import tkinter.ttk as ttk
import SURVIVE_GAME as sg

charater = [30, 5, 0]
fight = ''
boss_fight = ''
turn = 0
loading_bar = [i / 10 for i in range(1000)]

# 티킨터 객체 root 만들기
root = Tk()
# 제목, 사이즈 설정
root.title("SURVIVE_GAME")
root.geometry("640x480")

# # Progressbar 함수 호출(mode option = determinate/indeterminate)
# progress_bar = ttk.Progressbar(root, maximum=150, length=200)
# #프로그레스바 자동 실행 / 숫자가 0에 가까울수록 빠르게 참
# progress_bar.start(5)
# progress_bar.pack()

# #중지버튼 실행 함수 만들기
# def btncmd():
#     progress_bar.stop()
#
# #중지 버튼 만들기
# btn = Button(root, text="중지", command=btncmd)
# btn.pack()

# DoubleVar() 함수는 소수점의 숫자 사용
p_var = DoubleVar()
pro_bar = ttk.Progressbar(root, variable=p_var)
pro_bar.pack()

for i in range(1, 101):
    t.sleep(0.01)

    p_var.set(i)
    # update로 저장된 값 반영
    pro_bar.update()
    # print(p_var.get())

string_Opening = ['전투에서는 몬스터와 싸워 골드를 얻을 수 있습니다.(1/4)',
                  '회복에서는 랜덤한 양의 체력을 회복합니다. (2/4)',
                  '강화에서는 랜덤한 양의 공격력을 올립니다. (3/4)',
                  '상점에서는 골드를 사용하여 일정량의 회복 또는 강화를 할 수 있습니다. (4/4)',
                  '준비되었다면 아무 키나 누르세요.']

for s in string_Opening:
    label = Label(root, text=s)
    label.pack()
    label.update()
    t.sleep(1)

label = Label(root, text=sg.road(turn))
label.pack()

select_label = Label(root)

text = Text(root)
def result(n):
    global turn
    map = input_map.get()
    select = sg.road(turn)
    select_label.config(text="입력한 내용 > "+map)
    if map in select:
        if map == '전투':
            fight = sg.battle(charater)
            text.insert(fight[0])
            # print(fight)
        elif map == '강화':
            sg.upgrade(charater)
        elif map == '회복':
            sg.heal(charater)
        elif map == '보스전':
            boss_fight = sg.boss_battle(turn // 20, charater)
            text.insert(boss_fight[0])
            # print(boss_fight)
        # 나중에 구현 하기
        elif map == '상점':
            sg.shop(charater)
    print(f'플레이어: 체력: {charater[0]}, 공격력: {charater[1]}, 골드: {charater[2]}G')
    turn += 1
    if fight[1] == '----------패배----------' or boss_fight[1] == '----------패배----------':
        print(f'버틴 턴 수: {turn}')
        return

input_map = Entry(root, width=30)
input_map.bind('<Return>', result)
input_map.pack()
select_label.pack()

# while True:
#     select = sg.road(turn)
#     print(*select)
#     # map = input('선택: ')
#
#     map = input_map.get()
#     if map in select:
#         if map == '전투':
#             fight = sg.battle()
#             print(fight)
#         elif map == '강화':
#             sg.upgrade()
#         elif map == '회복':
#             sg.heal()
#         elif map == '보스전':
#             boss_fight = sg.boss_battle(turn // 20)
#             print(boss_fight)
#         elif map == '상점':
#             sg.shop()
#     print(f'플레이어: 체력: {charater[0]}, 공격력: {charater[1]}, 골드: {charater[2]}G')
#     turn += 1
#     if fight == '----------패배----------' or boss_fight == '----------패배----------':
#         print(f'버틴 턴 수: {turn}')
#         break


root.mainloop()