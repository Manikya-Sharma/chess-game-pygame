import pygame
from board import Board
from _timer import Timer
from images import Images


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        # size of squares:-
        self.margin = 8  # margin divisible by 8 will ensure continuous board
        self.size = (
            self.screen.get_width() - 2 * self.margin
        ) / 8  # Assuming square screen

        self.img = Images(self.size).get_images()
        self.board = Board(self.img)  # TODO add which color player

        # misc
        self.timer1 = Timer()  # To add small delay
        self.timer2 = Timer()

    def update(self):
        # Hover
        pos = pygame.mouse.get_pos()
        self.board.update(pos[0], pos[1], self.size, 0, self.margin)
        # Selection
        if pygame.mouse.get_pressed()[2]:
            if (
                self.timer1.get_time() >= 200
            ):  # prevents unwanted successive select/unselect
                self.timer1.reset()
                pos = pygame.mouse.get_pos()
                self.board.detect_right_click(pos[0], pos[1], self.size, 0, self.margin)
        if pygame.mouse.get_pressed()[0]:
            if self.timer2.get_time() >= 200:
                self.board.remove_all_selected()
                if not self.board.is_click_on_highlighted(
                    pos[0], pos[1], self.size, 0, self.margin
                ):
                    self.board.remove_all_highlighted()
                    # because if player wants to make a move, highlight must not be removed
                self.timer2.reset()
                pos = pygame.mouse.get_pos()
                self.board.detect_left_click(pos[0], pos[1], self.size, 0, self.margin)

    def play(self):
        self.board.draw(self.size, 0, self.margin)
        self.update()
