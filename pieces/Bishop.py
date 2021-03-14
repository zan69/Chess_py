from PIL import Image
from pieces import Piece

class Bishop(Piece.Piece):
    def __init__(self, x: int, y: int, white: bool):
        super().__init__(x, y, white)
        if white:
            self.img = Image.open('img/white_bishop.png').convert('RGBA')
        else:
            self.img = Image.open('img/black_bishop.png').convert('RGBA')

    def getPossibleMoves(self, board):
        self.possible_moves = []

        i = self.x
        j = self.y
        while i < 7 and j < 7:
            i = i + 1 # diagonal superior direita
            j = j + 1
            test = self.checkForPieceColor(board, i, j)
            if test == 'empty':
                self.possible_moves.append((i, j))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((i, j))
                break

        i = self.x
        j = self.y
        while i > 0 and j < 7:
            i = i - 1  # diagonal superior esquerda
            j = j + 1
            test = self.checkForPieceColor(board, i, j)
            if test == 'empty':
                self.possible_moves.append((i, j))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((i, j))
                break

        i = self.x
        j = self.y
        while i < 7 and j > 0:
            i = i + 1  # diagonal inferior direita
            j = j - 1
            test = self.checkForPieceColor(board, i, j)
            if test == 'empty':
                self.possible_moves.append((i, j))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((i, j))
                break

        i = self.x
        j = self.y
        while i > 0 and j > 0:
            i = i - 1  # diagonal inferior esquerda
            j = j - 1
            test = self.checkForPieceColor(board, i, j)
            if test == 'empty':
                self.possible_moves.append((i, j))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((i, j))
                break
        return self.possible_moves

    def possible_attacks(self, board):
        return self.getPossibleMoves(board)