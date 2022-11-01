import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((230, 230, 230))
circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 1)

circle(screen, (255, 0, 0), (150, 180), 23)
circle(screen, (0, 0, 0), (150, 180), 23, 1)
circle(screen, (0, 0, 0), (150, 180), 10)

circle(screen, (255, 0, 0), (250, 180), 17)
circle(screen, (0, 0, 0), (250, 180), 17, 1)
circle(screen, (0, 0, 0), (250, 180), 9)

line(screen, (0, 0, 0), [250, 260], [150, 260], 20)

line(screen, (0, 0, 0), [100, 117], [180, 165], 13)
line(screen, (0, 0, 0), [300, 135], [225, 167], 12)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()