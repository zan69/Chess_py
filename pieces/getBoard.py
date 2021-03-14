from PIL import Image

pos0 = [
    ['bRook',  'bKnight',  'bBishop',  'bQueen',  'bKing',  'bBishop',  'bKnight',  'bRook'],
    ['bPawn',  'bPawn',    'bPawn',    'bPawn',   'bPawn',  'bPawn',    'bPawn',    'bPawn'],
    [ '',      '',         '',         '',        '',       '',         '',         ''     ],
    [ '',      '',         '',         '',        '',       '',         '',         ''     ],
    [ '',      '',         '',         'wPawn',   '',       '',         '',         ''     ],
    [ '',      '',         '',         '',        '',       '',         '',         ''     ],
    ['wPawn',  'wPawn',    'wPawn',    '',        'wPawn',  'wPawn',    'wPawn',    'wPawn'],
    ['wRook',  'wKnight',  'wBishop',  'wQueen',  'wKing',  'wBishop',  'wKnight',  'wRook']
]


piece = {
    'wPawn': Image.open('img/white_pawn.png').convert('RGBA'),
    'wKnight': Image.open('img/white_knight.png').convert('RGBA'),
    'wBishop': Image.open('img/white_bishop.png').convert('RGBA'),
    'wRook': Image.open('img/white_rook.png').convert('RGBA'),
    'wQueen': Image.open('img/white_queen.png').convert('RGBA'),
    'wKing': Image.open('img/white_king.png').convert('RGBA'),
    'bPawn': Image.open('img/black_pawn.png').convert('RGBA'),
    'bKnight': Image.open('img/black_knight.png').convert('RGBA'),
    'bBishop': Image.open('img/black_bishop.png').convert('RGBA'),
    'bRook': Image.open('img/black_rook.png').convert('RGBA'),
    'bQueen': Image.open('img/black_queen.png').convert('RGBA'),
    'bKing': Image.open('img/black_king.png').convert('RGBA')
}



def blackBoard(pos):
    pos.reverse()
    for i in range(8):
        pos[i].reverse()
    return pos


def getBoard(pos = pos0, white=True):
    if white:
        board = Image.open("img/board_w.png").convert('RGBA')
    else:
        board = Image.open("img/board_b.png").convert('RGBA')
        pos = blackBoard(pos)

    for i in range(8):
        for j in range(8):
            if pos[j][i]:
                board.paste(piece[pos[j][i]], (i*50, j*50), piece[pos[j][i]])
    board.save('out.png')

getBoard()

