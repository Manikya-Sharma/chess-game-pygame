import pygame
from board import Board
from _timer import Timer
from images import Images


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        # size of squares:-
        self.margin = 10
        self.size = (
            self.screen.get_width() - 2 * self.margin
        ) / 8  # Assuming square screen

        self.img = Images(self.size).get_images()
        self.board = Board(self.img)  # TODO add which color player

        # misc
        self.timer = Timer()  # To add small delay

    def update(self):
        # Hover
        pos = pygame.mouse.get_pos()
        self.board.update(pos[0], pos[1], self.size, 0, self.margin)
        # Selection
        if pygame.mouse.get_pressed()[2]:
            if (
                self.timer.get_time() >= 200
            ):  # prevents unwanted successive select/unselect
                self.timer.reset()
                pos = pygame.mouse.get_pos()
                self.board.detect_click(pos[0], pos[1], self.size, 0, self.margin)
        if pygame.mouse.get_pressed()[0]:
            self.board.remove_all_selected()

    def play(self):
        self.board.draw(self.size, 0, self.margin)
        self.update()
