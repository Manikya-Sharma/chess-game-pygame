import pygame
from board import Board
from _timer import Timer
from images import Images

class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.board = Board()
        # misc
        self.timer = Timer()  # To add small delay
        self.img = Images().get_images()

    def update(self):
        # Hover
        pos = pygame.mouse.get_pos()
        self.board.update(pos[0], pos[1], 70, 5, 5)
        # Selection
        if pygame.mouse.get_pressed()[2]:
            if (
                self.timer.get_time() >= 200
            ):  # prevents unwanted successive select/unselect
                self.timer.reset()
                pos = pygame.mouse.get_pos()
                self.board.detect_click(pos[0], pos[1], 70, 5, 5)

    def play(self):
        # TESTS
        self.board.draw(70, 5, 5)
        self.screen.blit(self.img["black"]["king"], (20,20))
        for sq in self.board.get_all_squares_in_diagonal(4, 7):
            sq.highlighted = True
        self.update()
