from PIL import Image
from pieces import Piece

class Knight(Piece.Piece):
    def __init__(self, x: int, y: int, white: bool):
        super().__init__(x, y, white)
        if white:
            self.img = Image.open('img/white_knight.png').convert('RGBA')
        else:
            self.img = Image.open('img/black_knight.png').convert('RGBA')

    def getPossibleMoves(self, board):
        self.possible_moves = []
        if self.x + 2 < 8:
            if self.y + 1 < 8:
                self.possible_moves.append((self.x + 2, self.y + 1))
            if self.y - 1 >= 0:
                self.possible_moves.append((self.x + 2, self.y - 1))
        if self.x - 2 >= 0:
            if self.y + 1 < 8:
                self.possible_moves.append((self.x - 2, self.y + 1))
            if self.y - 1 >= 0:
                self.possible_moves.append((self.x - 2, self.y - 1))
        if self.y + 2 < 8:
            if self.x + 1 < 8:
                self.possible_moves.append((self.x + 1, self.y + 2))
            if self.x - 1 >= 0:
                self.possible_moves.append((self.x - 1, self.y + 2))
        if self.y - 2 >= 0:
            if self.x + 1 < 8:
                self.possible_moves.append((self.x + 1, self.y - 2))
            if self.x - 1 >= 0:
                self.possible_moves.append((self.x - 1, self.y - 2))

        for i in board:
            if i.white is not self.white:
                continue
            if (i.x, i.y) in self.possible_moves:
                self.possible_moves.remove((i.x, i.y))
        return self.possible_moves

    def possible_attacks(self, board):
        return self.getPossibleMoves(board)