import pygame


class ChessPiece:
    pieces = []

    def __init__(self, color, row, column, image, face_direction=-1):
        # face_direction: -1 => first player
        # face_direction: +1 => second player
        self.color = color
        self.row = row
        self.column = column
        self.img = image
        self.face_direction = face_direction
        self.wants_to_move = False
        ChessPiece.pieces.append(self)

    def draw(self, p, m):
        screen = pygame.display.get_surface()
        size = self.img.get_width()
        screen.blit(self.img, (m + self.column * (size + p), m + self.row * (size + p)))

    def get_next_possible_moves(self, board):
        print("There seems to be an error")
        return []
        # Every piece which inherits must implement this method its own way

    @classmethod
    def remove_all_pieces_want_to_move(cls):
        for pc in cls.pieces:
            pc.wants_to_move = False


class Pawn(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)

    def get_next_possible_moves(self, board):
        possible_moves = []
        for sq in board.get_all_squares_in_diagonal(self.row, self.column):
            if self.face_direction == -1:
                if self.row < sq.row:
                    continue
            elif self.face_direction == 1:
                if self.row > sq.row:
                    continue
            if abs(sq.row - self.row) == 1 and abs(sq.column - self.column) == 1:
                if sq.has_piece():
                    if sq.piece.color != self.color:
                        possible_moves.append(sq)
        try:
            front_piece = board.get_particular_square(
                self.row + self.face_direction, self.column
            )
        except IndexError:  # Should not have occurred since pawn reached opponent's end
            return possible_moves
        if not front_piece.has_piece():
            possible_moves.append(front_piece)
        return possible_moves


class Rook(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)

    def get_next_possible_moves(self, board):
        possible_moves_row = []
        possible_moves_column = []
        for row_sq in board.get_all_squares_in_row(self.row):
            if row_sq.has_piece() and row_sq.piece == self:
                continue
            if row_sq.has_piece():
                if row_sq.column < self.column:
                    possible_moves_row.clear()  # remove all squares to left
                    if row_sq.piece.color != self.color:
                        possible_moves_row.append(row_sq)
                elif row_sq.column > self.column:
                    if row_sq.piece.color != self.color:
                        possible_moves_row.append(row_sq)
                    break
                continue
            possible_moves_row.append(row_sq)
        for column_sq in board.get_all_squares_in_column(self.column):
            if column_sq.has_piece() and column_sq.piece == self:
                continue
            if column_sq.has_piece():
                if column_sq.row < self.row:
                    possible_moves_column.clear()  # remove all squares to top
                    if column_sq.piece.color != self.color:
                        possible_moves_column.append(column_sq)
                elif column_sq.row > self.row:
                    if column_sq.piece.color != self.color:
                        possible_moves_column.append(column_sq)
                    break
                continue
            possible_moves_column.append(column_sq)
        possible_moves_row.extend(possible_moves_column)
        return possible_moves_row


class Knight(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)


class Bishop(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)

    def get_next_possible_moves(self, board):
        possible_moves_d1 = []
        possible_moves_d2 = []
        stop_d1 = False
        stop_d2 = False
        for cell in board.get_all_squares_in_diagonal(self.row, self.column):
            # top left to bottom right and bottom left to top right
            if cell.has_piece() and cell.piece == self:
                continue
            # diagonal-1
            if cell.row < self.row and cell.column < self.column:
                if cell.has_piece():
                    possible_moves_d1.clear()
                    if cell.piece.color == self.color:
                        continue
                possible_moves_d1.append(cell)
            elif cell.row > self.row and cell.column > self.column:
                if stop_d1:
                    continue
                if cell.has_piece():
                    stop_d1 = True
                    if cell.piece.color == self.color:
                        continue
                possible_moves_d1.append(cell)
            # diagonal-2
            elif cell.row > self.row and cell.column < self.column:
                if cell.has_piece():
                    possible_moves_d2.clear()
                    if cell.piece.color == self.color:
                        continue
                possible_moves_d2.append(cell)
            elif cell.row < self.row and cell.column > self.column:
                if stop_d2:
                    continue
                if cell.has_piece():
                    stop_d2 = True
                    if cell.piece.color == self.color:
                        continue
                possible_moves_d2.append(cell)
        possible_moves_d1.extend(possible_moves_d2)
        return possible_moves_d1


class Queen(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)


class King(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)
