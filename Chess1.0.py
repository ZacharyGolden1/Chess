# Step1: make the board                     -- Done
# Step2: make the pieces                    -- Done
# Step3: create movement                    -- Done
# Step4: check general legality of movement -- isLegalMove is --severely-- bugged
# Step5: color possible board moves         -- ^^^^^^^^^^^^
# Step6: create piece capturing             -- buggy (you can capture a piece without moving to that square)
# Step7: create turns                       -- Done
# Step8: flip the board                     -- Done
# Step9: implement gameover/restart         -- ...
# Step10: create A.I. to play against       -- ...
# Step11: title screen other UI stuff       -- ...
# Step12: immplement different gamemodes
#         and a gameclock                   -- ...


from cmu_112_graphics import *

def appStarted(app):
    #initializing board size
    app.rows,app.cols,app.cellSize,app.margin,app.width,app.height = gameDimensions()

    # checks for board flippage:
    app.boardFlip = False

    # Passed piece toggle check
    app.passedPiece = False

    # Creates the color of the cell
    app.cellColor = ['white','lightgray','cyan']
    app.blueRowCol = []

    # Mouse press Coordinate vars
    app.x = app.y = 1000

    # Mouse released Coordinate vars
    app.xx = app.yy = 10000

    # placement of captured pieces:
    app.whitePlace = -1
    app.blackPlace = -1

    # Toggle for who's turn it is:
    app.isWhiteTurn = True

    # piece position to start (row,col,unicode character) 
    # BLACK
    app.blackKingCoords = [3,0,'\u265A']
    app.lBlackKnightCoords = [1,0,'\u265E']
    app.rBlackKnightCoords = [6,0,'\u265E']
    app.lBlackRookCoords = [0,0,'\u265C']
    app.rBlackRookCoords = [7,0,'\u265C']
    app.blackQueenCoords = [4,0,'\u265B']
    app.lBlackBishopCoords = [2,0,'\u265D']
    app.rBlackBishopCoords = [5,0,'\u265D']
    app.blackPawnCoords = [[0,1,'\u265F'],[1,1,'\u265F'],[2,1,'\u265F'],
                           [3,1,'\u265F'],[4,1,'\u265F'],[5,1,'\u265F'],
                           [6,1,'\u265F'],[7,1,'\u265F']]

    #WHITE
    app.whiteKingCoords = [4,7,'\u2654']
    app.lWhiteKnightCoords = [1,7,'\u2658']
    app.rWhiteKnightCoords = [6,7,'\u2658']
    app.lWhiteRookCoords = [0,7,'\u2656']
    app.rWhiteRookCoords = [7,7,'\u2656']
    app.whiteQueenCoords = [3,7,'\u2655']
    app.lWhiteBishopCoords = [2,7,'\u2657']
    app.rWhiteBishopCoords = [5,7,'\u2657']
    app.whitePawnCoords = [[0,6,'\u2659'],[1,6,'\u2659'],[2,6,'\u2659'],
                           [3,6,'\u2659'],[4,6,'\u2659'],[5,6,'\u2659'],
                           [6,6,'\u2659'],[7,6,'\u2659']]

    #All Pieces:
    app.pieces = [app.blackKingCoords,
                  app.lBlackKnightCoords,
                  app.rBlackKnightCoords,
                  app.lBlackRookCoords,
                  app.rBlackRookCoords,
                  app.blackQueenCoords,
                  app.lBlackBishopCoords,
                  app.rBlackBishopCoords,
                  app.blackPawnCoords,
                  app.whiteKingCoords,
                  app.lWhiteKnightCoords,
                  app.rWhiteKnightCoords,
                  app.lWhiteRookCoords,
                  app.rWhiteRookCoords,
                  app.whiteQueenCoords,
                  app.lWhiteBishopCoords,
                  app.rWhiteBishopCoords,
                  app.whitePawnCoords]
    
    #Black Pieces
    app.blackPieces = [app.blackKingCoords,
                  app.lBlackKnightCoords,
                  app.rBlackKnightCoords,
                  app.lBlackRookCoords,
                  app.rBlackRookCoords,
                  app.blackQueenCoords,
                  app.lBlackBishopCoords,
                  app.rBlackBishopCoords,
                  app.blackPawnCoords]

    #White Pieces
    app.whitePieces = [app.whiteKingCoords,
                  app.lWhiteKnightCoords,
                  app.rWhiteKnightCoords,
                  app.lWhiteRookCoords,
                  app.rWhiteRookCoords,
                  app.whiteQueenCoords,
                  app.lWhiteBishopCoords,
                  app.rWhiteBishopCoords,
                  app.whitePawnCoords]
    #current piece
    app.currPiece = 0

