import requests

from sprites import *


class Game:
    """
    Class representing all the logic behind the game.
    Attributes:
    board (Board): the game board (all the cells/tiles).
    lives (int): the number of lives remaining.
    state (GameState): the game state.
    total_guesses (int): the total number of guesses made.
    correct_guesses (int): the total number of correct guesses made.
    guess_button (Button): the button that lets the user guess.
    restart_button (Button): the button that lets the user restart the game once it is over.
    screen (pygame.display): the game screen.
    clock (pygame.time.Clock): the game clock (for FPS).
    """

    def __init__(self):
        self.board = None
        self.lives = None
        self.state = None
        self.total_guesses = 0
        self.correct_guesses = 0
        self.guess_button = Button(WIDTH // 2 - 50, HEIGHT - 50, 100, 40, "Guess",
                                   BUTTON_BG, WHITE, BUTTON_HOVER_GRAY, self.guess)
        self.restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Play Again",
                                     BUTTON_BG, WHITE, BUTTON_HOVER_GRAY, self.restart)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self, heights):
        self.board = Board(heights)
        self.lives = 3

    def run(self):
        self.state = StatesGame.PLAYING
        while self.state == StatesGame.PLAYING:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def events(self):
        """
        Handles every interaction with the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # left-click
                if not self.guess_button.check_click(event.pos):
                    # somewhere else on the screen (other than guess button)
                    mx, my = pygame.mouse.get_pos()
                    mx //= TILESIZE
                    my //= TILESIZE
                    if my < ROWS:
                        # somewhere on the board
                        self.board.lclick(mx, my)

    def guess(self):
        """
        Action to call when the guess button is pressed.
        """
        self.total_guesses += 1
        guess = self.board.guess()
        if guess is not None:
            if guess:
                self.correct_guesses += 1
                self.state = StatesGame.WON
            else:
                self.lives -= 1
                if self.lives == 0:
                    self.state = StatesGame.LOST

    def restart(self):
        return True

    def draw_lives(self):
        """
        Draws the number of lives remaining.
        """
        y = HEIGHT - 50
        # empty hearts first
        for i in range(3):  # three total
            x = 30 + i * 50  # distance between each heart
            self.screen.blit(life_empty_image, (x, y))

        # then full hearts
        for i in range(self.lives):  # number of lives left total
            x = 30 + i * 50  # distance between each heart
            self.screen.blit(life_image, (x, y))

    def draw_stats(self):
        """
        Draws the accuracy of the player for all games played.
        """
        y = HEIGHT - 30
        x = WIDTH - 120
        if self.total_guesses != 0:
            precision = self.correct_guesses * 100 / self.total_guesses
            message = font.render(f"Accuracy:{precision:.2f}" + "%", True, WHITE)
            message_rect = message.get_rect(center=(x, y))
            self.screen.blit(message, message_rect)

    def draw(self):
        """
        Draws the game screen.
        """
        self.screen.fill(BGCOLOUR)
        self.guess_button.draw(self.screen)
        self.guess_button.check_hover(pygame.mouse.get_pos())
        self.board.draw(self.screen)
        self.draw_lives()
        self.draw_stats()
        pygame.display.flip()

    def end_screen(self):
        """
        Once the game ended (win or lose) this function handles the end screen until the game is restarted.
        :return: None, goes back to the main while loop, that creates the new game.
        """
        self.screen.fill(BGCOLOUR)
        if self.state == StatesGame.WON:
            message = font.render("You Win!", True, VICTORY_GREEN)
            banner_rect = victory_trophy.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            banner = victory_trophy
        elif self.state == StatesGame.LOST:
            message = font.render("You Lose", True, RED)
            banner_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            banner = game_over
        else:
            return  # no state, should not happen

        self.screen.blit(banner, banner_rect)
        message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(message, message_rect)
        while True:
            # waits for the game to be closed or restarted
            self.restart_button.draw(self.screen)
            self.restart_button.check_hover(pygame.mouse.get_pos())
            pygame.display.flip()
            # check events (mouse clicks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # closed
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_button.check_click(event.pos):
                        # restarted
                        return


# main loop that initiates the new game from a list of heights gotten from the get request
game = Game()
while True:
    list_of_heights = []
    req = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
    for line in req.iter_lines():
        for val in line.split():
            list_of_heights.append(int(val))
    game.new(list_of_heights)
    game.run()
