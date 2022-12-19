import random as r
import time as t

def road(turn):
    road = r.sample([1, 2, 3, 4], r.randint(2, 3))
    list = ['전투', '강화', '회복', '상점']
    select = []
    if turn % 20 == 0 and turn != 0:
        select.append('보스전')
    else:
        for i in road:
            select.append(str(list[i - 1]))
    return select


def battle(charater):
    text = ''
    text += '--------전투 시작--------\n'
    monster = [r.randrange(10, 20, 5), r.randrange(5, 15, 5)]
    # print()
    text += f'몬스터: 체력: {monster[0]}, 공격력: {monster[1]}\n'
    while True:
        # print(f'플레이어: 체력: {charater[0]}, 공격력: {charater[1]}')
        text += f'플레이어: 체력: {charater[0]}, 공격력: {charater[1]}\n'
        monster[0] -= charater[1]
        if monster[0] <= 0:
            charater[2] += r.randint(3, 7)
            return text, '----------승리----------'
        # print(f'몬스터: 체력: {monster[0]}, 공격력: {monster[1]}')
        text += f'몬스터: 체력: {monster[0]}, 공격력: {monster[1]}\n'
        charater[0] -= monster[1]
        if charater[0] <= 0:
            return text, '----------패배----------'


def upgrade(charater):
    charater[1] += r.randrange(5, 15, 5)
    return charater


def heal(charater):
    charater[0] += r.randrange(20, 40, 10)
    return charater


def boss_battle(charater, a):
    text = ''
    text += '-------보스전 시작-------\n'
    # print('-------보스전 시작-------')
    boss = [r.randrange(75 * a, 100 * a, 5 * a), r.randrange(15 * a, 35 * a, 5 * a)]
    while True:
        boss[0] -= charater[1]
        if boss[0] <= 0:
            charater[2] += r.randint(35 * a, 55 * a)
            return text, '----------승리----------'
        charater[0] -= boss[1]
        if charater[0] <= 0:
            return text, '----------패배----------'


def shop(charater):
    item_list = {'철 검': '5골드', '회복약': '3골드'}
    while charater[2] >= 3:
        market = input(f'선택: {item_list}')
        if market == '철 검':
            charater[1] += 3
            charater[2] -= 5
        elif market == '회복약':
            charater[0] += 5
            charater[2] -= 3
        else:
            return charater
    return charater