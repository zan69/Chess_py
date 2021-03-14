from pieces.Knight import Knight
from pieces.Pawn import Pawn
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from pieces.Queen import Queen
from pieces.King import King
from PIL import Image
import copy

def getBoard(b, white, id, red_square=False):
    if white:
        board_img = Image.open("img/board_w.png").convert('RGBA')
        if red_square:
            square_img = Image.open("img/red_square.png").convert('RGBA')
            board_img.paste(square_img, (red_square[0] * 50, abs(red_square[1] - 7) * 50), square_img)
        for p in b:
            board_img.paste(p.img, (p.x * 50, abs(p.y - 7) * 50), p.img)
    else:
        board_img = Image.open("img/board_b.png").convert('RGBA')
        if red_square:
            square_img = Image.open("img/red_square.png").convert('RGBA')
            board_img.paste(square_img, (abs(red_square[0] - 7) * 50, red_square[1] * 50), square_img)
        for p in b:
            board_img.paste(p.img, (abs(p.x - 7) * 50, p.y * 50), p.img)
    board_img.save(id+'.png')


def initialize_board():
    b0 = [Rook(0, 7, False), Knight(1, 7, False), Bishop(2, 7, False), Queen(3, 7, False), King(4, 7, False), Bishop(5, 7, False), Knight(6, 7, False), Rook(7, 7, False),
          Pawn(0, 6, False), Pawn(1, 6, False),   Pawn(2, 6, False),   Pawn(3, 6, False),  Pawn(4, 6, False), Pawn(5, 6, False),   Pawn(6, 6, False),   Pawn(7, 6, False),
          Pawn(0, 1, True),  Pawn(1, 1, True),    Pawn(2, 1, True),    Pawn(3, 1, True),   Pawn(4, 1, True),  Pawn(5, 1, True),    Pawn(6, 1, True),    Pawn(7, 1, True),
          Rook(0, 0, True),  Knight(1, 0, True),  Bishop(2, 0, True),  Queen(3, 0, True),  King(4, 0, True),  Bishop(5, 0, True),  Knight(6, 0, True),  Rook(7, 0, True)
          ]
    return b0

def parseCommand(command : str): #e2e4
    if command == "0-0-0":
        return [0, 0, 0, 0] # long castle code
    elif command == "0-0":
        return [1, 1, 1, 1] # short castle
    elif command == "-draw":
        return [0, 0, 1, 1] # draw proposal
    elif command == "-forfeit":
        return [1, 1, 0, 0] # forfeit
    try:
        x0 = letter2number(command[0])
        y0 = int(command[1])-1
        x1 = letter2number(command[2])
        y1 = int(command[3])-1
        print(f'({x0},{y0}) -> ({x1},{y1})')
        return [x0, y0, x1, y1]
    except:
        return False

def letter2number(letter):
    if letter == 'a':
        return 0
    if letter == 'b':
        return 1
    if letter == 'c':
        return 2
    if letter == 'd':
        return 3
    if letter == 'e':
        return 4
    if letter == 'f':
        return 5
    if letter == 'g':
        return 6
    if letter == 'h':
        return 7


def movePiece(x0, y0, x1, y1, board, white):
    if [x0, y0, x1, y1] == [0, 0, 0, 0]:
        return long_castle(board, white)
    elif [x0, y0, x1, y1] == [1, 1, 1, 1]:
        return short_castle(board, white)
    for i in board:
        if (x0, y0) == (i.x, i.y):
            if i.white is white:
                if i.move(x1, y1, board):
                    return 'moveu'
                else:
                    return 'invalido'
            return 'wrong color'
    return 'not found'


def check_check(board):
    flag1 = False #whitekingposition
    flag2 = False #blackkingposition
    flag3 = False #whitecheck / blackcheck / bothcheck
    for i in board:
        if isinstance(i, King):
            if i.white:
                whiteKingPosition = (i.x, i.y)
            else:
                blackKingPosition = (i.x, i.y)
    for i in board:
        possible_attacks = i.possible_attacks(board)
        if i.white is False and whiteKingPosition in possible_attacks: # aqui
            flag1 = whiteKingPosition
            if flag3=='black_check':
                flag3 = 'both_check'
            elif flag3 is False: 
                flag3 = 'white_check'
            # if white king is under attack
        if i.white and blackKingPosition in possible_attacks:
            flag2 = blackKingPosition
            if flag3=='white_check':
                flag3 = 'both_check'
            elif flag3 is False:
                flag3 = 'black_check'

            # if black king is under attack
    return [flag1, flag2, flag3]


