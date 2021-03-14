from PIL import Image
from pieces import Piece

class Rook(Piece.Piece):
    def __init__(self, x: int, y: int, white: bool):
        super().__init__(x, y, white)
        self.moves = 0
        if white:
            self.img = Image.open('img/white_rook.png').convert('RGBA')
        else:
            self.img = Image.open('img/black_rook.png').convert('RGBA')

    def getPossibleMoves(self, board):
        self.possible_moves = []

        i = self.x
        while i < 7: # checando movimentos para a direita
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
        while i > 0: # checando movimentos para a esquerda
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
        return self.possible_moves

    def possible_attacks(self, board):
        return self.getPossibleMoves(board)

    def move(self, x: int, y: int, chess_board: list):
        if super().move(x, y, chess_board):
            self.moves += 1
            return True
        else:
            return False