def gameDimensions():
    rows = cols = 8
    cellSize = 50
    margin = 70
    width = height = cellSize*rows+2*margin
    return (rows,cols,cellSize,margin,width,height)

def keyPressed(app,event):
    if event.key == 'r':
        appStarted(app)

def mousePressed(app,event):
    app.x,app.y = event.x,event.y
    row,col = getCell(app,app.x,app.y)
    showPossibleMoves(app,col,row)

def mouseReleased(app,event):
    app.xx,app.yy = event.x,event.y
    selectPiece(app)
    pieceCaptured(app,app.x,app.y,app.xx,app.yy)
    movePiece(app)
    
def movePiece(app):
    #moves the pieces
    row,col = getCell(app,app.xx,app.yy)
    olerow,olecol = getCell(app,app.x,app.y)
    elementsOfPiece = getPieceFromCell(app,olerow,olecol)
    if elementsOfPiece in app.blackPawnCoords:
        if not app.isWhiteTurn:
            for pawn in range(len(app.blackPawnCoords)):
                if app.blackPawnCoords[pawn] == elementsOfPiece:
                    if moveIsLegal(app,elementsOfPiece,row,col):
                        app.blackPawnCoords[pawn].pop(0)
                        app.blackPawnCoords[pawn].pop(0)
                        app.blackPawnCoords[pawn].insert(0,row)
                        app.blackPawnCoords[pawn].insert(1,col)
    elif elementsOfPiece in app.whitePawnCoords:
        if app.isWhiteTurn:
            for pawn in range(len(app.whitePawnCoords)):
                if app.whitePawnCoords[pawn] == elementsOfPiece:
                    if moveIsLegal(app,elementsOfPiece,row,col):
                        app.whitePawnCoords[pawn].pop(0)
                        app.whitePawnCoords[pawn].pop(0)
                        app.whitePawnCoords[pawn].insert(0,row)
                        app.whitePawnCoords[pawn].insert(1,col)
    else:
        if not app.isWhiteTurn:
            if app.blackKingCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.blackKingCoords.pop(0)
                    app.blackKingCoords.pop(0)
                    app.blackKingCoords.insert(0,row)
                    app.blackKingCoords.insert(1,col)
            elif app.lBlackKnightCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.lBlackKnightCoords.pop(0)
                    app.lBlackKnightCoords.pop(0)
                    app.lBlackKnightCoords.insert(0,row)
                    app.lBlackKnightCoords.insert(1,col)
            elif app.blackQueenCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.blackQueenCoords.pop(0)
                    app.blackQueenCoords.pop(0)
                    app.blackQueenCoords.insert(0,row)
                    app.blackQueenCoords.insert(1,col)
            elif app.rBlackKnightCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.rBlackKnightCoords.pop(0)
                    app.rBlackKnightCoords.pop(0)
                    app.rBlackKnightCoords.insert(0,row)
                    app.rBlackKnightCoords.insert(1,col)
            elif app.rBlackBishopCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.rBlackBishopCoords.pop(0)
                    app.rBlackBishopCoords.pop(0)
                    app.rBlackBishopCoords.insert(0,row)
                    app.rBlackBishopCoords.insert(1,col)
            elif app.lBlackBishopCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.lBlackBishopCoords.pop(0)
                    app.lBlackBishopCoords.pop(0)
                    app.lBlackBishopCoords.insert(0,row)
                    app.lBlackBishopCoords.insert(1,col)
            elif app.rBlackRookCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.rBlackRookCoords.pop(0)
                    app.rBlackRookCoords.pop(0)
                    app.rBlackRookCoords.insert(0,row)
                    app.rBlackRookCoords.insert(1,col)
            elif app.lBlackRookCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.lBlackRookCoords.pop(0)
                    app.lBlackRookCoords.pop(0)
                    app.lBlackRookCoords.insert(0,row)
                    app.lBlackRookCoords.insert(1,col)
        if app.isWhiteTurn:
            if app.whiteKingCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.whiteKingCoords.pop(0)
                    app.whiteKingCoords.pop(0)
                    app.whiteKingCoords.insert(0,row)
                    app.whiteKingCoords.insert(1,col)
            elif app.lWhiteKnightCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.lWhiteKnightCoords.pop(0)
                    app.lWhiteKnightCoords.pop(0)
                    app.lWhiteKnightCoords.insert(0,row)
                    app.lWhiteKnightCoords.insert(1,col)
            elif app.whiteQueenCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.whiteQueenCoords.pop(0)
                    app.whiteQueenCoords.pop(0)
                    app.whiteQueenCoords.insert(0,row)
                    app.whiteQueenCoords.insert(1,col)
            elif app.rWhiteKnightCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.rWhiteKnightCoords.pop(0)
                    app.rWhiteKnightCoords.pop(0)
                    app.rWhiteKnightCoords.insert(0,row)
                    app.rWhiteKnightCoords.insert(1,col)
            elif app.rWhiteBishopCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.rWhiteBishopCoords.pop(0)
                    app.rWhiteBishopCoords.pop(0)
                    app.rWhiteBishopCoords.insert(0,row)
                    app.rWhiteBishopCoords.insert(1,col)
            elif app.lWhiteBishopCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.lWhiteBishopCoords.pop(0)
                    app.lWhiteBishopCoords.pop(0)
                    app.lWhiteBishopCoords.insert(0,row)
                    app.lWhiteBishopCoords.insert(1,col)
            elif app.rWhiteRookCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.rWhiteRookCoords.pop(0)
                    app.rWhiteRookCoords.pop(0)
                    app.rWhiteRookCoords.insert(0,row)
                    app.rWhiteRookCoords.insert(1,col)
            elif app.lWhiteRookCoords == elementsOfPiece:
                if moveIsLegal(app,elementsOfPiece,row,col):
                    app.lWhiteRookCoords.pop(0)
                    app.lWhiteRookCoords.pop(0)
                    app.lWhiteRookCoords.insert(0,row)
                    app.lWhiteRookCoords.insert(1,col)
    if row != olerow or col != olecol:
        app.blueRowCol = []
    xrow,xcol = getCell(app,app.x,app.y)
    zrow,zcol = getCell(app,app.xx,app.yy)
    if getPieceFromCell(app,xrow,xcol) != getPieceFromCell(app,zrow,zcol) and\
         (app.currPiece in app.whitePieces or app.currPiece in app.whitePieces[8]):
        app.isWhiteTurn = False
        flipBoard(app)
    if getPieceFromCell(app,xrow,xcol) != getPieceFromCell(app,zrow,zcol) and\
         (app.currPiece in app.blackPieces or app.currPiece in app.blackPieces[8]):
        app.isWhiteTurn = True
        flipBoard(app)

