from pieces import utils

class Piece:
    """generic piece class"""
    def __init__(self, x: int, y: int, white: bool):
        self.x = x
        self.y = y
        self.just_moved2 = False # only used for pawns
        self.white = white

    def __str__(self):
        color = 'White' if self.white else 'Black'
        return f'{color} {self.__class__.__name__} in ({self.x},{self.y})'

    def checkForPieceColor(self, chess_board, xx, yy):
        for i in chess_board:
            if (i.x, i.y) == (xx, yy):
                return i.white
        return 'empty'

    def getPossibleMoves(self):
        pass

    def move(self, x: int, y: int, chess_board: list):
        if (x, y) in self.getPossibleMoves(chess_board):
            oldx = self.x
            oldy = self.y
            old_piece = False
            for i in chess_board:
                if (i.x, i.y) == (x, y):
                    if i.white is not self.white:
                        chess_board.remove(i)
                        old_piece = i
                if i.just_moved2:
                    i.just_moved2 = False
            self.x = x
            self.y = y
            [_, _, check] = utils.check_check(chess_board) # aqui
            if check == 'both_check' or (check == 'white_check' and self.white) or (check == 'black_check' and not self.white): # if at the end of whites move, there's a check on whites king, go back to how it was before
                if old_piece:
                    chess_board.append(old_piece)
                self.x = oldx
                self.y = oldy
                return False
            return True
        else:
            return False