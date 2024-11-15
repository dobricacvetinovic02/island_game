import requests

from sprites import *

class Game:
    def __init__(self):
        self.board = None
        self.lives = None
        self.state = None
        self.total_guesses = 0
        self.correct_guesses = 0
        self.guess_button = Button(WIDTH // 2 - 50, HEIGHT - 50, 100, 40, "Guess",
                                   (70, 130, 180), (255, 255, 255),(200, 200, 200), self.guess)
        self.restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "Play Again",
                                     (70, 130, 180), (255, 255, 255), (200, 200, 200), self.restart)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self, heights):
        self.board = Board(heights)
        self.lives = 3

    def run(self):
        self.state = States_game.PLAYING
        while self.state == States_game.PLAYING:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # left-click
                if not self.guess_button.check_click(event.pos):
                    # somewhere else on the screen
                    mx, my = pygame.mouse.get_pos()
                    mx //= TILESIZE
                    my //= TILESIZE
                    if my < ROWS:
                        self.board.lclick(mx, my)

    def guess(self):
        self.total_guesses += 1
        guess = self.board.guess()
        if guess is not None:
            print(guess)
            if guess:
                self.correct_guesses += 1
                self.state = States_game.WON
            else:
                self.lives -= 1
                if self.lives == 0:
                    self.state = States_game.LOST

    def restart(self):
        return True

    def draw_lives(self):
        y = HEIGHT - 50
        # Prvo iscrtamo prazna srca
        for i in range(3):  # Ukupno tri srca
            x = 30 + i * 50  # Razmak između srca
            self.screen.blit(life_empty_image, (x, y))

        # Zatim iscrtamo popunjena srca za preostale živote
        for i in range(self.lives):
            x = 30 + i * 50
            self.screen.blit(life_image, (x, y))

    def draw_stats(self):
        y = HEIGHT - 30
        x =  WIDTH - 120
        if self.total_guesses != 0:
            precision = self.correct_guesses * 100 / self.total_guesses
            message = font.render(f"Accuracy:{precision:.2f}" + "%", True, (255, 255, 255))
            message_rect = message.get_rect(center=(x, y))
            self.screen.blit(message, message_rect)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.guess_button.draw(self.screen)
        self.guess_button.check_hover(pygame.mouse.get_pos())
        self.board.draw(self.screen)
        self.draw_lives()
        self.draw_stats()
        pygame.display.flip()

    def end_screen(self):
        self.screen.fill(BGCOLOUR)
        if self.state == States_game.WON:
            message = font.render("You Win!", True, (0, 122, 16))  # Zelena boja za pobedu
            banner_rect = victory_trophy.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            banner = victory_trophy
        elif self.state == States_game.LOST:
            message = font.render("You Lose", True, (255, 0, 0))  # Crvena boja za poraz
            banner_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            banner = game_over
        else:
            return  # no state, should not happen

        self.screen.blit(banner, banner_rect)
        # Pozicioniraj tekst u sredinu ekrana
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message, message_rect)
        self.restart_button.draw(self.screen)
        while True:
            self.restart_button.draw(self.screen)
            self.restart_button.check_hover(pygame.mouse.get_pos())
            pygame.display.flip()
            # Proveri događaje (klik na dugme)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_button.check_click(event.pos):  # Ako je kliknuto na dugme
                        return  # Pozovi metodu za restart igre



game = Game()
while True:
    heights = []
    x = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
    for line in x.iter_lines():
        for val in line.split():
            heights.append(int(val))
    game.new(heights)
    game.run()