def isInBoard(row,col):
    if -1<row<8 and -1<col<8:
        return True
    else: return False

def moveIsLegal(app,piece,row,col):
    app.currPiece = piece
    if piece in app.blackPawnCoords:
        for pawn in range(len(app.blackPawnCoords)):
            if app.blackPawnCoords[pawn] == piece:
                if (col - app.blackPawnCoords[pawn][1] == 1 or\
                    (app.blackPawnCoords[pawn][1] == 1 and col - app.blackPawnCoords[pawn][1] == 2) and isInBoard(row,col))and\
                    (row == piece[0]):
                    if ((getPieceFromCell(app,row,col) in app.whitePieces[8]) or\
                        (getPieceFromCell(app,row,col) in app.blackPieces[8])):
                        return False
                    else:
                        return True
    elif piece in app.whitePawnCoords:
        for pawn in range(len(app.whitePawnCoords)):
            if app.whitePawnCoords[pawn] == piece:
                if (col - app.whitePawnCoords[pawn][1] == -1 or\
                    (app.whitePawnCoords[pawn][1] == 6 and col - app.whitePawnCoords[pawn][1] == -2) and isInBoard(row,col)) and\
                    (row == app.whitePawnCoords[pawn][0]):
                    if (getPieceFromCell(app,row,col) in app.whitePieces[8]) or (getPieceFromCell(app,row,col) in app.blackPieces[8]):
                        return False
                    else:
                        return True
    elif app.blackKingCoords    == piece:
            for drow in [-1, 0, +1]:
                for dcol in [-1, 0, +1]:
                    if  isInBoard(row,col) and\
                        ((drow != 0) or (dcol != 0)) and\
                        (row - app.blackKingCoords[0] == drow and\
                        col - app.blackKingCoords[1] == dcol):
                        if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                            return False
                        else:
                            return True
    elif app.lBlackKnightCoords == piece:
        if isInBoard(row,col) and ((row-app.lBlackKnightCoords[0] == 2 and col-app.lBlackKnightCoords[1] == 1) or\
           (row-app.lBlackKnightCoords[0] == 1 and col-app.lBlackKnightCoords[1] == 2) or\
           (row-app.lBlackKnightCoords[0] == -2 and col-app.lBlackKnightCoords[1] == 1) or\
           (row-app.lBlackKnightCoords[0] == 2 and col-app.lBlackKnightCoords[1] == -1) or\
           (row-app.lBlackKnightCoords[0] == -2 and col-app.lBlackKnightCoords[1] == -1) or\
           (row-app.lBlackKnightCoords[0] == -1 and col-app.lBlackKnightCoords[1] == 2) or\
           (row-app.lBlackKnightCoords[0] == 1 and col-app.lBlackKnightCoords[1] == -2) or\
           (row-app.lBlackKnightCoords[0] == -1 and col-app.lBlackKnightCoords[1] == -2)):
            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
               return False
            else:
                return True
    elif app.blackQueenCoords   == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if abs(drow) == abs(dcol) and (app.blackQueenCoords[0] + drow*cols) == row and\
                             (app.blackQueenCoords[1] + dcol*cols) == col:
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
                        elif drow == 0 and (app.blackQueenCoords[0] == row) and ((app.blackQueenCoords[1] + dcol*cols) == col or\
                            (app.blackQueenCoords[1] - dcol*cols) == col):
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
                        elif dcol == 0 and ((app.blackQueenCoords[0] + drow*cols == row) or\
                             (app.blackQueenCoords[0] - drow*cols == row)) and (app.blackQueenCoords[1]) == col:
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
    elif app.rBlackKnightCoords == piece:
        if isInBoard(row,col) and ((row-app.rBlackKnightCoords[0] == 2 and col-app.rBlackKnightCoords[1] == 1) or\
           (row-app.rBlackKnightCoords[0] == 1 and col-app.rBlackKnightCoords[1] == 2) or\
           (row-app.rBlackKnightCoords[0] == -2 and col-app.rBlackKnightCoords[1] == 1) or\
           (row-app.rBlackKnightCoords[0] == 2 and col-app.rBlackKnightCoords[1] == -1) or\
           (row-app.rBlackKnightCoords[0] == -2 and col-app.rBlackKnightCoords[1] == -1) or\
           (row-app.rBlackKnightCoords[0] == -1 and col-app.rBlackKnightCoords[1] == 2) or\
           (row-app.rBlackKnightCoords[0] == 1 and col-app.rBlackKnightCoords[1] == -2) or\
           (row-app.rBlackKnightCoords[0] == -1 and col-app.rBlackKnightCoords[1] == -2)):
            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
               return False
            else:
                return True
    elif app.rBlackBishopCoords == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if abs(drow) == abs(dcol) and (app.rBlackBishopCoords[0] + drow*cols) == row and\
                             (app.rBlackBishopCoords[1] + dcol*cols) == col:
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
    elif app.lBlackBishopCoords == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if abs(drow) == abs(dcol) and (app.lBlackBishopCoords[0] + drow*cols) == row and\
                             (app.lBlackBishopCoords[1] + dcol*cols) == col:
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
    elif app.rBlackRookCoords   == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if drow == 0 and (app.rBlackRookCoords[0] == row) and ((app.rBlackRookCoords[1] + dcol*cols) == col or\
                            (app.rBlackRookCoords[1] - dcol*cols) == col):
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
                        elif dcol == 0 and ((app.rBlackRookCoords[0] + drow*cols == row) or\
                             (app.rBlackRookCoords[0] - drow*cols == row)) and (app.rBlackRookCoords[1]) == col:
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
    elif app.lBlackRookCoords   == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if drow == 0 and (app.lBlackRookCoords[0] == row) and ((app.lBlackRookCoords[1] + dcol*cols) == col or\
                            (app.lBlackRookCoords[1] - dcol*cols) == col):
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
                        elif dcol == 0 and ((app.lBlackRookCoords[0] + drow*cols == row) or\
                             (app.lBlackRookCoords[0] - drow*cols == row)) and (app.lBlackRookCoords[1]) == col:
                            if getPieceFromCell(app,row,col) in app.blackPieces or getPieceFromCell(app,row,col) in app.blackPieces[8]:
                                return False
                            else:
                                return True
    elif app.whiteKingCoords    == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)) and\
                    (row - app.whiteKingCoords[0] == drow and\
                    col - app.whiteKingCoords[1] == dcol):
                    if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                        return False
                    else:
                        return True
    elif app.lWhiteKnightCoords == piece:
        if isInBoard(row,col) and ((row-app.lWhiteKnightCoords[0] == 2 and col-app.lWhiteKnightCoords[1] == 1) or\
           (row-app.lWhiteKnightCoords[0] == 1 and col-app.lWhiteKnightCoords[1] == 2) or\
           (row-app.lWhiteKnightCoords[0] == -2 and col-app.lWhiteKnightCoords[1] == 1) or\
           (row-app.lWhiteKnightCoords[0] == 2 and col-app.lWhiteKnightCoords[1] == -1) or\
           (row-app.lWhiteKnightCoords[0] == -2 and col-app.lWhiteKnightCoords[1] == -1) or\
           (row-app.lWhiteKnightCoords[0] == -1 and col-app.lWhiteKnightCoords[1] == 2) or\
           (row-app.lWhiteKnightCoords[0] == 1 and col-app.lWhiteKnightCoords[1] == -2) or\
           (row-app.lWhiteKnightCoords[0] == -1 and col-app.lWhiteKnightCoords[1] == -2)):
            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
               return False
            else:
                return True
    elif app.whiteQueenCoords   == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if abs(drow) == abs(dcol) and (app.whiteQueenCoords[0] + drow*cols) == row and\
                             (app.whiteQueenCoords[1] + dcol*cols) == col:
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
                        elif drow == 0 and (app.whiteQueenCoords[0] == row) and ((app.whiteQueenCoords[1] + dcol*cols) == col or\
                            (app.whiteQueenCoords[1] - dcol*cols) == col):
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
                        elif dcol == 0 and ((app.whiteQueenCoords[0] + drow*cols == row) or\
                             (app.whiteQueenCoords[0] - drow*cols == row)) and (app.whiteQueenCoords[1]) == col:
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
    elif app.rWhiteKnightCoords == piece:
        if isInBoard(row,col) and ((row-app.rWhiteKnightCoords[0] == 2 and col-app.rWhiteKnightCoords[1] == 1) or\
           (row-app.rWhiteKnightCoords[0] == 1 and col-app.rWhiteKnightCoords[1] == 2) or\
           (row-app.rWhiteKnightCoords[0] == -2 and col-app.rWhiteKnightCoords[1] == 1) or\
           (row-app.rWhiteKnightCoords[0] == 2 and col-app.rWhiteKnightCoords[1] == -1) or\
           (row-app.rWhiteKnightCoords[0] == -2 and col-app.rWhiteKnightCoords[1] == -1) or\
           (row-app.rWhiteKnightCoords[0] == -1 and col-app.rWhiteKnightCoords[1] == 2) or\
           (row-app.rWhiteKnightCoords[0] == 1 and col-app.rWhiteKnightCoords[1] == -2) or\
           (row-app.rWhiteKnightCoords[0] == -1 and col-app.rWhiteKnightCoords[1] == -2)):
            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                return False
            else:
                return True
    elif app.rWhiteBishopCoords == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if abs(drow) == abs(dcol) and (app.rWhiteBishopCoords[0] + drow*cols) == row and\
                             (app.rWhiteBishopCoords[1] + dcol*cols) == col:
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
    elif app.lWhiteBishopCoords == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if abs(drow) == abs(dcol) and (app.lWhiteBishopCoords[0] + drow*cols) == row and\
                             (app.lWhiteBishopCoords[1] + dcol*cols) == col:
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
    elif app.rWhiteRookCoords   == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if drow == 0 and (app.rWhiteRookCoords[0] == row) and ((app.rWhiteRookCoords[1] + dcol*cols) == col or\
                            (app.rWhiteRookCoords[1] - dcol*cols) == col):
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
                        elif dcol == 0 and ((app.rWhiteRookCoords[0] + drow*cols == row) or\
                             (app.rWhiteRookCoords[0] - drow*cols == row)) and (app.rWhiteRookCoords[1]) == col:
                            if getPieceFromCell(app,row,col) in getPieceFromCell(app,row,col) or getPieceFromCell(app,row,col) in app.whitePieces:
                                return False
                            else:
                                return True
    elif app.lWhiteRookCoords   == piece:
        for drow in [-1, 0, +1]:
            for dcol in [-1, 0, +1]:
                if  isInBoard(row,col) and\
                    ((drow != 0) or (dcol != 0)):
                    for cols in range(app.cols):
                        if drow == 0 and (app.lWhiteRookCoords[0] == row) and ((app.lWhiteRookCoords[1] + dcol*cols) == col or\
                            (app.lWhiteRookCoords[1] - dcol*cols) == col):
                            if getPieceFromCell(app,row,col) in app.whitePieces or getPieceFromCell(app,row,col) in app.whitePieces[8]:
                                return False
                            else:
                                return True
                        elif dcol == 0 and ((app.lWhiteRookCoords[0] + drow*cols == row) or\
                             (app.lWhiteRookCoords[0] - drow*cols == row)) and (app.lWhiteRookCoords[1]) == col:
                            if getPieceFromCell(app,row,col) in app.whitePieces:
                                return False
                            else:
                                return True
    return False
    
