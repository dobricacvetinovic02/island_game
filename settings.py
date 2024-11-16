import os.path

import pygame

# params
TILESIZE = 24
ROWS = 30
COLS = 30
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS + 60
FPS = 30
TITLE = "GUESS THE ISLAND"

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (140, 140, 140)
GREEN = (0, 255, 0)
YELLOW = (139, 135, 19)
BROWN = (111, 78, 55)
SEA_BLUE = (39, 39, 184)
BGCOLOUR = GRAY
VICTORY_GREEN = (0, 122, 16)
BUTTON_HOVER_GRAY = (200, 200, 200)
BUTTON_BG = (70, 130, 180)

# assets
pygame.init()
pygame.font.init()
life_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "life.png")), (40, 40))  # full heart
life_empty_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "life-empty.png")),
                                          (40, 40))  # empty heart
victory_trophy = pygame.transform.scale(pygame.image.load(os.path.join("assets", "trophy.png")),
                                        (70, 70))  # win screen trophy
game_over = pygame.transform.scale(pygame.image.load(os.path.join("assets", "game-over.png")),
                                   (70, 70))  # lose screen banner
font = pygame.font.Font(None, 36)
