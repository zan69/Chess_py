from PIL import Image
from pieces import Piece

class Queen(Piece.Piece):
    def __init__(self, x: int, y: int, white: bool):
        super().__init__(x, y, white)
        if white:
            self.img = Image.open('img/white_queen.png').convert('RGBA')
        else:
            self.img = Image.open('img/black_queen.png').convert('RGBA')

    def getPossibleMoves(self, board):
        self.possible_moves = []

        i = self.x
        while i < 7:  # checando movimentos para a direita
            i = i + 1
            test = self.checkForPieceColor(board, i, self.y)
            if test == 'empty':
                self.possible_moves.append((i, self.y))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((i, self.y))
                break

        i = self.x
        while i > 0:  # checando movimentos para a esquerda
            i = i - 1
            test = self.checkForPieceColor(board, i, self.y)
            if test == 'empty':
                self.possible_moves.append((i, self.y))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((i, self.y))
                break

        i = self.y
        while i < 7:  # checando movimentos para cima
            i = i + 1
            test = self.checkForPieceColor(board, self.x, i)
            if test == 'empty':
                self.possible_moves.append((self.x, i))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((self.x, i))
                break

        i = self.y
        while i > 0:  # checando movimentos baixo
            i = i - 1
            test = self.checkForPieceColor(board, self.x, i)
            if test == 'empty':
                self.possible_moves.append((self.x, i))
            elif test == self.white:
                break
            else:
                self.possible_moves.append((self.x, i))
                break

        i = self.x
        j = self.y
        while i < 7 and j < 7:
            i = i + 1  # diagonal superior direita
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