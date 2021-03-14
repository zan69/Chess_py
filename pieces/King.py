from PIL import Image
from pieces import Piece

class King(Piece.Piece):
    def __init__(self, x: int, y: int, white: bool):
        super().__init__(x, y, white)
        self.moves = 0
        if white:
            self.img = Image.open('img/white_king.png').convert('RGBA')
        else:
            self.img = Image.open('img/black_king.png').convert('RGBA')

    def getPossibleMoves(self, board):
        #possible_attacks = []
        #for i in board:
        #    if (i.white is not self.white):
        #        possible_attacks.extend(i.possible_attacks(board))
        #print('color: ' + str(self.white))
        #print(possible_attacks)
        self.possible_moves = []
        for di in [0, 1, -1]:
            for dj in [0, 1, -1]:
                if dj==0 and di==0:
                    continue
                i = self.x + di
                j = self.y + dj
                if (0 <= i <= 7) and (0 <= j <= 7):
                    test = self.checkForPieceColor(board, i, j)
                    if test == 'empty':# and (i, j) not in possible_attacks:
                        self.possible_moves.append((i, j))
                    elif test == self.white:
                        continue
                    else:# (i, j) not in possible_attacks:
                        self.possible_moves.append((i, j))
        return self.possible_moves

    def possible_attacks(self, board):
        possible_attacks = []
        for di in [0, 1, -1]:
            for dj in [0, 1, -1]:
                i = self.x + di
                j = self.y + dj
                if (0 <= i <= 7) and (0 <= j <= 7):
                    possible_attacks.append((i, j))
        possible_attacks.remove((self.x, self.y))
        return possible_attacks
    
    def move(self, x: int, y: int, chess_board: list):
        if super().move(x, y, chess_board):
            self.moves += 1
            return True
        else:
            return False