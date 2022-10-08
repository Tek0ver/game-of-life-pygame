import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
GRID_SPACE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


class Grid:
    def __init__(self, color='black'):
        self.color = color
        self.space = GRID_SPACE

    def display(self, display_surface):
        # draw vertical lines
        x = 0
        y = display_surface.get_height()
        while x < display_surface.get_width():
            x += self.space
            pygame.draw.line(display_surface, self.color, (x,0), (x,y))
        
        # draw horizontal lines
        x = display_surface.get_width()
        y = 0
        while y < display_surface.get_width():
            y += self.space
            pygame.draw.line(display_surface, self.color, (0,y), (x,y))




grid = Grid()
display_grid = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.exit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                # toggle grid display
                display_grid = not display_grid

    screen.fill('grey')

    if display_grid is True:
        grid.display(screen)

    pygame.display.update()

    clock.tick(30)
