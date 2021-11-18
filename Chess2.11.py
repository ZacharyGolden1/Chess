# Step1:  make the board                     -- Done
# Step2:  make the pieces                    -- Done
# Step3:  create movement                    -- Done
# Step4:  check general legality of movement -- Done
# Step5:  color possible board moves         -- Done
# Step6:  create piece capturing             -- Done <-- make better UI for final product
# Step7:  create castling                    -- ...
# Step8:  detect checks and checkmates       -- ...
# Step9:  create A.I. to play against        -- ...
# Step10: Allow for pawn promotion           -- ...
########### Minimum needed for MVP ################
# Step11: create turns                       -- ...
# Step12: flip the board                     -- ...
# Step13: implement gameover/restart         -- ...
# Step14: title screen other UI stuff        -- ...
# Step15: immplement different gamemodes
#         and a gameclock                    -- ...

###################################################
################### VERSIONS ######################
###################################################
# Chess 1.0:
#### in this version I made the basics of the game 
#### just using lists
# Chess 2.0
#### in this version i remade the basics of the 
#### game using dictionaries and sets this made
#### the game faster and also helper clean up 
#### the code. I also got the game to further be 
#### like a real chess game and addressed major
#### bugs and issues from 1.0
# Chess 2.0.1
#### I have a major bug right now that has to do 
#### with what squares are legal for a piece to 
#### move to that I hope to address here
# Chess 2.0.2
#### Fixed some of the bugs mentioned above but
#### I still have this annoying bunnyhop problem
#### where pieces don't obey their legal blue
#### square placement and instead jump outside
#### this set boundary.
# Chess 2.0.3
#### Adding in some changes for getPieceFromCell
#### in order to deal with piece capturing
# Chess 2.0.4
#### Added in a terminal board just to help with
#### formatting when I eventually write my legal
#### move functions. Also implemented findLegal
#### Move. And I will implement castling and en
#### passant restrictions as well.
# Chess 2.10
#### Still need to fix castling and add en passant
#### implemented function that randomly moves
#### blacks pieces
# Chess 2.11
#### Progress save and some bug fixes

#################### Notes ######################
# I wrote app.pieceLegalMoves as a list instead of
# a dictionary, dictionary would be more efficient 
# and clearer. Figure out how to manipulate 
# dictionaries to make this work.


from cmu_112_graphics import *
import copy,random

