import pygame
from level import Level


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
        self.level = Level()

    def initialize_screen(self):
        print("Initializing the screen")  #!

    def end_game(self):
        print("The game was ended")  #!
        self.running = False

    def play(self):
        while self.running:
            self.screen.fill(self.bg_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_game()
            self.level.play()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.play()