def selectPiece(app):
    if getCell(app,app.x,app.y) == getCell(app,app.xx,app.yy):
        row,col = getCell(app,app.x,app.y)
        if getPieceFromCell(app,row,col) != 0:
            return True

def pieceCaptured(app,x,y,xx,yy):
    oleRow,oleCol = getCell(app,x,y)
    newRow,newCol = getCell(app,xx,yy)
    oldPiece = getPieceFromCell(app,oleRow,oleCol)
    newPiece = getPieceFromCell(app,newRow,newCol)
    if moveIsLegal(app,oldPiece,newRow,newCol):
        if not selectPiece(app):
            if (oldPiece in app.blackPieces or oldPiece in app.blackPieces[8]) and\
                (newPiece in app.whitePieces or newPiece in app.whitePieces[8]):
                for piece in range(len(app.whitePieces)):
                    for pawn in range(len(app.whitePieces[8])):
                        if newPiece == app.whitePieces[piece]:
                            app.whitePieces[piece][0] = app.whitePlace
                            app.whitePieces[piece][1] = -1
                            app.whitePlace += 1/15
                        elif newPiece == app.whitePieces[8][pawn]:
                            app.whitePieces[8][pawn][0] = app.whitePlace
                            app.whitePieces[8][pawn][1] = -1
                            app.whitePlace += 1/15
            elif oldPiece in app.whitePieces or oldPiece in app.whitePieces[8] and\
                (newPiece in app.blackPieces or newPiece in app.blackPieces[8]):
                for piece in range(len(app.blackPieces)):
                    for pawn in range(len(app.blackPieces[8])):
                        if newPiece == app.blackPieces[piece]:
                            app.blackPieces[piece][0] = app.blackPlace
                            app.blackPieces[piece][1] = 8
                            app.blackPlace += 1/15
                        elif newPiece == app.blackPieces[8][pawn]:
                            app.blackPieces[8][pawn][0] = app.blackPlace
                            app.blackPieces[8][pawn][1] = 8
                            app.blackPlace += 1/15