################# Board and Rules ################
def appStarted(app):
    #initializing board size
    app.rows,app.cols,app.cellSize,app.margin,app.width,app.height,app.pieceSize = gameDimensions()

    # checks for board flippage:
    app.boardFlip = False

    # Passed piece toggle check
    app.passedPiece = False

    # Creates the color of the cell
    app.cellColor = ['white','lightgray','cyan']
    app.blueRowCol = []

    # List of legal moves:
    app.legalMoves = []

    # Mouse press Coordinate vars
    app.x = app.y = 1000

    # Mouse released Coordinate vars
    app.xx = app.yy = 10000

    # Mouse Dragged Coordinate vars 
    # (to see live pieces moving)
    app.xxx = app.yyy = 100000

    # placement of captured pieces:
    app.whitePlace = -1
    app.blackPlace = -1

    # Toggle for who's turn it is:
    app.isWhiteTurn = True
    app.isBlackTurn = False

    # Castling rights for kings 
    app.canBKingCastle = True
    app.canWKingCastle = True
    app.canlBRookCastle = True
    app.canrBRookCastle = True
    app.canlWRookCastle = True
    app.canrWRookCastle = True

    # En Passant
    app.enPassant = False

    # Checks to see if pawns have been promoted or not
    app.aBPawnHasBeenPromoted = False
    app.bBPawnHasBeenPromoted = False
    app.cBPawnHasBeenPromoted = False
    app.dBPawnHasBeenPromoted = False
    app.eBPawnHasBeenPromoted = False
    app.fBPawnHasBeenPromoted = False
    app.gBPawnHasBeenPromoted = False
    app.hBPawnHasBeenPromoted = False
    app.aWPawnHasBeenPromoted = False
    app.bWPawnHasBeenPromoted = False
    app.cWPawnHasBeenPromoted = False
    app.dWPawnHasBeenPromoted = False
    app.eWPawnHasBeenPromoted = False
    app.fWPawnHasBeenPromoted = False
    app.gWPawnHasBeenPromoted = False
    app.hWPawnHasBeenPromoted = False

    # piece position to start (row,col,unicode character) 
    # White then Black
    # All Pieces:
    app.pieces = {'wKing':[7,4,'\u2654',app.canWKingCastle],'wQueen':[7,3,'\u2655'],'lWKnight':[7,1,'\u2658'],
                  'rWKnight':[7,6,'\u2658'],'lWRook':[7,0,'\u2656',app.canlWRookCastle],
                  'rWRook':[7,7,'\u2656',app.canrWRookCastle],
                  'lWBishop':[7,2,'\u2657'],'rWBishop':[7,5,'\u2657'],
                  'aWPawn':[6,0,'\u2659',app.enPassant,app.aWPawnHasBeenPromoted],
                  'bWPawn':[6,1,'\u2659',app.enPassant,app.bWPawnHasBeenPromoted],
                  'cWPawn':[6,2,'\u2659',app.enPassant,app.cWPawnHasBeenPromoted],
                  'dWPawn':[6,3,'\u2659',app.enPassant,app.dWPawnHasBeenPromoted],
                  'eWPawn':[6,4,'\u2659',app.enPassant,app.eWPawnHasBeenPromoted],
                  'fWPawn':[6,5,'\u2659',app.enPassant,app.fWPawnHasBeenPromoted],
                  'gWPawn':[6,6,'\u2659',app.enPassant,app.gWPawnHasBeenPromoted],
                  'hWPawn':[6,7,'\u2659',app.enPassant,app.hWPawnHasBeenPromoted],

                  'bKing':[0,4,'\u265A',app.canBKingCastle],'bQueen':[0,3,'\u265B'],'lBKnight':[0,1,'\u265E'],
                  'rBKnight':[0,6,'\u265E'],'lBRook':[0,0,'\u265C',app.canlBRookCastle],
                  'rBRook':[0,7,'\u265C',app.canrBRookCastle],
                  'lBBishop':[0,2,'\u265D'],'rBBishop':[0,5,'\u265D'],
                  'aBPawn':[1,0,'\u265F',app.enPassant,app.aBPawnHasBeenPromoted],
                  'bBPawn':[1,1,'\u265F',app.enPassant,app.bBPawnHasBeenPromoted],
                  'cBPawn':[1,2,'\u265F',app.enPassant,app.cBPawnHasBeenPromoted],
                  'dBPawn':[1,3,'\u265F',app.enPassant,app.dBPawnHasBeenPromoted],
                  'eBPawn':[1,4,'\u265F',app.enPassant,app.eBPawnHasBeenPromoted],
                  'fBPawn':[1,5,'\u265F',app.enPassant,app.fBPawnHasBeenPromoted],
                  'gBPawn':[1,6,'\u265F',app.enPassant,app.gBPawnHasBeenPromoted],
                  'hBPawn':[1,7,'\u265F',app.enPassant,app.hBPawnHasBeenPromoted]}

    # Legal Moves of pieces
    app.allLegalPieceMoves = []

    # Black Pieces
    app.blackPieces = ['bKing','bQueen','rBKnight','lBKnight',
                       'rBBishop','lBBishop','rBRook','lBRook',
                       'aBPawn','bBPawn','cBPawn','dBPawn',
                       'eBPawn','fBPawn','gBPawn','hBPawn']

    # White Pieces
    app.whitePieces = ['wKing','wQueen','rWKnight','lWKnight',
                       'rWBishop','lWBishop','rWRook','lWRook',
                       'aWPawn','bWPawn','cWPawn','dWPawn',
                       'eWPawn','fWPawn','gWPawn','hWPawn']  

    # All Pieces
    app.pieceNames = [ 'bKing','bQueen','lBKnight','rBKnight',
                       'lBRook','rBRook','lBBishop','rBBishop',
                       'aBPawn','bBPawn','cBPawn','dBPawn',
                       'eBPawn','fBPawn','gBPawn','hBPawn',
                       'wKing','wQueen','lWKnight','rWKnight',
                       'lWRook','rWRook','lWBishop','rWBishop',
                       'aWPawn','bWPawn','cWPawn','dWPawn',
                       'eWPawn','fWPawn','gWPawn','hWPawn'
                       ]

    # Piece row and col of encountered pieces on the board
    app.possibleCapturePieceRow = 100
    app.possibleCapturePieceCol = 100

    # Keep a list of all the pieces that are in a row/col/diag 
    # after an encountered piece
    app.afterPieceRowColDiag = []

    # current piece
    app.currPiece = 0

    # captured black and white piece positions:
    app.capBlackrow = 8
    app.capBlackcol = 0
    app.capWhiterow = -1
    app.capWhitecol = 7

    # Gamemodes 
    app.randomMode = False

