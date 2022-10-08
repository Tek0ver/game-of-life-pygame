from time import clock_getres
import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()
            exit()

    screen.fill('grey')

    pygame.display.update()

    clock.tick(30)
    