def flipBoard(app):
    for piece in range(len(app.pieces)):
        if app.pieces[piece] == app.blackPawnCoords:
            for pawn in range(len(app.blackPawnCoords)):
                drow = 4 - app.blackPawnCoords[pawn][0]
                dcol = 4 - app.blackPawnCoords[pawn][1]
                ddrow = 3 - app.blackPawnCoords[pawn][0]
                ddcol = 3 - app.blackPawnCoords[pawn][1]
                app.blackPawnCoords[pawn][0] += drow + ddrow
                app.blackPawnCoords[pawn][1] += dcol + ddcol
        elif app.pieces[piece] == app.whitePawnCoords:
            for pawn in range(len(app.whitePawnCoords)):
                drow = 4 - app.whitePawnCoords[pawn][0]
                dcol = 4 - app.whitePawnCoords[pawn][1]
                ddrow = 3 - app.whitePawnCoords[pawn][0]
                ddcol = 3 - app.whitePawnCoords[pawn][1]
                app.whitePawnCoords[pawn][0] += drow + ddrow
                app.whitePawnCoords[pawn][1] += dcol + ddcol
        else:
            drow = 4 - app.pieces[piece][0]
            dcol = 4 - app.pieces[piece][1]
            ddrow = 3 - app.pieces[piece][0]
            ddcol = 3 - app.pieces[piece][1]
            app.pieces[piece][0] += drow + ddrow
            app.pieces[piece][1] += dcol + ddcol
    app.boardFlip = not app.boardFlip