def gameDimensions():
    width = height = 700
    rows = cols = 8
    margin = 70
    pieceSize = cellSize = (width - 2*margin)/8
    return (rows,cols,cellSize,margin,width,height,pieceSize)

def keyPressed(app,event):
    if event.key == 'r':
        appStarted(app)

def mousePressed(app,event):
    app.x,app.y = event.x,event.y
    row,col = getCell(app,app.y,app.x)
    showPossibleMoves(app,row,col)

def mouseReleased(app,event):
    app.xx,app.yy = event.x,event.y
    pieceCaptured(app,app.x,app.y,app.xx,app.yy)
    selectPiece(app)
    movePiece(app)
    legalPieceMoves(app)
    if app.randomMode:
        moveBlackPieceRandomly(app)
    app.allLegalPieceMoves = []

def mouseDragged(app,event):
    pass

def timerFired(app):
    pass

def isInBoard(row,col):
    if -1<row<8 and -1<col<8:
        return True
    else: return False

def movePiece(app):
    # moves the pieces
    kings = ['wKing','bKing']
    pawns = ['aWPawn','bWPawn','cWPawn','dWPawn',
             'eWPawn','fWPawn','gWPawn','hWPawn',
             'aBPawn','bBPawn','cBPawn','dBPawn',
             'eBPawn','fBPawn','gBPawn','hBPawn']
    newrow,newcol = getCell(app,app.yy,app.xx)
    olerow,olecol = getCell(app,app.y,app.x)
    elementsOfPiece = 0
    if getPieceFromCell(app,olerow,olecol) != 0:
        elementsOfPiece = app.pieces[getPieceFromCell(app,olerow,olecol)]

    for piece in app.pieces:
        if app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol):
            app.pieces[piece][0] = newrow
            app.pieces[piece][1] = newcol
            if piece in pawns and piece in app.whitePieces and newrow == 0:
                app.pieces[piece][4] = True
            if piece in pawns and piece in app.blackPieces and newrow == 7:
                app.pieces[piece][4] = True
            if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                app.isBlackTurn = True
            if not moveIsLegal(app,piece,newrow,newcol,olerow,olecol) or\
                 passedPiece(app,newrow,newcol,olerow,olecol):
                app.pieces[piece][0] = olerow
                app.pieces[piece][1] = olecol
        # Castling
        if piece in kings and newcol-olecol == 2 and\
             app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol):
             castleKingSideWhite(app)
             if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                app.isBlackTurn = True
             if not moveIsLegal(app,piece,newrow,newcol,olerow,olecol) or\
                 passedPiece(app,newrow,newcol,olerow,olecol):
                app.pieces[piece][0] = olerow
                app.pieces[piece][1] = olecol
                app.pieces['rWRook'][1] = 7
        if piece in kings and newcol-olecol == -2 and\
             app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol):
             castleQueenSideWhite(app)
             if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                app.isBlackTurn = True
             if not moveIsLegal(app,piece,newrow,newcol,olerow,olecol) or\
                 passedPiece(app,newrow,newcol,olerow,olecol):
                app.pieces[piece][0] = olerow
                app.pieces[piece][1] = olecol
                app.pieces['lWRook'][1] = 0

    # Pawn Promotion
    for piece in app.pieces:
        if app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol) and piece in pawns:
            if elementsOfPiece[4] and getPieceFromCell(app,olerow,olecol) != 0 and\
                 newrow == 0 and app.pieces[piece][0] == newrow and piece in app.whitePieces:
                app.pieces[getPieceFromCell(app,olerow,olecol)][2] = '\u2655' 
            if elementsOfPiece[4] and getPieceFromCell(app,olerow,olecol) != 0 and\
                 app.pieces[piece][0] == 7 and piece in app.blackPieces:
                app.pieces[getPieceFromCell(app,olerow,olecol)][2] = '\u265B'

