import pygame
from board import Board

class Game:
    def __init__(self):
        # Initialize
        pygame.init()
        pygame.display.set_caption("Chess")

        # Game Constants
        self.width = 600
        self.height = 600
        self.bg_color = (150, 150, 150)

        # Game Variables
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.board = Board()

    def initialize_screen(self):
        print("Initializing the screen") #!

    def end_game(self):
        print("The game was ended") #!
        self.running = False

    def play(self):
        while self.running:
            self.screen.fill(self.bg_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()
            #TESTS
            self.board.draw(70, 5, 5)
            for sq in self.board.get_all_squares_in_diagonal(4, 7):
                sq.highlighted = True
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.play()