def showPossibleMoves(app,row,col):
    app.blueRowCol = [(row,col)]
    piece = getPieceFromCell(app,row,col)
    if selectPiece(app):
        for row in range(-app.rows,app.rows):
                for col in range(-app.cols,app.cols):
                    if moveIsLegal(app,app.currPiece,row,col):
                        app.blueRowCol.append((col,row))

    else:
        app.blueRowCol = []

def getPieceFromCell(app,row,col):
    #returns the list that represents the piece and its coordinates
    thePiece = 0
    try:
        for piece in range(len(app.pieces)):
            if app.pieces[piece] == app.whitePawnCoords:
                for wapiece in range(len(app.whitePawnCoords)):
                    if app.whitePawnCoords[wapiece][0] == row and app.whitePawnCoords[wapiece][1] == col:
                        thePiece = app.whitePawnCoords[wapiece]
            elif app.pieces[piece] == app.blackPawnCoords:
                for bapiece in range(len(app.blackPawnCoords)):
                    if app.blackPawnCoords[bapiece][0] == row and app.blackPawnCoords[bapiece][1] == col:
                        thePiece = app.blackPawnCoords[bapiece]
            elif  app.pieces[piece][0] == row and app.pieces[piece][1] == col:
                thePiece = app.pieces[piece]
        return thePiece
    except:
        pass