def passedPiece(app,newrow,newcol,olerow,olecol):
    for piece in app.pieces:
        # rows and columns
        if app.pieces[piece][0] > newrow and app.pieces[piece][1] == newcol and\
            app.pieces[piece][0] < olerow and newcol == olecol:
            return True
        if app.pieces[piece][0] < newrow and app.pieces[piece][1] == newcol and\
            app.pieces[piece][0] > olerow and newcol == olecol:
            return True
        if app.pieces[piece][1] < newcol and app.pieces[piece][0] == newrow and\
            app.pieces[piece][1] > olecol and newrow == olerow:
            return True
        if app.pieces[piece][1] > newcol and app.pieces[piece][0] == newrow and\
            app.pieces[piece][1] < olecol and newrow == olerow:
            return True
        # diagonals
        # Right Down
        if abs(newrow - app.pieces[piece][0]) == abs(newcol - app.pieces[piece][1]) and\
             abs(olerow - app.pieces[piece][0]) == abs(olecol - app.pieces[piece][1]) and\
             olecol < app.pieces[piece][1] and olerow > app.pieces[piece][0] and\
             newcol > app.pieces[piece][1] and newrow < app.pieces[piece][0]:
             return True
        # Right Up
        if newrow - app.pieces[piece][0] == newcol - app.pieces[piece][1] and\
             olerow - app.pieces[piece][0] == olecol - app.pieces[piece][1] and\
             olecol < app.pieces[piece][1] and olerow < app.pieces[piece][0] and\
             newcol > app.pieces[piece][1] and newrow > app.pieces[piece][0]:
             return True
        # Left Down
        if newrow - app.pieces[piece][0] == newcol - app.pieces[piece][1] and\
             olerow - app.pieces[piece][0] == olecol - app.pieces[piece][1] and\
             olecol > app.pieces[piece][1] and olerow > app.pieces[piece][0] and\
             newcol < app.pieces[piece][1] and newrow < app.pieces[piece][0]:
             return True
        # Left Up
        if abs(newrow - app.pieces[piece][0]) == abs(newcol - app.pieces[piece][1]) and\
             abs(olerow - app.pieces[piece][0]) == abs(olecol - app.pieces[piece][1]) and\
             olecol > app.pieces[piece][1] and olerow < app.pieces[piece][0] and\
             newcol < app.pieces[piece][1] and newrow > app.pieces[piece][0]:
             return True

