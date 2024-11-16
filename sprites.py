import math
from enum import Enum

from settings import *

neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class StatesIsland(Enum):
    UNSELECTED = 0
    SELECTED = 1
    GUESSED = 2


class StatesGame(Enum):
    PLAYING = 0
    WON = 1
    LOST = 2


def interpolate_color(start_color, end_color, factor):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * factor),
        int(start_color[1] + (end_color[1] - start_color[1]) * factor),
        int(start_color[2] + (end_color[2] - start_color[2]) * factor)
    )


def gradient_color(value):
    """
    Generates a gradient of color based on value between 0 and 1.
    :param value: value between 0 and 1
    :return: color in a range from blue(0) to white(1)
    """
    if value <= 0.3:
        # Interpolation between blue and green (0 - 0.2)
        return interpolate_color(SEA_BLUE, GREEN, value / 0.3)
    elif value <= 0.5:
        # Interpolation between green and yellow (0.3 - 0.5)
        return interpolate_color(GREEN, YELLOW, (value - 0.3) / 0.2)
    elif value <= 0.75:
        # Interpolation between yellow and brown (0.5 - 0.75)
        return interpolate_color(YELLOW, BROWN, (value - 0.5) / 0.25)
    else:
        # Interpolation between brown and white (0.75 - 1)
        return interpolate_color(BROWN, WHITE, (value - 0.75) / 0.25)


def get_color(height):
    """
    Returns the color representation of a given height.
    :param height: height to be represented.
    :return: color representation of a given height.
    """
    return gradient_color(height / 1000)


def rgb_to_grayscale(rgb):
    """
    Converts a given RGB color to grayscale.
    :param rgb: RGB color to convert.
    :return: grayscale representation of a given RGB color.
    """
    g = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return g, g, g


class Button:
    """
    Class for drawing a button on the screen.
    """

    def __init__(self, x, y, width, height, text, bg_color, text_color, hover_color=None, action=None):
        """
        :param x: x coordinate on the screen where the button will be drawn.
        :param y: y coordinate on the screen where the button will be drawn.
        :param width: width of the button.
        :param height: height of the button.
        :param text: text to be displayed on the button.
        :param bg_color: color of the button.
        :param text_color: color of the text.
        :param hover_color: color of the button while being hovered.
        :param action: function to be called when the button is pressed.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color if hover_color else bg_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        """
        Draws a button on the screen.
        :param screen: screen to draw button on
        :return: None
        """
        color = self.hover_color if self.is_hovered else self.bg_color  # Change the color of the button if the mouse is hovering it
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Add the edge around the button
        text_surface = font.render(self.text, True, self.text_color)  # Add text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """
        Checks if the button is hovered and returns it.
        :param mouse_pos: position of the mouse.
        :return: True if the button is hovered, False otherwise.
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        """
        Checks if the button is clicked and returns it.
        :param mouse_pos: position of the mouse.
        :return: True if the button is clicked, False otherwise.
        """
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()
            return True
        return False


class Tile:
    """
    Class for representing a tile.
    Tile being one instance of a given cell that has height.
    Attributes:
        island (int): representing the island that the tile belongs to.
        state (StatesIsland): representing the state of the tile.
        surface (pygame.Surface): representing the surface of the tile.
        pulsating_tint (pygame.Surface): representing the pulsating tint of the tile (used while the island is selected).
    """

    def __init__(self, x, y, height):
        """
        :param x: x coordinate of the tile on the screen.
        :param y: y coordinate of the tile on the screen.
        :param height: height of the tile.
        """
        self.x = x
        self.y = y
        self.height = height
        self.island = None
        self.state = StatesIsland.UNSELECTED
        self.surface = pygame.Surface((TILESIZE, TILESIZE))
        self.surface.fill(get_color(self.height))
        self.pulsating_tint = pygame.Surface((TILESIZE, TILESIZE))
        self.pulsating_tint.fill(RED)

    def get_height(self):
        return self.height

    def get_island(self):
        return self.island

    def set_island(self, island):
        self.island = island

    def change_state(self, state):
        """
        Changes the state of the tile.
        Once the state is "StatesIsland.GUESSED" it can not be changed.
        :param state: new state of the tile.
        """
        if self.state != StatesIsland.GUESSED:
            self.state = StatesIsland(state.value)

    def __repr__(self):
        return str(self.height)

    def draw(self, surface):
        """
        Draws the tile on the screen. With regard to the state of the tile (island).
        If the island is selected it will show with pulsating red tint to it, if it was already guessed it will show gray.
        :param surface: surface to draw the tile on.
        """
        time = pygame.time.get_ticks() / 1000  # seconds
        alpha_value = 50 + (255 - 155) * (0.5 + 0.5 * math.sin(time * 2))  # freq 2 HZ
        self.pulsating_tint.set_alpha(int(alpha_value))  # alpha determines the opacity of the surface

        if self.state == StatesIsland.GUESSED:
            self.surface.fill(rgb_to_grayscale(get_color(self.height)))
        else:
            self.surface.fill(get_color(self.height))

        surface.blit(self.surface, (self.x * TILESIZE, self.y * TILESIZE))
        if self.state == StatesIsland.SELECTED:
            surface.blit(self.pulsating_tint, (self.x * TILESIZE, self.y * TILESIZE))


