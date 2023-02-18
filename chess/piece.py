import pygame


class ChessPiece:
    def __init__(self, color, row, column, image, face_direction=-1):
        # face_direction: -1 => first player
        # face_direction: +1 => second player
        self.color = color
        self.row = row
        self.column = column
        self.img = image
        self.face_direction = face_direction

    def draw(self, p, m):
        screen = pygame.display.get_surface()
        size = self.img.get_width()
        screen.blit(self.img, (m + self.column * (size + p), m + self.row * (size + p)))

    def get_next_possible_moves(self, board):
        print("There seems to be an error")
        return []
        # Every piece which inherits must implement this method its own way


class Pawn(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)

    def get_next_possible_moves(self, board):
        possible_moves = []
        for sq in board.get_all_squares_in_diagonal(self.row, self.column):
            if self.face_direction == 1:
                if self.row < sq.row:
                    continue
            elif self.face_direction == -1:
                if self.row > sq.row:
                    continue
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


class Knight(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)


class Bishop(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)


class Queen(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)


class King(ChessPiece):
    def __init__(self, color, row, column, image, face_direction=+1):
        super().__init__(color, row, column, image, face_direction)