def moveIsLegal(app,piece,newrow,newcol,olerow,olecol):
    kings = ['wKing','bKing']
    queens = ['wQueen','bQueen']
    knights = ['rWKnight','lWKnight','rBKnight','lBKnight']
    bishops = ['rWBishop','lWBishop','rBBishop','lBBishop']
    rooks = ['rWRook','lWRook','rBRook','lBRook']
    pawns = ['aWPawn','bWPawn','cWPawn','dWPawn',
             'eWPawn','fWPawn','gWPawn','hWPawn',
             'aBPawn','bBPawn','cBPawn','dBPawn',
             'eBPawn','fBPawn','gBPawn','hBPawn']

    if isInBoard(newrow,newcol):
        if piece in app.blackPieces and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.blackPieces or\
            piece in app.whitePieces and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.whitePieces:
            if piece not in knights:
                if newrow > olerow and newcol == olecol:
                    for row in range(newrow,8):
                        app.afterPieceRowColDiag.append((row,olecol))
                if newrow < olerow and newcol == olecol:
                    for row in range(0,newrow+1):
                        app.afterPieceRowColDiag.append((row,olecol))
                
                # checks whether there are pieces ahead of the current piece in the same col
                if newcol > olecol and newrow == olerow:
                    for col in range(newcol,8):
                        app.afterPieceRowColDiag.append((olerow,col))
                if newcol < olecol and newrow == olerow:
                    for col in range(0,newcol+1):
                        app.afterPieceRowColDiag.append((olerow,col))

                # checks whether there are pieces ahead of the current piece in the same diagonal
                if newcol>olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol,8):
                        for row in range(newrow,8):
                            app.afterPieceRowColDiag.append((row,col))
                if newcol>olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol,8):
                        for row in range(0,newrow+1):
                            app.afterPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol+1):
                        for row in range(newrow,8):
                            app.afterPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol+1):
                        for row in range(0,newrow+1):
                            app.afterPieceRowColDiag.append((row,col))

        if piece in app.blackPieces and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.whitePieces or\
            piece in app.whitePieces and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.blackPieces:
            if piece not in knights:
                if newrow > olerow and newcol == olecol:
                    for row in range(newrow+1,8):
                        app.afterPieceRowColDiag.append((row,olecol))
                if newrow < olerow and newcol == olecol:
                    for row in range(0,newrow):
                        app.afterPieceRowColDiag.append((row,olecol))
                
                # checks whether there are pieces ahead of the current piece in the same col
                if newcol > olecol and newrow == olerow:
                    for col in range(newcol+1,8):
                        app.afterPieceRowColDiag.append((olerow,col))
                if newcol < olecol and newrow == olerow:
                    for col in range(0,newcol):
                        app.afterPieceRowColDiag.append((olerow,col))

                # checks whether there are pieces ahead of the current piece in the same diagonal
                if newcol>olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol+1,8):
                        for row in range(newrow+1,8):
                            app.afterPieceRowColDiag.append((row,col))
                if newcol>olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol+1,8):
                        for row in range(0,newrow):
                            app.afterPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol):
                        for row in range(newrow+1,8):
                            app.afterPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol):
                        for row in range(0,newrow):
                            app.afterPieceRowColDiag.append((row,col))

        if piece in app.blackPieces and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.blackPieces or\
            piece in app.whitePieces and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.whitePieces:
            return False

        if piece in kings and\
            ((abs(newcol - olecol) == 1 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 0 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 0) or\
            (abs(newcol - olecol) == 0 and abs(newrow - olerow) == 0)):
            return True
        if piece in kings and\
            (app.canWKingCastle and app.canlWRookCastle and getPieceFromCell(app,7,1) == 0 and\
            getPieceFromCell(app,7,2) == 0 and getPieceFromCell(app,7,3) == 0 and\
            newcol - olecol == -2 and newrow == olerow and piece == kings[0]):
            return True
        if piece in kings and\
            (app.canWKingCastle and app.canrWRookCastle and getPieceFromCell(app,7,5) == 0 and\
            getPieceFromCell(app,7,6) == 0 and newcol - olecol == 2 and\
            newrow == olerow and piece == kings[0]):
            return True
        elif piece in queens or (piece != 0 and (app.pieces[piece][2] == '\u265B' or app.pieces[piece][2] == '\u2655'))  and\
             ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow)) or\
            (newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            return True
        elif piece in knights and\
            ((abs(newcol - olecol) == 2 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 2)):
            return True
        elif piece in bishops and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow))):
            return True
        elif piece in rooks and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            return True
        elif piece in pawns and piece in app.blackPieces and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            (((newrow - olerow) == 1 and olecol - newcol == 0 and\
            getWhitePieceFromCell(app,newrow,newcol) not in app.whitePieces) or\
            (olerow == 1 and (newrow - olerow) == 2 and olecol - newcol == 0 and\
            getWhitePieceFromCell(app,newrow,newcol) not in app.whitePieces) or\
            (getPieceFromCell(app,newrow,newcol) != 0 and\
            getWhitePieceFromCell(app,newrow,newcol) in app.whitePieces and\
            (newrow - olerow) == 1 and abs(olecol - newcol) == 1)):
            return True
        elif piece in pawns and piece in app.whitePieces and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            (((newrow - olerow) == -1 and olecol - newcol == 0 and\
            getBlackPieceFromCell(app,newrow,newcol) not in app.blackPieces) or\
            (olerow == 6 and (newrow - olerow) == -2 and olecol - newcol == 0 and\
            getBlackPieceFromCell(app,newrow,newcol) not in app.blackPieces) or\
            (getPieceFromCell(app,newrow,newcol) != 0 and\
            getBlackPieceFromCell(app,newrow,newcol) in app.blackPieces and\
            (newrow - olerow) == -1 and abs(olecol - newcol) == 1)):
            return True

