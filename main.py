from tkinter import Y
import pygame
from sys import exit
from copy import deepcopy

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
GRID_SPACE = 25

# adjust screen dimensions to wanted GRID_SPACE
SCREEN_WIDTH = SCREEN_WIDTH // GRID_SPACE * GRID_SPACE
SCREEN_HEIGHT = SCREEN_HEIGHT // GRID_SPACE * GRID_SPACE

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


class Cells:
    def __init__(self):
        self.color = 'red'
        self.max_x = pygame.display.get_surface().get_width()
        self.max_y = pygame.display.get_surface().get_height()
        self.space = GRID_SPACE
        self.cells = []
        self.neighbour_to_born = [3]
        self.neighbour_to_live = [2, 3]

        self.build_grid()

    def build_grid(self):
        for row in range(self.max_y // self.space):
            self.cells.append([0] * (self.max_x // self.space))

    def convert_clic_to_pos(self, pos):
        col = pos[0] // self.space
        row = pos[1] // self.space
        return col, row

    def add(self, col, row):
        self.cells[row][col] = 1

    def kill_cell(self, col, row):
        self.cells[row][col] = 0

    def count_neighbours(self, cell_grid, col, row):
        count = 0

        check = [
            ( -1,-1), (0,-1), ( 1,-1),
            ( -1, 0),         ( 1, 0),
            ( -1, 1), (0, 1), ( 1, 1)
        ]

        max_x = self.max_x // self.space - 1
        max_y = self.max_y // self.space - 1

        for coord in check:
            x_coord = col + coord[0]
            y_coord = row + coord[1]
            if x_coord > max_x or x_coord < 0 or y_coord > max_y or y_coord < 0:
                continue
            if cell_grid[y_coord][x_coord] == 1:
                count += 1
        return count
        
    def update(self):
        cells_before = deepcopy(self.cells)
        for row_index, row in enumerate(cells_before):
            for col_index, cell in enumerate(row):
                neighbours = self.count_neighbours(cells_before, col_index, row_index)
                # empty cell
                if cells_before[row_index][col_index] == 0:
                    if neighbours in self.neighbour_to_born:
                        self.add(col_index, row_index)
                # already living cell
                if cells_before[row_index][col_index] == 1:
                    if neighbours not in self.neighbour_to_live:
                        self.kill_cell(col_index, row_index)

    def display(self, display_surface):
        for row_index, row in enumerate(self.cells):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(
                        display_surface,
                        self.color,
                        pygame.Rect(
                            col_index * self.space,
                            row_index * self.space,
                            self.space,
                            self.space
                        ))


grid = Grid()
display_grid = True

cells = Cells()

pause = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # toggle grid display
            if event.key == pygame.K_g:
                display_grid = not display_grid
            # pause
            if event.key == pygame.K_p:
                pause = not pause
            # reset
            if event.key == pygame.K_r:
                pause = True
                cells = Cells()
        if event.type == pygame.MOUSEBUTTONDOWN:
        # add cell with clic
            if event.button == 1:
                cells.add(*cells.convert_clic_to_pos(event.pos))
        if event.type == pygame.MOUSEBUTTONDOWN:
        # kill cell with clic
            if event.button == 3:
                cells.kill_cell(*cells.convert_clic_to_pos(event.pos))

    screen.fill('grey')

    if not pause:
        cells.update()
    cells.display(screen)

    if display_grid is True:
        grid.display(screen)

    pygame.display.update()

    clock.tick(5)
