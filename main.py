import requests

from sprites import *

class Game:
    def __init__(self):
        self.playing = None
        self.board = None
        self.lives = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self, heights):
        self.board = Board(heights)
        self.lives = 3

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()  # this still never happens because game mechanics is not implemented

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE
                if event.button == 1:
                #     left-click on the tile
                    self.board.lclick(mx, my)


    def draw(self):
        self.board.draw(self.screen)
        pygame.display.flip()

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return


heights = []
x = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
for line in x.iter_lines():
    for val in line.split():
        heights.append(int(val))

game = Game()
while True:
    game.new(heights)
    game.run()