def pawnPromotion(app,piece):
    app.pieces[piece][4] = True
    if piece in app.whitePieces:
        app.pieces[piece][2] = '\u2655'
    elif piece in app.blackPieces:
        app.pieces[piece][2] = '\u265B'

def castleQueenSideWhite(app):
    app.pieces['wKing'][1] -= 2
    app.pieces['lWRook'][1] += 3
    app.canWKingCastle = False

def castleKingSideWhite(app):
    app.pieces['wKing'][1] += 2
    app.pieces['rWRook'][1] -= 2
    app.canWKingCastle = False

def selectPiece(app):
    if getCell(app,app.y,app.x) == getCell(app,app.yy,app.xx):
        row,col = getCell(app,app.y,app.x)
        if getPieceFromCell(app,row,col) != 0:
            return True

def automatedPieceCaptured(app,oleRow,oleCol,newRow,newCol):
    oldPiece = getPieceFromCell(app,oleRow,oleCol)
    newPiece = getPieceFromCell(app,newRow,newCol)
    if oldPiece in app.blackPieces and newPiece in app.whitePieces:
        app.pieces[newPiece][0] = app.capWhiterow
        app.pieces[newPiece][1] = app.capWhitecol
        app.pieces[oldPiece][0] = newRow
        app.pieces[oldPiece][1] = newCol
        app.capWhitecol -= 1
        if app.capWhitecol == 0:
            app.capWhitecol = 7
            app.capWhiterow = -2
    if oldPiece in app.whitePieces and newPiece in app.blackPieces:
        app.pieces[newPiece][0] = app.capBlackrow
        app.pieces[newPiece][1] = app.capBlackcol
        app.pieces[oldPiece][0] = newRow
        app.pieces[oldPiece][1] = newCol
        app.capBlackcol += 1
        if app.capBlackcol == 7:
            app.capBlackcol = 9
            app.capBlackrow = 0

def pieceCaptured(app,x,y,xx,yy):
    oleRow,oleCol = getCell(app,y,x)
    newRow,newCol = getCell(app,yy,xx)
    oldPiece = getPieceFromCell(app,oleRow,oleCol)
    newPiece = getPieceFromCell(app,newRow,newCol)
    if moveIsLegal(app,oldPiece,newRow,newCol,oleRow,oleCol):
        if not (selectPiece(app) or passedPiece(app, newRow, newCol, oleRow, oleCol)):
            if oldPiece in app.blackPieces and newPiece in app.whitePieces:
                app.pieces[newPiece][0] = app.capWhiterow
                app.pieces[newPiece][1] = app.capWhitecol
                app.pieces[oldPiece][0] = newRow
                app.pieces[oldPiece][1] = newCol
                app.capWhitecol -= 1
                if app.capWhitecol == 0:
                    app.capWhitecol = 7
                    app.capWhiterow = -2
            if oldPiece in app.whitePieces and newPiece in app.blackPieces:
                app.pieces[newPiece][0] = app.capBlackrow
                app.pieces[newPiece][1] = app.capBlackcol
                app.pieces[oldPiece][0] = newRow
                app.pieces[oldPiece][1] = newCol
                app.capBlackcol += 1
                if app.capBlackcol == 7:
                    app.capBlackcol = 9
                    app.capBlackrow = 0

