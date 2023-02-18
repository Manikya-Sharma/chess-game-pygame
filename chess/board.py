import pygame
import piece

"""
The board is numbered as:-

            second person
   +---+---+---+---+---+---+---+---+
   |0,0|0,1|0,2|0,3|0,4|0,5|0,6|0,7|
   +---+---+---+---+---+---+---+---+
   |1,0|1,1|1,2|1,3|1,4|1,5|1,6|1,7|
   +---+---+---+---+---+---+---+---+
            first person
"""


class Square:
    def __init__(self, color, row, col, piece=None):
        self.color = color
        self.row = row
        self.col = col
        self.highlighted = False
        self.hover = False
        self.selected = False
        self.piece = piece

    def draw(self, size, p, m):
        screen = pygame.display.get_surface()
        pygame.draw.rect(
            screen,
            self.rgb_color(),
            [m + self.col * (size + p), m + self.row * (size + p), size, size],
        )
        if self.has_piece():
            self.piece.draw(p, m)

    def check_hover(self, pos_x, pos_y, size, p, m):
        if (
            pos_x >= m + self.col * (size + p)
            and pos_x <= m + self.col * (size + p) + size
        ):
            if (
                pos_y >= m + self.row * (size + p)
                and pos_y <= m + self.row * (size + p) + size
            ):
                return True

    def rgb_color(self):
        if self.hover and not (self.selected or self.highlighted):
            return (255, 204, 153)
        elif self.selected:
            return (200, 0, 0)
        elif self.highlighted:
            return (0, 255, 255)
        if self.color == "white":
            return (255, 255, 255)
        elif self.color == "black":
            return (64, 64, 64)

    def has_piece(self):
        return bool(self.piece)


class Board:
    # Board is nothing but a 2d array with extra methods
    def __init__(self, image_dict, first_person_color="white"):
        self.board = Board.make_board()
        self.color_major = first_person_color
        if self.color_major == "black":
            self.color_minor = "white"
        else:
            self.color_minor = "black"
        self.d = image_dict
        self.pieces = self.prepare_pieces(self.d)

    def highlight_square(self, row, col):
        for i in range(64):
            sq = self.board[i]
            if (sq.row, sq.col) == (row, col):
                sq.highlighted = True

    def get_all_squares_in_row(self, row):
        reqd_squares = []
        for i in range(64):
            if self.board[i].row == row:
                reqd_squares.append(self.board[i])
        return reqd_squares

    def get_all_squares_in_column(self, column):
        reqd_squares = []
        for i in range(64):
            if self.board[i].col == column:
                reqd_squares.append(self.board[i])
        return reqd_squares

    def get_all_squares_in_diagonal(self, row, col):
        i = min(row, col)
        first_row, first_col = row - i, col - i  # Get the top left diagonal piece
        redq_squares = []
        for l in range(min(8 - first_row, 8 - first_col)):
            reqd_row = first_row + l
            reqd_col = first_col + l
            for x in range(64):
                sq = self.board[x]
                if sq.row == reqd_row and sq.col == reqd_col:
                    redq_squares.append(sq)
        j = min(row, col)
        first_row, first_col = row + j, col - j  # Get the top left diagonal piece
        for k in range(max(8 - first_row, 8 - first_col)):
            reqd_row = first_row - k
            reqd_col = first_col + k
            for y in range(64):
                sq = self.board[y]
                if sq.row == reqd_row and sq.col == reqd_col:
                    redq_squares.append(sq)
        return redq_squares

    def get_horse_squares(self, row, col):
        pass  # TODO

    def get_particular_square(self, row, col):
        return self.board[row * 8 + col]  # Faster access

    def draw(self, size, p, m):
        """p:padding, m:margin"""
        for sq in self.board:
            sq.draw(size, p, m)

    def update(self, pos_x, pos_y, size, p, m):
        for sq in self.board:
            if sq.check_hover(pos_x, pos_y, size, p, m):
                sq.hover = True
            else:
                sq.hover = False

    def detect_click(self, pos_x, pos_y, size, p, m):
        for sq in self.board:
            if sq.check_hover(pos_x, pos_y, size, p, m):
                if not sq.selected:
                    sq.selected = True
                else:
                    sq.selected = False

    def remove_all_selected(self):
        for sq in self.board:
            sq.selected = False

    def prepare_pieces(self, d):
        # second person
        self.get_particular_square(0, 0).piece = piece.Rook(
            self.color_minor, 0, 0, d[self.color_minor]["rook"], -1
        )
        self.get_particular_square(0, 1).piece = piece.Knight(
            self.color_minor, 0, 1, d[self.color_minor]["knight"], -1
        )
        self.get_particular_square(0, 2).piece = piece.Bishop(
            self.color_minor, 0, 2, d[self.color_minor]["bishop"], -1
        )
        self.get_particular_square(0, 3).piece = piece.Queen(
            self.color_minor, 0, 3, d[self.color_minor]["queen"], -1
        )
        self.get_particular_square(0, 4).piece = piece.King(
            self.color_minor, 0, 4, d[self.color_minor]["king"], -1
        )
        self.get_particular_square(0, 5).piece = piece.Bishop(
            self.color_minor, 0, 5, d[self.color_minor]["bishop"], -1
        )
        self.get_particular_square(0, 6).piece = piece.Knight(
            self.color_minor, 0, 6, d[self.color_minor]["knight"], -1
        )
        self.get_particular_square(0, 7).piece = piece.Rook(
            self.color_minor, 0, 7, d[self.color_minor]["rook"], -1
        )
        for i in range(8):
            self.get_particular_square(1, i).piece = piece.Pawn(
                self.color_minor, 1, i, d[self.color_minor]["pawn"], -1
            )

        # first person
        self.get_particular_square(7, 0).piece = piece.Rook(
            self.color_minor, 7, 0, d[self.color_minor]["rook"], 1
        )
        self.get_particular_square(7, 1).piece = piece.Knight(
            self.color_minor, 7, 1, d[self.color_minor]["knight"], 1
        )
        self.get_particular_square(7, 2).piece = piece.Bishop(
            self.color_minor, 7, 2, d[self.color_minor]["bishop"], 1
        )
        self.get_particular_square(7, 3).piece = piece.Queen(
            self.color_minor, 7, 3, d[self.color_minor]["queen"], 1
        )
        self.get_particular_square(7, 4).piece = piece.King(
            self.color_minor, 7, 4, d[self.color_minor]["king"], 1
        )
        self.get_particular_square(7, 5).piece = piece.Bishop(
            self.color_minor, 7, 5, d[self.color_minor]["bishop"], 1
        )
        self.get_particular_square(7, 6).piece = piece.Knight(
            self.color_minor, 7, 6, d[self.color_minor]["knight"], 1
        )
        self.get_particular_square(7, 7).piece = piece.Rook(
            self.color_minor, 7, 7, d[self.color_minor]["rook"], 1
        )
        for i in range(8):
            self.get_particular_square(6, i).piece = piece.Pawn(
                self.color_minor, 6, i, d[self.color_minor]["pawn"], 1
            )

    @staticmethod
    def make_board():
        arr = []
        color = "white"
        for i in range(8):
            for j in range(8):
                arr.append(Square(color, i, j))
                if color == "white":
                    color = "black"
                else:
                    color = "white"
            if color == "white":
                color = "black"
            else:
                color = "white"
        return arr