def getCell(app,x,y):
    row = int(((x-app.margin)/(app.width - 2*app.margin)*app.cols))
    col = int(((y-app.margin)/(app.height - 2*app.margin)*app.rows))
    return row,col

def getPieceCoords(app,piece):
    # gets Piece coordinates of non-pawn Pieces
    x = app.margin + piece[0]*app.cellSize + app.cellSize/2
    y = app.margin + piece[1]*app.cellSize + app.cellSize/2
    return x,y

def getPawnCoords(app,piece,pawn):
    # Gets pawn coordinates
    x = app.margin + piece[pawn][0]*app.cellSize + app.cellSize/2
    y = app.margin + piece[pawn][1]*app.cellSize + app.cellSize/2
    return x,y

def drawPieces(app,canvas):
    # initializes all the pieces on the board
    for piece in app.pieces:
        if piece == app.blackPawnCoords:
            for blackpawn in range(len(app.blackPawnCoords)):
                x,y = getPawnCoords(app,app.blackPawnCoords,blackpawn)
                canvas.create_text(x,y,text = piece[blackpawn][2],font = 'Arial 50 bold')
        elif piece == app.whitePawnCoords:
            for whitepawn in range(len(app.whitePawnCoords)):
                x,y = getPawnCoords(app,app.whitePawnCoords,whitepawn)
                canvas.create_text(x,y,text = piece[whitepawn][2],font = 'Arial 50 bold')
        else:
            x,y = getPieceCoords(app,piece)
            canvas.create_text(x,y,text = piece[2],font = 'Arial 50 bold')