class Island:
    """
    Class for representing an island.
    Island is a set of connected tiles.
    Attributes:
        height (int): height of the island (average height of all tiles).
        state (StatesIsland): representing the state of the island.
    """

    def __init__(self, tiles):
        """
        :param tiles: list of tiles that represent the island.
        """
        self.tiles = tiles
        self.height = self.calc_avg_height()
        self.state = StatesIsland.UNSELECTED

    def get_tiles(self):
        return self.tiles

    def calc_avg_height(self):
        sum_height = 0
        cnt = len(self.tiles)
        for tile in self.tiles:
            sum_height += tile.height
        return sum_height / cnt

    def change_state(self, state):
        """
        Changes the state of the island and all its tiles.
        Once the state is "StatesIsland.GUESSED" it can not be changed.
        :param state: new state of the island.
        """
        if self.state != StatesIsland.GUESSED:
            self.state = StatesIsland(state.value)
            for tile in self.tiles:
                tile.change_state(state)

    def get_state(self):
        return self.state

    def __repr__(self):
        return str(self.height)


class Board:
    """
    Class for representing a board that contains ROWS * COLS number of tiles that represent the islands and the water.
    Attributes:
    board_surface (pygame.Surface): representing the board surface.
    tiles (list of Tiles): representing all the tiles.
    islands (list of Islands): representing the islands.
    highest_island (int): representing the index of the highest island.
    selected_island (int): representing the index of the currently selected island.
    """

    def __init__(self, heights):
        """
        :param heights: list of heights of the tiles
        """
        self.board_surface = pygame.Surface((WIDTH, HEIGHT - 60))
        self.tiles = [[Tile(x, y, heights[x * COLS + y]) for y in range(ROWS)] for x in range(COLS)]
        self.islands = self.find_islands(heights)
        self.highest_island = max(self.islands, key=lambda x: x.height)
        self.selected_island = None

    def dfs(self, x, y, heights, number_of_island):
        """
        Depth firs search over the heights list that finds connected tiles with height greater than zero
        beginning with the tile x, y that represent the islands.
        :param x: x coordinate of the first tile.
        :param y: y coordinate of the first tile.
        :param heights: list of heights of the tiles
        :param number_of_island: number of currently found islands.
        :return: list of tiles that represent the found island.
        """
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
        """
        Finds all connected tiles that represent the islands.
        :param heights: heights of the tiles.
        :return: list of islands found.
        """
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
        """
        Left-click on the board.
        Changes the state of the island and all its tiles if clicked appropriately.
        :param x: x coordinate of the click.
        :param y: y coordinate of the click.
        :return: None
        """
        tile = self.tiles[x][y]
        # water
        if tile.get_height() == 0:
            if self.selected_island is not None:
                self.selected_island.change_state(StatesIsland.UNSELECTED)
                self.selected_island = None
            return
        # island
        island = self.islands[tile.get_island()]
        if self.selected_island is not None:
            self.selected_island.change_state(StatesIsland.UNSELECTED)
        self.selected_island = island
        self.selected_island.change_state(StatesIsland.SELECTED)

    def guess(self):
        """
        Determines if the guessed island is the highest.
        :return: None if no island is selected, True/False if selected island is the highest island or not.
        """
        if self.selected_island is None or self.selected_island.get_state() == StatesIsland.GUESSED:
            return None
        elif self.selected_island == self.highest_island:
            return True
        else:
            self.selected_island.change_state(StatesIsland.GUESSED)
            return False

    def draw(self, screen):
        """
        Draws all the tiles on the screen.
        :param screen: screen to draw on.
        """
        for row in self.tiles:
            for tile in row:
                tile.draw(self.board_surface)
        screen.blit(self.board_surface, (0, 0))
