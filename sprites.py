import pygame

from settings import *


def interpolate_color(start_color, end_color, factor):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * factor),
        int(start_color[1] + (end_color[1] - start_color[1]) * factor),
        int(start_color[2] + (end_color[2] - start_color[2]) * factor)
    )


# Generates gradient of color
def gradient_color(value):
    if value <= 0.3:
        # Interpolation between blue and green (0 - 0.2)
        return interpolate_color((0, 0, 255), (0, 255, 0), value / 0.3)
    elif value <= 0.5:
        # Interpolation between green and yellow (0.3 - 0.5)
        return interpolate_color((0, 255, 0), (139, 135, 19), (value - 0.3) / 0.2)
    elif value <= 0.75:
        # Interpolation between yellow and brown (0.5 - 0.75)
        return interpolate_color((139, 135, 19), (111, 78, 55), (value - 0.5) / 0.25)
    else:
        # Interpolation between brown and white (0.75 - 1)
        return interpolate_color((111, 78, 55), (255, 255, 255), (value - 0.75) / 0.25)


def get_color(height):
    return gradient_color(height / 1000)


class Tile:
    def __init__(self, x, y, height):
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.height = height
        self.surface = pygame.Surface((TILESIZE, TILESIZE))
        self.surface.fill(get_color(self.height))

    def __repr__(self):
        return str(self.height)

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))


class Board:
    def __init__(self, heights):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        self.board_list = [[Tile(row, col, heights[col * ROWS + row]) for row in range(ROWS)] for col in range(COLLS)]

    def draw(self, screen):
        for row in self.board_list:
            for tile in row:
                tile.draw(self.board_surface)
        screen.blit(self.board_surface, (0, 0))

    def display_board(self):
        for row in self.board_list:
            print(row)