def getCellBounds(app,row,col):
    # gets cell bounds
    x0 = app.margin + app.cellSize*col
    y0 = app.margin + app.cellSize*row
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    return x0,y0,x1,y1

def drawBoard(app,canvas):
    # creates the board
    for row in range(app.rows):
        for col in range(app.cols):
            if selectPiece(app) and (row,col) in app.blueRowCol and\
                (getPieceFromCell(app,col,row) in app.whitePieces or\
                getPieceFromCell(app,col,row) == 0 or\
                getPieceFromCell(app,col,row) in app.whitePieces[8]):
                x0,y0,x1,y1 = getCellBounds(app,row,col)
                canvas.create_rectangle(x0,y0,x1,y1, fill = app.cellColor[2])
            elif selectPiece(app) and (row,col) in app.blueRowCol and\
                (getPieceFromCell(app,col,row) in app.blackPieces or\
                getPieceFromCell(app,col,row) == 0 or\
                getPieceFromCell(app,col,row) in app.blackPieces[8]):
                x0,y0,x1,y1 = getCellBounds(app,row,col)
                canvas.create_rectangle(x0,y0,x1,y1, fill = app.cellColor[2])
            else:
                if not app.boardFlip:
                    x0,y0,x1,y1 = getCellBounds(app,row,col)
                    canvas.create_rectangle(x0,y0,x1,y1, fill = app.cellColor[(row+col)%2])
                elif app.boardFlip:
                    x0,y0,x1,y1 = getCellBounds(app,row,col)
                    canvas.create_rectangle(x0,y0,x1,y1, fill = app.cellColor[(row+col+1)%2])                    

def redrawAll(app,canvas):
    drawBoard(app,canvas)
    drawPieces(app,canvas)

def playChess():
    rows,cols,cellSize,margin,width,height = gameDimensions()
    runApp(width=width, height=height)

def main():
    playChess()

if __name__ == '__main__':
    main()