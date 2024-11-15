import math
from enum import Enum

from settings import *

islands = []
neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class States_island(Enum):
    UNSELECTED = 0
    SELECTED = 1
    GUESSED = 2

class States_game(Enum):
    PLAYING = 0
    WON = 1
    LOST = 2


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
        return interpolate_color((39, 39, 184), (0, 255, 0), value / 0.3)
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

def rgb_to_grayscale(rgb):
    g = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return g, g, g


class Button:
    def __init__(self, x, y, width, height, text, bg_color, text_color, hover_color=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else bg_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        # Boja dugmeta zavisi od toga da li je miš iznad
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect)

        # Dodaj obod da bi dugme izgledalo kao okvir
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Crni okvir oko dugmeta

        # Iscrtavanje teksta
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        # Proverava da li je miš iznad dugmeta
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        # Proverava klik na dugme i poziva akciju ako postoji
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()
            return True
        return False

class Tile:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.island = None
        self.state = States_island.UNSELECTED
        self.surface = pygame.Surface((TILESIZE, TILESIZE))
        self.surface.fill(get_color(self.height))

    def get_height(self):
        return self.height

    def get_island(self):
        return self.island

    def set_island(self, island):
        self.island = island

    def change_state(self, state):
        if self.state != States_island.GUESSED:
            self.state = States_island(state.value)

    def __repr__(self):
        return str(self.height)

    def draw(self, surface):
        if self.state == States_island.UNSELECTED:
            self.surface.fill(get_color(self.height))
        else:
            self.surface.fill(rgb_to_grayscale(get_color(self.height)))

        surface.blit(self.surface, (self.x * TILESIZE, self.y * TILESIZE))


class Island:
    def __init__(self, tiles):
        self.tiles = tiles
        self.height = self.calc_avg_height()
        self.state = States_island.UNSELECTED

    def get_tiles(self):
        return self.tiles

    def calc_avg_height(self):
        sum_height = 0
        cnt = len(self.tiles)
        for tile in self.tiles:
            sum_height += tile.height
        return sum_height / cnt

    def change_state(self, state):
        if self.state != States_island.GUESSED:
            self.state = States_island(state.value)
            for tile in self.tiles:
                tile.change_state(state)

    def get_state(self):
        return self.state

    def __repr__(self):
        return str(self.height)


class Board:
    def __init__(self, heights):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT - 60))
        self.tiles = [[Tile(x, y, heights[x * COLS + y]) for y in range(ROWS)] for x in range(COLS)]
        self.islands = self.find_islands(heights)
        self.highest_island = max(self.islands, key=lambda x: x.height)
        self.selected_island = None

    def dfs(self, x, y, heights, number_of_island):
        stack = [(x, y)]
        island = []
        while stack:
            x, y = stack.pop()
            if heights[x * COLS + y] == 0:
                continue
            island.append(self.tiles[x][y])
            self.tiles[x][y].set_island(number_of_island)
            heights[x * COLS + y] = 0
            for dx, dy in neighbours:
                nx, ny = x + dx, y + dy
                if 0 <= nx < ROWS and 0 <= ny < COLS and heights[nx * COLS + ny] != 0:
                    stack.append((nx, ny))
        return island

    def find_islands(self, heights):
        number_of_islands = 0
        islands = []
        for x in range(ROWS):
            for y in range(COLS):
                if heights[x * COLS + y] != 0:
                    islands.append(Island(self.dfs(x, y, heights, number_of_islands)))
                    number_of_islands += 1
        return islands

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def lclick(self, x, y):
        tile = self.tiles[x][y]
        # water
        if tile.get_height() == 0:
            if self.selected_island is not None:
                self.selected_island.change_state(States_island.UNSELECTED)
                self.selected_island = None
            return
        # island
        island = self.islands[tile.get_island()]
        if self.selected_island is not None:
            self.selected_island.change_state(States_island.UNSELECTED)
        self.selected_island = island
        self.selected_island.change_state(States_island.SELECTED)

    def guess(self):
        if self.selected_island is None:
            return None
        elif self.selected_island.get_state() == States_island.GUESSED:
            return None
        elif self.selected_island == self.highest_island:
            return True
        else:
            self.selected_island.change_state(States_island.GUESSED)
            return False

    def draw(self, screen):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.board_surface)
        screen.blit(self.board_surface, (0, 0))

    def display_board(self):
        for row in self.tiles:
            print(row)
