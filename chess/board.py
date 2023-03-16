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
        self.column = col
        self.highlighted = False
        self.hover = False
        self.selected = False
        self.piece = piece

    def draw(self, size, p, m):
        screen = pygame.display.get_surface()
        pygame.draw.rect(
            screen,
            self.rgb_color(),
            [m + self.column * (size + p), m + self.row * (size + p), size, size],
        )
        # adding borders for more visual clarity
        if self.highlighted or self.selected:
            pygame.draw.rect(
                screen,
                tuple(map(lambda x: abs(x - 50), self.rgb_color())),
                [m + self.column * (size + p), m + self.row * (size + p), size, size],
                1,
            )
        if self.has_piece():
            self.piece.draw(p, m)

    def check_hover(self, pos_x, pos_y, size, p, m):
        if (
            pos_x >= m + self.column * (size + p)
            and pos_x <= m + self.column * (size + p) + size
        ):
            if (
                pos_y >= m + self.row * (size + p)
                and pos_y <= m + self.row * (size + p) + size
            ):
                return True

    def rgb_color(self):
        if self.has_piece() and self.piece.under_attack:
            return (255, 50, 50)
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
    def __init__(self, image_dict, first_person_color="black"):
        self.board = Board.make_board()
        self.color_major = first_person_color
        if self.color_major == "black":
            self.color_minor = "white"
            self.face_direction = 1
        else:
            self.color_minor = "black"
            self.face_direction = -1
        # self.face_direction is used to tell whose move
        self.d = image_dict
        self.prepare_pieces(self.d)

    def highlight_square(self, row, col):
        for i in range(64):
            sq = self.board[i]
            if (sq.row, sq.column) == (row, col):
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
            if self.board[i].column == column:
                reqd_squares.append(self.board[i])
        return reqd_squares

    def get_all_squares_in_diagonal(self, row, col):
        # top left to bottom right then bottom left to top right
        reqd_squares = []
        # diagonal-1
        input_data_d1 = [row, col]
        min_d1 = min(input_data_d1)
        input_data_d1[0] = input_data_d1[0] - min_d1
        input_data_d1[1] = input_data_d1[1] - min_d1
        # now input_data_d1 has top left square
        while max(input_data_d1) < 8:
            reqd_squares.append(
                self.get_particular_square(input_data_d1[0], input_data_d1[1])
            )
            input_data_d1[0] += 1
            input_data_d1[1] += 1

        # # diagonal-2
        row = 7 - row
        # consider transformation of rotating the board 180 degree
        # now we need to follow same procedure
        input_data_d2 = [row, col]
        min_d2 = min(input_data_d2)
        input_data_d2[0] = input_data_d2[0] - min_d2
        input_data_d2[1] = input_data_d2[1] - min_d2
        # now input_data_d2 has top left square (for rotated board)
        while max(input_data_d2) < 8:
            reqd_squares.append(
                self.get_particular_square(7 - input_data_d2[0], input_data_d2[1])
            )
            input_data_d2[0] += 1
            input_data_d2[1] += 1
        return reqd_squares

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
            if sq.has_piece():
                if len(sq.piece.attacking) == 0:
                    sq.piece.is_attacking = False
                if sq.piece.face_direction == self.face_direction:
                    for possible_move in sq.piece.get_next_possible_moves(self):
                        if possible_move.has_piece():  # under attack
                            possible_move.piece.set_under_attack(sq.piece)

    def detect_right_click(self, pos_x, pos_y, size, p, m):
        for sq in self.board:
            if sq.check_hover(pos_x, pos_y, size, p, m):
                if not sq.selected:
                    sq.selected = True
                else:
                    sq.selected = False

    def detect_left_click(self, pos_x, pos_y, size, p, m):
        for sq in self.board:
            if sq.check_hover(pos_x, pos_y, size, p, m):
                if sq.has_piece() and not sq.highlighted:
                    if sq.piece.face_direction != self.face_direction:
                        continue
                    if sq.piece.wants_to_move:
                        self.remove_all_highlighted()
                        piece.ChessPiece.remove_all_pieces_want_to_move()
                        continue  # click again on the piece to remove highlight.
                        # ! note continue here, might cause errors if
                        # ! more statements added to the loop.
                    for n_sq in sq.piece.get_next_possible_moves(self):
                        n_sq.highlighted = True
                        piece.ChessPiece.remove_all_pieces_want_to_move()
                        sq.piece.wants_to_move = True
                elif sq.highlighted:
                    for _piece in piece.ChessPiece.pieces:
                        if _piece.wants_to_move:
                            if sq.has_piece():
                                piece.ChessPiece.pieces.remove(sq.piece)
                            self.get_particular_square(
                                _piece.row, _piece.column
                            ).piece = None
                            _piece.row, _piece.column = sq.row, sq.column
                            sq.piece = _piece
                            self.remove_all_highlighted()
                            sq.piece.wants_to_move = False
                            self.face_direction *= -1
                            piece.ChessPiece.remove_all_under_attack()

    def is_click_on_highlighted(self, pos_x, pos_y, size, p, m):
        for sq in self.board:
            if sq.check_hover(pos_x, pos_y, size, p, m):
                if sq.highlighted:
                    return True
                else:
                    return False

    def remove_all_selected(self):
        for sq in self.board:
            sq.selected = False

    def remove_all_highlighted(self):
        for sq in self.board:
            sq.highlighted = False
            if sq.has_piece():
                sq.piece.want_to_move = False

    def prepare_pieces(self, d):
        # second person
        self.get_particular_square(0, 0).piece = piece.Rook(
            self.color_minor, 0, 0, d[self.color_minor]["rook"], 1
        )
        self.get_particular_square(0, 1).piece = piece.Knight(
            self.color_minor, 0, 1, d[self.color_minor]["knight"], 1
        )
        self.get_particular_square(0, 2).piece = piece.Bishop(
            self.color_minor, 0, 2, d[self.color_minor]["bishop"], 1
        )
        self.get_particular_square(0, 3).piece = piece.Queen(
            self.color_minor, 0, 3, d[self.color_minor]["queen"], 1
        )
        self.get_particular_square(0, 4).piece = piece.King(
            self.color_minor, 0, 4, d[self.color_minor]["king"], 1
        )
        self.get_particular_square(0, 5).piece = piece.Bishop(
            self.color_minor, 0, 5, d[self.color_minor]["bishop"], 1
        )
        self.get_particular_square(0, 6).piece = piece.Knight(
            self.color_minor, 0, 6, d[self.color_minor]["knight"], 1
        )
        self.get_particular_square(0, 7).piece = piece.Rook(
            self.color_minor, 0, 7, d[self.color_minor]["rook"], 1
        )
        for i in range(8):
            self.get_particular_square(1, i).piece = piece.Pawn(
                self.color_minor, 1, i, d[self.color_minor]["pawn"], 1
            )

        # first person
        self.get_particular_square(7, 0).piece = piece.Rook(
            self.color_major, 7, 0, d[self.color_major]["rook"], -1
        )
        self.get_particular_square(7, 1).piece = piece.Knight(
            self.color_major, 7, 1, d[self.color_major]["knight"], -1
        )
        self.get_particular_square(7, 2).piece = piece.Bishop(
            self.color_major, 7, 2, d[self.color_major]["bishop"], -1
        )
        self.get_particular_square(7, 3).piece = piece.Queen(
            self.color_major, 7, 3, d[self.color_major]["queen"], -1
        )
        self.get_particular_square(7, 4).piece = piece.King(
            self.color_major, 7, 4, d[self.color_major]["king"], -1
        )
        self.get_particular_square(7, 5).piece = piece.Bishop(
            self.color_major, 7, 5, d[self.color_major]["bishop"], -1
        )
        self.get_particular_square(7, 6).piece = piece.Knight(
            self.color_major, 7, 6, d[self.color_major]["knight"], -1
        )
        self.get_particular_square(7, 7).piece = piece.Rook(
            self.color_major, 7, 7, d[self.color_major]["rook"], -1
        )
        for i in range(8):
            self.get_particular_square(6, i).piece = piece.Pawn(
                self.color_major, 6, i, d[self.color_major]["pawn"], -1
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
