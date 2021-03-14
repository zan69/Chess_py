from PIL import Image
from pieces import Piece
from pieces import utils
from pieces.Queen import Queen

class Pawn(Piece.Piece):
    def __init__(self, x: int, y: int, white: bool):
        super().__init__(x, y, white)
        self.moves = 0
        if white:
            self.img = Image.open('img/white_pawn.png').convert('RGBA')
        else:
            self.img = Image.open('img/black_pawn.png').convert('RGBA')


    def getPossibleMoves(self, board):
        if self.white:
            self.possible_moves = [(self.x, self.y+1)] # para frente
            if self.moves == 0:
                self.possible_moves.append((self.x, self.y+2)) # move 2 para frente se não se moveu ainda
            for i in board:
                if (i.x, i.y) == (self.x, self.y):
                    continue
                if (i.x, i.y) in self.possible_moves and i.x == self.x and (i.y == self.y + 1 or i.y == self.y + 2):
                    self.possible_moves.remove((i.x, i.y))  # se tiver alguem na frente não pode mover para la
                    if (self.x, self.y - 2) in self.possible_moves:
                        self.possible_moves.remove((self.x, self.y + 2))
                if (i.x == self.x + 1 or i.x == self.x-1) and (i.y == self.y + 1) and not i.white:
                    self.possible_moves.append((i.x, i.y)) # comer uma peça na diagonal
                if type(i) == type(self) and self.y == 4 and self.y == i.y and i.moves == 1 and i.just_moved2:
                    self.possible_moves.append((i.x, i.y+1)) # en passant
            return self.possible_moves
        else:
            self.possible_moves = [(self.x, self.y - 1)]  # para frente (baixo)
            if self.moves == 0:
                self.possible_moves.append((self.x, self.y - 2))  # move 2 para frente (baixo) se não se moveu ainda
            for i in board:
                if (i.x, i.y) == (self.x, self.y):
                    pass
                if (i.x, i.y) in self.possible_moves and i.x == self.x and (i.y == self.y - 1 or i.y == self.y - 2):
                    self.possible_moves.remove((i.x, i.y))  # se tiver alguem na frente (baixo) não pode mover para la
                    if (self.x, self.y - 2) in self.possible_moves:
                        self.possible_moves.remove((self.x, self.y - 2))
                if (i.x == self.x + 1 or i.x == self.x - 1) and (i.y == self.y - 1) and i.white:
                    self.possible_moves.append((i.x, i.y))  # comer uma peça na diagonal
                if type(i) == type(self) and self.y == 3 and self.y == i.y and i.moves == 1 and i.just_moved2:
                    self.possible_moves.append((i.x, i.y - 1)) # en passant
            return self.possible_moves


    def possible_attacks(self, board):
        if self.white:
            return [(self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]
        else:
            return [(self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]


    def move(self, x: int, y: int, board: list):
        if (x, y) in self.getPossibleMoves(board):
            oldx = self.x
            oldy = self.y
            old_piece = False
            for i in board:
                if (i.x, i.y) == (x, y):
                    if i.white is not self.white:
                        board.remove(i)
                        old_piece = i
                if isinstance(i, Pawn):
                    i.just_moved2 = False
            self.x = x
            self.y = y
            [_, _, check] = utils.check_check(board) # aqui
            if check == 'both_check' or (check == 'white_check' and self.white) or (check == 'black_check' and not self.white): # if at the end of x move, there's a check on x king, go back to how it was before
                if old_piece:
                    board.append(old_piece)
                self.x = oldx
                self.y = oldy
                return False
            if abs(oldx-self.x) == 1 and not old_piece: # if it moved to the side, but never removed a piece -> en passant -> remove the piece behind it
                deltay = 1 if self.white else -1
                for i in board:
                    if (i.x, i.y) == (self.x, self.y-deltay):
                        board.remove(i)
            if abs(self.y - oldy) == 2: # just_moved2 flag - for en passant
                self.just_moved2 = True
            if self.y == 7 or self.y == 0: # if pawn gets to the end of the board, promote
                board.remove(self)
                board.append(Queen(self.x, self.y, self.white))        
            self.moves += 1
            return True
        else:
            return False