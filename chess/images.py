import pygame


class Images:
    def __init__(self, size):
        self.d = {"black": {}, "white": {}}
        self.size = size
        self.init_images()
        self.prepare_images()

    def init_images(self):
        # TODO: change the main directory to ./chess
        self.d["black"]["king"] = pygame.image.load("./images/black/king.png")
        self.d["black"]["queen"] = pygame.image.load("./images/black/queen.png")
        self.d["black"]["bishop"] = pygame.image.load("./images/black/bishop.png")
        self.d["black"]["rook"] = pygame.image.load("./images/black/rook.png")
        self.d["black"]["pawn"] = pygame.image.load("./images/black/pawn.png")
        self.d["black"]["knight"] = pygame.image.load("./images/black/knight.png")

        self.d["white"]["king"] = pygame.image.load("./images/white/king.png")
        self.d["white"]["queen"] = pygame.image.load("./images/white/queen.png")
        self.d["white"]["bishop"] = pygame.image.load("./images/white/bishop.png")
        self.d["white"]["rook"] = pygame.image.load("./images/white/rook.png")
        self.d["white"]["pawn"] = pygame.image.load("./images/white/pawn.png")
        self.d["white"]["knight"] = pygame.image.load("./images/white/knight.png")

    def get_images(self):
        return self.d

    def get_white_images(self):
        return self.d["white"]

    def get_black_images(self):
        return self.d["black"]

    def prepare_images(self):
        for dic in self.d.values():
            for key, img in dic.items():
                img.set_colorkey((255, 0, 255))
                dic[key] = pygame.transform.scale(img, (self.size, self.size))