def check_stalemate(board, white): # are there any moves the player can do?
    if len(board) == 2:
        return True
    testBoard = copy.deepcopy(board)
    for i in range(len(testBoard)):
        if testBoard[i].white is not white:
            continue
        possible_moves = testBoard[i].getPossibleMoves(testBoard)
        for movimento in possible_moves:
            if testBoard[i].move(movimento[0], movimento[1], testBoard):
                return False
            else:
                testBoard = copy.deepcopy(board)
    return True

def print_board(board):
    for i in board:
        print(i, end=', ')
    print()

def check_attacks(board, squares, white): # check attacks in the 3 squares the king will have to go through in a castle
    for i in board:
        if i.white == white:
            continue
        possible_attacks = i.possible_attacks(board)
        if any(square in possible_attacks for square in squares):
            return True # returns true if one of the squares are being attacked
    return False #returns false if they're clear


def short_castle(board, white):
    king = False
    rook = False
    doable = True
    if white:
        for i in board:
            if not i.white:
                continue
            if (i.x, i.y) == (4, 0) and isinstance(i, King) and i.moves==0:
                king = i
            if (i.x, i.y) == (7, 0) and isinstance(i, Rook) and i.moves==0:
                rook = i
            if (i.x, i.y) == (5, 0) or (i.x, i.y) == (6, 0):
                doable = False
        if not all([king, rook]) or not doable:
            return 'invalido'
        if check_attacks(board, [(4,0),(5,0),(6,0)], white):
            return 'invalido'
        board.remove(king)
        board.remove(rook)
        board.append(King(6, 0, True))
        board.append(Rook(5, 0, True))
        return 'moveu'
    else:
        for i in board:
            if i.white:
                continue
            if (i.x, i.y) == (4, 7) and isinstance(i, King) and i.moves==0:
                king = i
            if (i.x, i.y) == (7, 7) and isinstance(i, Rook) and i.moves==0:
                rook = i
            if (i.x, i.y) == (5, 7) or (i.x, i.y) == (6, 7):
                doable = False
        if not all([king, rook]) or not doable:
            return 'invalido'
        if check_attacks(board, [(4,7),(5,7),(6,7)], white):
            return 'invalido'
        board.remove(king)
        board.remove(rook)
        board.append(King(6, 7, False))
        board.append(Rook(5, 7, False))
        return 'moveu'
        
def long_castle(board, white):
    king = False
    rook = False
    doable = True
    if white:
        for i in board:
            if not i.white:
                continue
            if (i.x, i.y) == (4, 0) and isinstance(i, King) and i.moves==0:
                king = i
            if (i.x, i.y) == (0, 0) and isinstance(i, Rook) and i.moves==0:
                rook = i
            if (i.x, i.y) == (1, 0) or (i.x, i.y) == (2, 0) or (i.x, i.y) == (3, 0):
                doable = False
        if not all([king, rook]) or not doable:
            return 'invalido'
        if check_attacks(board, [(4,0),(2,0),(3,0)], white):
            return 'invalido'
        board.remove(king)
        board.remove(rook)
        board.append(King(2, 0, True))
        board.append(Rook(3, 0, True))
        return 'moveu'
    else:
        for i in board:
            if i.white:
                continue
            if (i.x, i.y) == (4, 7) and isinstance(i, King) and i.moves==0:
                king = i
            if (i.x, i.y) == (0, 7) and isinstance(i, Rook) and i.moves==0:
                rook = i
            if (i.x, i.y) == (1, 7) or (i.x, i.y) == (2, 7) or (i.x, i.y) == (3, 7):
                doable = False
        if not all([king, rook]) or not doable:
            return 'invalido'
        if check_attacks(board, [(4,7),(3,7),(2,7)], white):
            return 'invalido'
        board.remove(king)
        board.remove(rook)
        board.append(King(2, 7, False))
        board.append(Rook(3, 7, False))
        return 'moveu'