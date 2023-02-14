import pygame

class Images:
    def __init__(self):
        self.d = {"black":{}, "white":{}}
        self.init_images()

    def init_images(self):
        self.d["black"]["king"] = pygame.image.load("./chess/images/black/king.png")
        self.d["black"]["queen"] = pygame.image.load("./chess/images/black/queen.png")
        self.d["black"]["bishop"] = pygame.image.load("./chess/images/black/bishop.png")
        self.d["black"]["rook"] = pygame.image.load("./chess/images/black/rook.png")
        self.d["black"]["pawn"] = pygame.image.load("./chess/images/black/pawn.png")
        self.d["white"]["king"] = pygame.image.load("./chess/images/black/king.png")
        self.d["white"]["queen"] = pygame.image.load("./chess/images/black/queen.png")
        self.d["white"]["bishop"] = pygame.image.load("./chess/images/black/bishop.png")
        self.d["white"]["rook"] = pygame.image.load("./chess/images/black/rook.png")
        self.d["white"]["pawn"] = pygame.image.load("./chess/images/black/pawn.png")

    def get_images(self):
        return self.d

    def get_white_images(self):
        return self.d["white"]

    def get_black_images(self):
        return self.d["black"]