"""def flipBoard(app):
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
            drow = 4 - app.pieces[piece][1]
            dcol = 4 - app.pieces[piece][0]
            ddrow = 3 - app.pieces[piece][1]
            ddcol = 3 - app.pieces[piece][0]
            app.pieces[piece][1] += drow + ddrow
            app.pieces[piece][0] += dcol + ddcol
    app.boardFlip = not app.boardFlip"""

def showPossibleMoves(app,pieceRow,pieceCol):
    app.blueRowCol = [(pieceRow,pieceCol)]
    piece = getPieceFromCell(app,pieceRow,pieceCol)
    if getPieceFromCell(app,pieceRow,pieceCol) != 0:
        olerow = app.pieces[getPieceFromCell(app,pieceRow,pieceCol)][0]
        olecol = app.pieces[getPieceFromCell(app,pieceRow,pieceCol)][1]
    if selectPiece(app):
        for row in range(-app.rows,app.rows):
                for col in range(-app.cols,app.cols):
                    if moveIsLegal(app,piece,row,col,olerow,olecol):
                        app.blueRowCol.append((row,col))
        app.blueRowCol = list(set(app.blueRowCol)-set(app.afterPieceRowColDiag))
        app.blueRowCol.append((pieceRow,pieceCol))
    else:
        app.blueRowCol = []
        app.afterPieceRowColDiag = []

def possibleMoves(app,pieceRow,pieceCol):
    piece = getPieceFromCell(app,pieceRow,pieceCol)
    if getPieceFromCell(app,pieceRow,pieceCol) != 0:
        olerow = app.pieces[getPieceFromCell(app,pieceRow,pieceCol)][0]
        olecol = app.pieces[getPieceFromCell(app,pieceRow,pieceCol)][1]
    for row in range(-app.rows,app.rows):
            for col in range(-app.cols,app.cols):
                if moveIsLegal(app,piece,row,col,olerow,olecol):
                    app.legalMoves.append((row,col))
    app.legalMoves = list(set(app.legalMoves)-set(app.afterPieceRowColDiag))
    app.allLegalPieceMoves.append([piece,app.legalMoves])
    app.legalMoves = []
    app.afterPieceRowColDiag = []

def legalPieceMoves(app):
    for row in range(app.rows):
        for col in range(app.cols):
            piece = getPieceFromCell(app,row,col)
            if piece == 0:
                app.allLegalPieceMoves.append([None,[row,col]])
            else:
                possibleMoves(app,row,col)

def getPieceFromCell(app,row,col):
    # returns the piece from the given position
    thePiece = 0
    for piece in app.pieces:
        if app.pieces[piece][0] == row and app.pieces[piece][1] == col:
            thePiece = piece
    return thePiece

def getBlackPieceFromCell(app,row,col):
   # returns the black piece from the given position
    thePiece = 0
    for piece in app.blackPieces:
        if app.pieces[piece][0] == row and app.pieces[piece][1] == col:
            thePiece = piece
    return thePiece

def getWhitePieceFromCell(app,row,col):
   # returns the black piece from the given position
    thePiece = 0
    for piece in app.whitePieces:
        if app.pieces[piece][0] == row and app.pieces[piece][1] == col:
            thePiece = piece
    return thePiece

def getCell(app,y,x):
    row = int(((y-app.margin)/(app.height - 2*app.margin)*app.rows))
    col = int(((x-app.margin)/(app.width - 2*app.margin)*app.cols))
    return row,col

def getPieceCoords(app,piece):
    # gets coordinates of Pieces
    x = app.margin + app.pieces[piece][1]*app.cellSize + app.cellSize/2
    y = app.margin + app.pieces[piece][0]*app.cellSize + app.cellSize/2
    return x,y

