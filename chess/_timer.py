import pygame


class Timer:
    def __init__(self):
        self.i = pygame.time.get_ticks()

    def get_time(self):
        return pygame.time.get_ticks() - self.i

    def reset(self):
        self.i = pygame.time.get_ticks()
