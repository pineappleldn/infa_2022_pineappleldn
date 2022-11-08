import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
n = 10
x, y, r, dx, dy = [0]*n, [0]*n, [0]*n, [0]*n, [0]*n
color = [RED]*n
count = 0


def new_ball(i):
    '''рисует новый шарик'''
    global x, y, r, color, dx, dy
    x[i] = randint(100, 1100)
    y[i] = randint(100, 700)
    r[i] = randint(20, 100)
    color[i] = COLORS[randint(0, 5)]
    dx[i] = randint(-10, 10)
    dy[i] = randint(-10, 10)


def goal():
    '''проверяет попадание в шарик
    возвращает номер шарика, в который попали'''
    global x, y, r
    miss = True
    for i in range(n):
        if ((x[i] - event.pos[0]) ** 2 + (y[i] - event.pos[1]) ** 2) <= r[i] ** 2:
            miss = False
            return i
    if miss:
        return -1


def update_position():
    '''обновляет позиции всех шариков'''
    global x, y, r, dx, dy
    for i in range(n):
        if x[i] + r[i] >= 1200 or x[i] - r[i] <= 0:
            dx[i] *= (-1)
        if y[i] + r[i] >= 800 or y[i] - r[i] <= 0:
            dy[i] *= (-1)
        x[i], y[i] = x[i] + dx[i], y[i] + dy[i]


def all_circles():
    '''рисует все шарики'''
    for i in range(n):
        circle(screen, color[i], (x[i], y[i]), r[i])


def text():
    global count, s
    s = 'Scores: ' + str(count)
    f1 = pygame.font.Font(None, 30)
    text1 = f1.render(s, True, (255, 255, 255))
    screen.blit(text1, (15, 50))


for i in range(n):
    new_ball(i)
all_circles()

text()
pygame.display.update()
screen.fill(BLACK)
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if goal() >= 0:
                count += 1
                new_ball(goal())

    screen.fill(BLACK)
    all_circles()
    text()
    update_position()
    pygame.display.update()

pygame.quit()