def drawPieces(app,canvas):
    # initializes all the pieces on the board
    for piece in app.pieces:
        x,y = getPieceCoords(app,piece)
        canvas.create_text(x,y,text = app.pieces[piece][2],font = f'Arial {int(app.pieceSize)} bold')

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
            if selectPiece(app) and (row,col) in app.blueRowCol:
                x1,y1,x2,y2 = getCellBounds(app,row,col)
                canvas.create_rectangle(x1,y1,x2,y2,fill = app.cellColor[2]) 
            elif selectPiece(app) and (row,col) not in app.blueRowCol:
                x1,y1,x2,y2 = getCellBounds(app,row,col)
                canvas.create_rectangle(x1,y1,x2,y2,fill = app.cellColor[(row+col)%2])                  
            elif not selectPiece(app):
                x1,y1,x2,y2 = getCellBounds(app,row,col)
                canvas.create_rectangle(x1,y1,x2,y2,fill = app.cellColor[(row+col)%2])      

def drawTerminalBoard(app):
    pieceLocations = []
    for piece in app.pieces:
        pieceLocations.append((app.pieces[piece][0],app.pieces[piece][1]))

    for row in range(app.rows):
        for col in range(app.cols):
            if (row,col) in pieceLocations:
                piecePositionInList = pieceLocations.index((row,col))
                piece = app.pieceNames[piecePositionInList]
                print(app.pieces[piece][2],end='  ')
            if (row,col) not in pieceLocations:
                print('.',end='  ')
            if col == 7:
                print(f'{row+1}\n')

    print('A  B  C  D  E  F  G  H')


############## A.I. Algorithm ###############
#*********** Completely Random *************#
def randomBlackPieceOnBoard(app):
    tempAllLegalPieceMoves = app.allLegalPieceMoves
    if not selectPiece(app):
        for piece in app.blackPieces:
            for pieceNCoords in app.allLegalPieceMoves:
                pieceIndex = app.allLegalPieceMoves.index(pieceNCoords)
                if piece == pieceNCoords[0] and len(pieceNCoords[1]) <= 1:
                    tempAllLegalPieceMoves.remove(pieceNCoords)
                if pieceNCoords[0] in app.whitePieces:
                    tempAllLegalPieceMoves.remove(pieceNCoords)
                if (app.pieces[piece][0],app.pieces[piece][1]) in pieceNCoords[1] and\
                    (app.pieces[piece][0],app.pieces[piece][1]) in app.allLegalPieceMoves[pieceIndex][1]:
                    app.allLegalPieceMoves[pieceIndex][1].remove((app.pieces[piece][0],app.pieces[piece][1]))
    piece = random.choice(tempAllLegalPieceMoves)
    return piece[0]
    
def randomBlackPieceOnBoardWithAvailableMoves(app):
    piece = randomBlackPieceOnBoard(app)
    for pieceNCoords in app.allLegalPieceMoves:
        if piece in pieceNCoords:
            return pieceNCoords

def chooseRandomMove(app,pieceNCoords):    
    move = random.choice(pieceNCoords[1])
    return  move

def moveBlackPieceRandomly(app):
    pieceNCoords = randomBlackPieceOnBoardWithAvailableMoves(app)
    if app.isBlackTurn and not selectPiece(app):
        newCoords = chooseRandomMove(app,pieceNCoords)
        pieceName = pieceNCoords.pop(0)
        pieceNCoords.insert(0,pieceName)
        oleRow = app.pieces[pieceName][0]
        oleCol = app.pieces[pieceName][1]
        newRow = newCoords[0]
        newCol = newCoords[1]
        automatedPieceCaptured(app,oleRow,oleCol,newRow,newCol)
        app.pieces[pieceName][0] = newCoords[0]
        app.pieces[pieceName][1] = newCoords[1]
        pieceNCoords
        app.isBlackTurn = False


############## Print 2d Lists ###############
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')


############### Draw Board ##################
def redrawAll(app,canvas):
    #drawTerminalBoard(app)
    drawBoard(app,canvas)
    drawPieces(app,canvas)

def playChess():
    rows,cols,cellSize,margin,width,height,pieceSize = gameDimensions()
    runApp(width=width, height=height)

def main():
    playChess()

if __name__ == '__main__':
    main()
