# Step1:  make the board                     -- Done
# Step2:  make the pieces                    -- Done
# Step3:  create movement                    -- Done
# Step4:  check general legality of movement -- Done
# Step5:  color possible board moves         -- Done
# Step6:  create piece capturing             -- Done <-- make better UI for final product
# Step7:  create castling/En Passant         -- Done
# Step8:  detect checks and checkmates       -- ...
# Step9:  create A.I. to play against        -- Done <-- Super slow optimize
# Step10: Allow for pawn promotion           -- Done <-- only promotes to queens however
# Step11: create turns                       -- Done
############ Minimum needed for MVP ################
# Step12: flip the board                     -- ...
# Step13: implement gameover/restart         -- Done
# Step14: title screen other UI stuff        -- Done
# Step15: immplement different gamemodes     -- Done

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
# Chess 2.12
#### Working on Pawn Promotion
#### Made a non-functional U.I.
# Chess 2.13
#### Working Castling
#### Working En Passant
# Chess 2.14
#### save for En Passant and Castling
# Chess 2.15
#### save for progress or lack thereof
#### if it ends up getting reverted later on
#### for the minimax backtracking algorithm
# Chess 2.16
#### save for minimax progress
###################################################
###################################################
################## Chess 3.0 ######################
###################################################
###################################################
#### Actual working AI that is super slow and 
#### super bad. Needs a lot of optimization
#### worked on the UI and toggles for gameModes.
#### Working fisher random gamemode.
# Chess 3.01
#### Checks and Checkmates sorta implemented
# Chess 3.02
#### save for a working game with kinna check stuff
# Chess 3.03
#### save for a working game with kinna check stuff
#### implemented weighted odds



from graphics import *
import copy,random

################# Board and Rules ################
def appStarted(app):
    #initializing board size
    app.rows,app.cols,app.cellSize,app.margin,app.width,app.height,app.pieceSize = gameDimensions()

    # StartGame Toggle:
    app.startGame = False
    app.started = True

    # GameModes:
    app.twoPlayerMode = False
    app.playerVsComputer = False
    app.easyMode = False
    app.mediumMode = False
    app.hardMode = False
    app.classicChess = False
    app.fisherRandomChess = False
    app.weightedOdds = False 

    # checks for board flippage:
    app.boardFlip = False

    # Toggle for gamesense security issues:
    app.canCheck = False

    # Board in a list for all the pieces:
    app.board = [([None]*app.cols) for i in range (app.rows)]

    # Passed piece toggle check
    app.passedPiece = False

    # Creates the color of the cell
    app.cellColor = ['white','lightgray','cyan']
    app.blueRowCol = []

    # List of legal moves:
    app.legalMoves = []

    # List of legal AI moves
    app.legalAIMoves = []

    # For miniMax algo:
    app.doableMoves = []
    app.heuristics = []
    app.allBoardStates = []
    app.depthLimit = 6
    app.bestMove = None

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
    app.isBlackTurn = False
    app.isWhiteTurn = True

    # Castling rights for kings 
    app.canBKingCastle = True
    app.canWKingCastle = True
    app.canlBRookCastle = True
    app.canrBRookCastle = True
    app.canlWRookCastle = True
    app.canrWRookCastle = True

    # Castling rights for AI kings 
    app.canAIBKingCastle = True
    app.canAIWKingCastle = True
    app.canAIlBRookCastle = True
    app.canAIrBRookCastle = True
    app.canAIlWRookCastle = True
    app.canAIrWRookCastle = True

    # Kings are in check:
    app.wKingCheck = False
    app.bKingCheck = False

    # If the king is in check this will find his legal squares to move to:
    app.illegalKingMoves = []
    app.illegalAIKingMoves = []

    # En Passant
    # create two fantom pawns that go to places where there is a pawn that has just
    # advanced two squares and then leaves 
    app.whiteEnPassantPawn = [100,100,'\u2659']
    app.blackEnPassantPawn = [101,101,'\u265F']
    app.blackAIEnPassantPawn = [102,102,'\u265F']
    app.whiteAIEnPassantPawn = [103,103,'\u2659']

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
                  'aWPawn':[6,0,'\u2659',app.aWPawnHasBeenPromoted],
                  'bWPawn':[6,1,'\u2659',app.bWPawnHasBeenPromoted],
                  'cWPawn':[6,2,'\u2659',app.cWPawnHasBeenPromoted],
                  'dWPawn':[6,3,'\u2659',app.dWPawnHasBeenPromoted],
                  'eWPawn':[6,4,'\u2659',app.eWPawnHasBeenPromoted],
                  'fWPawn':[6,5,'\u2659',app.fWPawnHasBeenPromoted],
                  'gWPawn':[6,6,'\u2659',app.gWPawnHasBeenPromoted],
                  'hWPawn':[6,7,'\u2659',app.hWPawnHasBeenPromoted],

                  'bKing':[0,4,'\u265A',app.canBKingCastle],'bQueen':[0,3,'\u265B'],'lBKnight':[0,1,'\u265E'],
                  'rBKnight':[0,6,'\u265E'],'lBRook':[0,0,'\u265C',app.canlBRookCastle],
                  'rBRook':[0,7,'\u265C',app.canrBRookCastle],
                  'lBBishop':[0,2,'\u265D'],'rBBishop':[0,5,'\u265D'],
                  'aBPawn':[1,0,'\u265F',app.aBPawnHasBeenPromoted],
                  'bBPawn':[1,1,'\u265F',app.bBPawnHasBeenPromoted],
                  'cBPawn':[1,2,'\u265F',app.cBPawnHasBeenPromoted],
                  'dBPawn':[1,3,'\u265F',app.dBPawnHasBeenPromoted],
                  'eBPawn':[1,4,'\u265F',app.eBPawnHasBeenPromoted],
                  'fBPawn':[1,5,'\u265F',app.fBPawnHasBeenPromoted],
                  'gBPawn':[1,6,'\u265F',app.gBPawnHasBeenPromoted],
                  'hBPawn':[1,7,'\u265F',app.hBPawnHasBeenPromoted]}

    # Legal Moves of pieces
    app.allLegalPieceMoves = []

    # Legal Moves of AI pieces
    app.allLegalAIPieceMoves = []

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

    # Keep a list of all the pieces that are in a row/col/diag 
    # after an encountered piece for the A.I.
    app.afterAIPieceRowColDiag = []

    # current piece
    app.currPiece = 0

    # captured black and white piece positions:
    app.capBlackrow = 8
    app.capBlackcol = 0
    app.capWhiterow = -1
    app.capWhitecol = 7

    # Gamemodes 
    app.randomMode = False

def restartApp(app):
    # Toggle for who's turn it is:
    app.isBlackTurn = False
    app.isWhiteTurn = True

    # Castling rights for kings 
    app.canBKingCastle = True
    app.canWKingCastle = True
    app.canlBRookCastle = True
    app.canrBRookCastle = True
    app.canlWRookCastle = True
    app.canrWRookCastle = True

    # Castling rights for AI kings 
    app.canAIBKingCastle = True
    app.canAIWKingCastle = True
    app.canAIlBRookCastle = True
    app.canAIrBRookCastle = True
    app.canAIlWRookCastle = True
    app.canAIrWRookCastle = True

    # Pieces
    app.pieces = {'wKing':[7,4,'\u2654',app.canWKingCastle],'wQueen':[7,3,'\u2655'],'lWKnight':[7,1,'\u2658'],
                  'rWKnight':[7,6,'\u2658'],'lWRook':[7,0,'\u2656',app.canlWRookCastle],
                  'rWRook':[7,7,'\u2656',app.canrWRookCastle],
                  'lWBishop':[7,2,'\u2657'],'rWBishop':[7,5,'\u2657'],
                  'aWPawn':[6,0,'\u2659',app.aWPawnHasBeenPromoted],
                  'bWPawn':[6,1,'\u2659',app.bWPawnHasBeenPromoted],
                  'cWPawn':[6,2,'\u2659',app.cWPawnHasBeenPromoted],
                  'dWPawn':[6,3,'\u2659',app.dWPawnHasBeenPromoted],
                  'eWPawn':[6,4,'\u2659',app.eWPawnHasBeenPromoted],
                  'fWPawn':[6,5,'\u2659',app.fWPawnHasBeenPromoted],
                  'gWPawn':[6,6,'\u2659',app.gWPawnHasBeenPromoted],
                  'hWPawn':[6,7,'\u2659',app.hWPawnHasBeenPromoted],

                  'bKing':[0,4,'\u265A',app.canBKingCastle],'bQueen':[0,3,'\u265B'],'lBKnight':[0,1,'\u265E'],
                  'rBKnight':[0,6,'\u265E'],'lBRook':[0,0,'\u265C',app.canlBRookCastle],
                  'rBRook':[0,7,'\u265C',app.canrBRookCastle],
                  'lBBishop':[0,2,'\u265D'],'rBBishop':[0,5,'\u265D'],
                  'aBPawn':[1,0,'\u265F',app.aBPawnHasBeenPromoted],
                  'bBPawn':[1,1,'\u265F',app.bBPawnHasBeenPromoted],
                  'cBPawn':[1,2,'\u265F',app.cBPawnHasBeenPromoted],
                  'dBPawn':[1,3,'\u265F',app.dBPawnHasBeenPromoted],
                  'eBPawn':[1,4,'\u265F',app.eBPawnHasBeenPromoted],
                  'fBPawn':[1,5,'\u265F',app.fBPawnHasBeenPromoted],
                  'gBPawn':[1,6,'\u265F',app.gBPawnHasBeenPromoted],
                  'hBPawn':[1,7,'\u265F',app.hBPawnHasBeenPromoted]}

def keyPressed(app,event):
    if event.key == 'r':
        restartApp(app)
    elif event.key == 'c' and (app.twoPlayerMode or app.playerVsComputer) and\
        (app.fisherRandomChess or app.classicChess or app.weightedOdds):
        app.startGame = True
    elif event.key == 'm':
        appStarted(app)
    
def mousePressed(app,event):
    app.x,app.y = event.x,event.y
    if app.startGame:
        row,col = getCell(app,app.y,app.x)
        showPossibleMoves(app,row,col)

def mouseReleased(app,event):
    app.xx,app.yy = event.x,event.y
    if not app.startGame:
        selectGameMode(app,event)
    if app.startGame:
        pieceCaptured(app,app.x,app.y,app.xx,app.yy)
        selectPiece(app)
        legalPieceMoves(app)
        app.canCheck = True
        movePiece(app)
    if app.isBlackTurn and app.playerVsComputer and (app.mediumMode or app.hardMode):
        if app.hardMode:
            app.depthLimit = 2
        if app.mediumMode:
            app.depthLimit = 1
        minimaxAlgo(app)
        app.pieces = app.bestMove
        app.isBlackTurn = not app.isBlackTurn
    if app.playerVsComputer and app.easyMode and\
       (app.classicChess or app.fisherRandomChess or app.weightedOdds) and\
       app.startGame:
        app.pieces = moveBlackPieceRandomly(app)
        app.isBlackTurn = not app.isBlackTurn
    app.allLegalPieceMoves = []
    app.illegalKingMoves = []
    app.bKingCheck = False
    app.wKingCheck = False
    app.canCheck = False

def selectGameMode(app,event):
    if 580 < app.x < 620 and 160 < app.y < 200 and\
       580 < app.xx < 620 and 160 < app.yy < 200 and\
       not app.playerVsComputer:
       app.twoPlayerMode = True
    if 580 < app.x < 620 and 210 < app.y < 250 and\
       580 < app.xx < 620 and 210 < app.yy < 250 and\
       not app.twoPlayerMode:
       app.playerVsComputer = True
    if 220 < app.x < 260 and 290 < app.y < 330 and\
       220 < app.xx < 260 and 290 < app.yy < 330 and\
       app.playerVsComputer and not app.mediumMode and not app.hardMode:
       app.easyMode = True
    if 220 < app.x < 260 and 340 < app.y < 390 and\
       220 < app.xx < 260 and 340 < app.yy < 390 and\
       app.playerVsComputer and not app.easyMode and not app.hardMode:
       app.mediumMode = True
    if 220 < app.x < 260 and 400 < app.y < 450 and\
       220 < app.xx < 260 and 400 < app.yy < 450 and\
       app.playerVsComputer and not app.easyMode and not app.mediumHard:
       app.hardMode = True
    if 580 < app.x < 620 and 500 < app.y < 540 and\
       580 < app.xx < 620 and 500 < app.yy < 540 and\
       not app.fisherRandomChess and not app.weightedOdds:
       app.classicChess = True
    if 580 < app.x < 620 and 550 < app.y < 590 and\
       580 < app.xx < 620 and 550 < app.yy < 590 and\
       not app.classicChess and not app.weightedOdds:
       app.fisherRandomChess = True
    if 580 < app.x < 620 and 600 < app.y < 640 and\
       580 < app.xx < 620 and 600 < app.yy < 640 and\
       not app.classicChess and not app.fisherRandomChess:
       app.weightedOdds = True

def fisherRandomChess(app):
    app.canWKingCastle = app.canBKingCastle = False
    order = ['rook1','knight1','bishop1','queen','king','bishop2','knight2','rook2']
    random.shuffle(order)
    for i in range(len(order)):
        if order[i] == 'rook1':
            app.pieces['lWRook'][1] = app.pieces['lBRook'][1] = i
        elif order[i] == 'rook2':
            app.pieces['rWRook'][1] = app.pieces['rBRook'][1] = i
        elif order[i] == 'knight1':
            app.pieces['lWKnight'][1] = app.pieces['lBKnight'][1] = i
        elif order[i] == 'knight2':
            app.pieces['rWKnight'][1] = app.pieces['rBKnight'][1] = i
        elif order[i] == 'bishop1':
            app.pieces['lWBishop'][1] = app.pieces['lBBishop'][1] = i
        elif order[i] == 'bishop2':
            app.pieces['rWBishop'][1] = app.pieces['rBBishop'][1] = i
        elif order[i] == 'queen':
            app.pieces['bQueen'][1] = app.pieces['wQueen'][1] = i
        elif order[i] == 'king':
            app.pieces['bKing'][1] = app.pieces['wKing'][1] = i

def weightedOdds(app):
    app.canWKingCastle = app.canBKingCastle = False
    order = ['rook1','knight1','bishop1','queen','bishop2','knight2','rook2']
    piece = random.choice(order)
    if piece == 'rook1':
        app.pieces['lWRook'][0] = 100
    elif piece == 'rook2':
        app.pieces['rWRook'][0] = 100
    elif piece == 'knight1':
        app.pieces['lWKnight'][0] = 100
    elif piece == 'knight1':
        app.pieces['rWKnight'][0] = 100
    elif piece == 'bishop1':
        app.pieces['lWBishop'][0] = 100
    elif piece == 'bishop2':
        app.pieces['rWBishop'][0] = 100
    elif piece == 'queen':
        app.pieces['wQueen'][0] = 100
    
def timerFired(app):
    if app.fisherRandomChess and app.started:
        fisherRandomChess(app)
        app.started = False
    if app.weightedOdds and app.started:
        weightedOdds(app)
        app.started = False

def isInBoard(row,col):
    if -1<row<8 and -1<col<8:
        return True
    else: return False

def movePiece(app):
    # moves the pieces
    kings = ['wKing','bKing']
    rooks = ['rWRook','lWRook','rBRook','lBRook']
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
        if (app.isBlackTurn and piece in app.blackPieces) or\
           (not app.isBlackTurn and piece in app.whitePieces):
            if app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol):
                if not ((piece == 'wKing' or piece == 'bKing') and abs(newcol - olecol == 2)):
                    app.pieces[piece][0] = newrow
                    app.pieces[piece][1] = newcol
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.blackPieces:
                    app.isBlackTurn = False
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol):
                    if piece in pawns and piece in app.whitePieces and newrow == 0:
                        app.pieces[piece][3] = True
                    if piece in pawns and piece in app.blackPieces and newrow == 7:
                        app.pieces[piece][3] = True
                if not moveIsLegal(app,piece,newrow,newcol,olerow,olecol) or\
                    passedPiece(app,newrow,newcol,olerow,olecol):
                    app.pieces[piece][0] = olerow
                    app.pieces[piece][1] = olecol

            # Castling
            if piece == 'wKing' and newcol-olecol == 2 and\
                app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleKingSideWhite(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.blackPieces:
                    app.isBlackTurn = False
                    app.wKingCheck = False
                    app.bKingCheck = False
                if piece == 'wKing':
                    app.canWKingCastle = False
                if piece == 'lWRook':
                    app.canlWRookCastle = False
            elif piece == 'wKing' and newcol-olecol == -2 and\
                app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleQueenSideWhite(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if piece == 'wKing':
                    app.canWKingCastle = False
                if piece == 'rWRook':
                    app.canrWRookCastle = False
            if piece == 'bKing' and newcol-olecol == 2 and\
                app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleKingSideBlack(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.blackPieces:
                    app.isBlackTurn = False
                if piece == 'bKing':
                    app.canBKingCastle = False
                if piece == 'lBRook':
                    app.canlWRookCastle = False
            elif piece == 'bKing' and newcol-olecol == -2 and\
                app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleQueenSideBlack(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.whitePieces:
                    app.isBlackTurn = True
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece in app.blackPieces:
                    app.isBlackTurn = False
                if piece == 'bKing':
                    app.canBKingCastle = False
                if piece == 'rBRook':
                    app.canrBRookCastle = False
        
            # En Passant
            if piece in pawns and piece in app.blackPieces and newrow - olerow == 2:
                if app.pieces[piece][0] == newrow and app.pieces[piece][1] == newcol:
                    app.blackEnPassantPawn[0] = newrow - 1
                    app.blackEnPassantPawn[1] = newcol
            if piece in pawns and piece in app.whitePieces and newrow - olerow == -2:
                if app.pieces[piece][0] == newrow and app.pieces[piece][1] == newcol:
                    app.whiteEnPassantPawn[0] = newrow + 1
                    app.whiteEnPassantPawn[1] = newcol


    # Pawn Promotion
    for piece in app.pieces:
        if app.pieces[piece] == elementsOfPiece and isInBoard(olerow,olecol) and piece in pawns:
            if elementsOfPiece[3] and getPieceFromCell(app,olerow,olecol) != 0 and\
                 newrow == 0 and app.pieces[piece][0] == newrow and piece in app.whitePieces:
                app.pieces[getPieceFromCell(app,olerow,olecol)][2] = '\u2655' 
            if elementsOfPiece[3] and getPieceFromCell(app,olerow,olecol) != 0 and\
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
    kings =   ['wKing','bKing']
    queens =  ['wQueen','bQueen']
    knights = ['rWKnight','lWKnight','rBKnight','lBKnight']
    bishops = ['rWBishop','lWBishop','rBBishop','lBBishop']
    rooks =   ['rWRook','lWRook','rBRook','lBRook']
    pawns =   ['aWPawn','bWPawn','cWPawn','dWPawn',
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
        
        whiteKingIndex = blackKingIndex = 0

        for kingIndex in range(len(app.allLegalPieceMoves)):
            if app.allLegalPieceMoves[kingIndex][0] == 'wKing':
                whiteKingIndex = kingIndex
            elif app.allLegalPieceMoves[kingIndex][0] == 'bKing':
                blackKingIndex = kingIndex

        # Check to see if the king is in check
        # if piece in kings and app.canCheck:
        for notKing in range(len(app.allLegalPieceMoves)):
            if app.allLegalPieceMoves[notKing][0] != None and\
                    app.allLegalPieceMoves[notKing][0] != 'wKing' and\
                    app.allLegalPieceMoves[notKing][0] != 'bKing':
                if (newrow,newcol) in app.allLegalPieceMoves[notKing][1] and\
                   ((newrow,newcol) == (app.pieces['wKing'][0],app.pieces['wKing'][1]) or\
                    (newrow,newcol) == (app.pieces['bKing'][0],app.pieces['bKing'][1])):
                    if app.allLegalPieceMoves[notKing][0] in app.blackPieces or\
                       app.allLegalPieceMoves[notKing][0] in app.whitePieces:
                        app.illegalKingMoves.append((newrow,newcol))
                    if app.allLegalPieceMoves[notKing][0] in app.blackPieces and\
                       app.illegalKingMoves != []:
                        app.wKingCheck = True
                    if app.allLegalPieceMoves[notKing][0] in app.whitePieces and\
                       app.illegalKingMoves != []:
                        app.bKingCheck = True
            
        # check for legal movement
        if piece in kings and\
            ((abs(newcol - olecol) == 1 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 0 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 0) or\
            (abs(newcol - olecol) == 0 and abs(newrow - olerow) == 0)) and\
            (newrow,newcol) not in app.illegalKingMoves:
            return True
        if piece in kings and\
            (app.canWKingCastle and app.canlWRookCastle and getPieceFromCell(app,7,1) == 0 and\
            getPieceFromCell(app,7,2) == 0 and getPieceFromCell(app,7,3) == 0 and\
            newcol - olecol == -2 and newrow == olerow and piece == kings[0]) and not app.wKingCheck:
            return True
        if piece in kings and\
            (app.canWKingCastle and app.canrWRookCastle and getPieceFromCell(app,7,5) == 0 and\
            getPieceFromCell(app,7,6) == 0 and newcol - olecol == 2 and\
            newrow == olerow and piece == kings[0]) and not app.wKingCheck:
            return True
        if piece in kings and\
            (app.canBKingCastle and app.canlBRookCastle and getPieceFromCell(app,0,1) == 0 and\
            getPieceFromCell(app,0,2) == 0 and getPieceFromCell(app,0,3) == 0 and\
            newcol - olecol == -2 and newrow == olerow and piece == kings[1]) and not app.bKingCheck:
            return True
        if piece in kings and\
            (app.canBKingCastle and app.canrBRookCastle and getPieceFromCell(app,0,5) == 0 and\
            getPieceFromCell(app,0,6) == 0 and newcol - olecol == 2 and\
            newrow == olerow and piece == kings[1]) and not app.bKingCheck:
            return True
        elif piece in queens and\
             ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow)) or\
            (newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in pawns and (piece != 0 and (app.pieces[piece][2] == '\u265B' or app.pieces[piece][2] == '\u2655')) and\
             ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow)) or\
            (newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in knights and\
            ((abs(newcol - olecol) == 2 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 2)):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in bishops and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow))):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in rooks and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in pawns and piece in app.blackPieces and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            (((newrow - olerow) == 1 and olecol - newcol == 0 and\
            getWhitePieceFromCell(app,newrow,newcol) not in app.whitePieces) or\
            (olerow == 1 and (newrow - olerow) == 2 and olecol - newcol == 0 and\
            getWhitePieceFromCell(app,newrow,newcol) not in app.whitePieces) or\
            (getPieceFromCell(app,newrow,newcol) != 0 and\
            getWhitePieceFromCell(app,newrow,newcol) in app.whitePieces and\
            (newrow - olerow) == 1 and abs(olecol - newcol) == 1)):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in pawns and piece in app.whitePieces and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            (((newrow - olerow) == -1 and olecol - newcol == 0 and\
            getBlackPieceFromCell(app,newrow,newcol) not in app.blackPieces) or\
            (olerow == 6 and (newrow - olerow) == -2 and olecol - newcol == 0 and\
            getBlackPieceFromCell(app,newrow,newcol) not in app.blackPieces) or\
            (getPieceFromCell(app,newrow,newcol) != 0 and\
            getBlackPieceFromCell(app,newrow,newcol) in app.blackPieces and\
            (newrow - olerow) == -1 and abs(olecol - newcol) == 1)):
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        if piece in pawns and piece in app.whitePieces and\
            ((newrow - olerow) == -1 and abs(olecol - newcol) == 1) and\
            getBlackPieceFromCell(app,newrow,newcol) == app.blackEnPassantPawn:
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        if piece in pawns and piece in app.blackPieces and\
            ((newrow - olerow) == 1 and abs(olecol - newcol) == 1) and\
            getWhitePieceFromCell(app,newrow,newcol) == app.whiteEnPassantPawn:
            if app.wKingCheck and piece in app.whitePieces and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece in app.blackPieces and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True

def kingInCheck(app):
    if (app.pieces['wKing'][0],app.pieces['wKing'][1]) in app.allLegalPieceMoves:
        app.wKingCheck = True
    elif (app.pieces['bKing'][0],app.pieces['bKing'][1]) in app.allLegalPieceMoves:
        app.bKingCheck = True
    else:
        app.wKingCheck = app.bKingCheck = False

def pawnPromotion(app,piece):
    app.pieces[piece][3] = True
    if piece in app.whitePieces:
        app.pieces[piece][2] = '\u2655'
    elif piece in app.blackPieces:
        app.pieces[piece][2] = '\u265B'

def castleQueenSideWhite(app):
    app.pieces['wKing'][1] -= 2
    app.pieces['lWRook'][1] += 3

def castleKingSideWhite(app):
    app.pieces['wKing'][1] += 2
    app.pieces['rWRook'][1] -= 2

def castleQueenSideBlack(app):
    app.pieces['bKing'][1] -= 2
    app.pieces['lBRook'][1] += 3

def castleKingSideBlack(app):
    app.pieces['bKing'][1] += 2
    app.pieces['rBRook'][1] -= 2

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
    if app.blackEnPassantPawn[0] == newRow and app.blackEnPassantPawn[1] == newCol:
        newPiece = app.blackEnPassantPawn
    elif app.whiteEnPassantPawn[0] == newRow and app.whiteEnPassantPawn[1] == newCol:
        newPiece = app.whiteEnPassantPawn
    if moveIsLegal(app,oldPiece,newRow,newCol,oleRow,oleCol):
        if not (selectPiece(app) or passedPiece(app, newRow, newCol, oleRow, oleCol)):
            if oldPiece in app.blackPieces and (newPiece in app.whitePieces or newPiece == app.whiteEnPassantPawn):
                if newPiece == app.whiteEnPassantPawn:
                    newPiece = getPieceFromCell(app,newRow - 1,newCol)
                app.pieces[newPiece][0] = app.capWhiterow
                app.pieces[newPiece][1] = app.capWhitecol
                app.pieces[oldPiece][0] = newRow
                app.pieces[oldPiece][1] = newCol
                app.capWhitecol -= 1
                app.whiteEnPassantPawn[0] = 100
                if app.capWhitecol == 0:
                    app.capWhitecol = 7
                    app.capWhiterow = -2
            if oldPiece in app.whitePieces and (newPiece in app.blackPieces or newPiece == app.blackEnPassantPawn):
                if newPiece == app.blackEnPassantPawn:
                    newPiece = getPieceFromCell(app,newRow + 1,newCol)
                app.pieces[newPiece][0] = app.capBlackrow
                app.pieces[newPiece][1] = app.capBlackcol
                app.pieces[oldPiece][0] = newRow
                app.pieces[oldPiece][1] = newCol
                app.capBlackcol += 1
                app.blackEnPassantPawn[0] = 101
                if app.capBlackcol == 7:
                    app.capBlackcol = 9
                    app.capBlackrow = 0

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
        app.illegalKingMoves = []
        app.wKingCheck = app.bKingCheck = False
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
    app.illegalKingMoves = []
    app.wKingCheck = app.bKingCheck = False
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
    if thePiece == 0:
        if app.blackEnPassantPawn[0] == row and app.blackEnPassantPawn[1] == col:
            thePiece = app.blackEnPassantPawn
    return thePiece

def getWhitePieceFromCell(app,row,col):
   # returns the black piece from the given position
    thePiece = 0
    for piece in app.whitePieces:
        if app.pieces[piece][0] == row and app.pieces[piece][1] == col:
            thePiece = piece
    if thePiece == 0:
        if app.whiteEnPassantPawn[0] == row and app.whiteEnPassantPawn[1] == col:
            thePiece = app.whiteEnPassantPawn
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

def getCellBounds(app,row,col):
    # gets cell bounds
    x0 = app.margin + app.cellSize*col
    y0 = app.margin + app.cellSize*row
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    return x0,y0,x1,y1


############## A.I. Algorithm ###############
#*********** Completely Random *************#
def moveBlackPieceRandomly(app):
    boardStates = generateAllFutureBoardStates(app,app.pieces,app.allLegalPieceMoves,True)
    return random.choice(boardStates)


#*********** Minimax Attempt 1 *************#
# the function directly below is inspired by
# https://www.chessprogramming.org/Evaluation
def boardWorthHeuristic(app,pieces):
    kings =   ['wKing','bKing']
    queens =  ['wQueen','bQueen']
    knights = ['rWKnight','lWKnight','rBKnight','lBKnight']
    blackKnights = ['rBKnight','lBKnight']
    whiteKnights = ['rWKnight','lWKnight']
    bishops = ['rWBishop','lWBishop','rBBishop','lBBishop']
    blackBishops = ['rBBishop','lBBishop']
    whiteBishops = ['rWBishop','lWBishop']
    rooks =   ['rWRook','lWRook','rBRook','lBRook']
    blackRooks = ['rBRook','lBRook']
    whiteRooks = ['rWRook','lWRook']
    pawns =   ['aWPawn','bWPawn','cWPawn','dWPawn',
               'eWPawn','fWPawn','gWPawn','hWPawn',
               'aBPawn','bBPawn','cBPawn','dBPawn',
               'eBPawn','fBPawn','gBPawn','hBPawn']
    blackPawns = ['aBPawn','bBPawn','cBPawn','dBPawn',
                  'eBPawn','fBPawn','gBPawn','hBPawn']
    whitePawns = ['aWPawn','bWPawn','cWPawn','dWPawn',
                  'eWPawn','fWPawn','gWPawn','hWPawn']

    # board score
    boardScore = 0
    piecesInTheBoard = []

    # individual piece counts:
    wPawnCount = 0
    bPawnCount = 0
    wRookCount = 0
    bRookCount = 0
    wBishopCnt = 0
    bBishopCnt = 0
    wKnightCnt = 0
    bKnightCnt = 0
    wQueenCount = 0
    bQueenCount = 0
    wKingCount = 0
    bKingCount = 0

    for piece in pieces:
        if isInBoard(pieces[piece][0],pieces[piece][1]):
            piecesInTheBoard.append(piece)
    
    # Calculate the Board Score
    for piece in piecesInTheBoard:
        if piece in blackPawns:
            bPawnCount += 1
        elif piece in whitePawns:
            wPawnCount += 1
        elif piece in blackBishops:
            bBishopCnt += 1
        elif piece in whiteBishops:
            wBishopCnt += 1
        elif piece in blackRooks:
            bRookCount += 1
        elif piece in whiteRooks:
            wRookCount += 1
        elif piece in blackKnights:
            bKnightCnt += 1
        elif piece in whiteKnights:
            wKnightCnt += 1
        elif piece == 'wQueen':
            wQueenCount += 1
        elif piece == 'bQueen':
            bQueenCount += 1
        elif piece == 'wKing':
            wKingCount += 1
        elif piece == 'bKing':
            bKingCount += 1
    
    legalWhiteMoves = 0
    legalBlackMoves = 0

    # total white piece moves
    for piece in pieces:
        for legalMove in app.allLegalPieceMoves:
            if legalMove[0] == piece and\
                (pieces[piece][0],pieces[piece][1]) not in legalMove[1]:
                if piece in app.whitePieces:
                    legalWhiteMoves += len(legalMove[1])
                elif piece in app.blackPieces:
                    legalBlackMoves += len(legalMove[1])
            if legalMove[0] == piece and\
                (pieces[piece][0],pieces[piece][1]) in legalMove[1]:
                legalMoveSet = set(legalMove[1])
                list(legalMoveSet)
                legalMoveSet.remove((pieces[piece][0],pieces[piece][1]))
                if piece in app.whitePieces:
                    legalWhiteMoves += len(legalMoveSet)
                elif piece in app.blackPieces:
                    legalBlackMoves += len(legalMoveSet)

    boardScore = 1*(wPawnCount - bPawnCount) + \
                 3*(wBishopCnt - bBishopCnt) + \
                 3*(wKnightCnt - bKnightCnt) + \
                 5*(wRookCount - bRookCount) + \
                 9*(wQueenCount - bQueenCount) + \
                 200*(wKingCount - bKingCount) + \
                 0.1*(legalWhiteMoves - legalBlackMoves)
    
    return boardScore

def generateAllFutureBoardStates(app,pieces,moves,isBlackTurn):
    boardStates = []
    piecesCopy = copy.deepcopy(pieces)
    doableMoves = []
    playedMoves = []
    for move in moves:
        if move[0] != None:
            doableMoves.append(move)

    i = 0
    while i < len(doableMoves):
        if doableMoves[i][1] == []:
            doableMoves.pop(i)
        else:
            i += 1
    
    if not isBlackTurn:   
        for move in doableMoves:
           for j in range(len(move[1])):
                if move[0] in app.whitePieces:
                    piecesCopy[move[0]][0] = move[1][j][0]
                    piecesCopy[move[0]][1] = move[1][j][1]
                    playedMoves.append((move[0],move[1][j]))
                    boardStates.append(piecesCopy)
                piecesCopy = copy.deepcopy(pieces)
            
    elif isBlackTurn:
        for move in doableMoves:
            for j in range(len(move[1])):
                if move[0] in app.blackPieces:
                    piecesCopy[move[0]][0] = move[1][j][0]
                    piecesCopy[move[0]][1] = move[1][j][1]
                    playedMoves.append((move[0],move[1][j]))
                    boardStates.append(piecesCopy)
                piecesCopy = copy.deepcopy(pieces)
    
    i = 0
    while i < len(boardStates):
        if boardStates[i][playedMoves[i][0]][0] == pieces[playedMoves[i][0]][0] and\
            boardStates[i][playedMoves[i][0]][1] == pieces[playedMoves[i][0]][1]:
            boardStates.pop(i)
            playedMoves.pop(i)
        i+=1
    
    i = 0
    while i < len(boardStates):
        if boardStates[i] == pieces:
            boardStates.pop(i)
            playedMoves.pop(i)
        else:
            i+=1

    return boardStates

# inspired by:
# https://www.youtube.com/watch?v=VoVPYVwulQs&feature=emb_title
def minimaxAlgo(app):
    pieces = copy.deepcopy(app.pieces)
    moves = myDeepCopy(app.allLegalPieceMoves)
    minimaxHelper(app,pieces,moves,True,0)

def minimaxHelper(app,pieces,moves,isBlackTurn,depth):
    boardStates = generateAllFutureBoardStates(app,pieces,moves,isBlackTurn)
    highestValue = -10**6
    for state in boardStates:
        currentValue = maxi(app,state,depth+1)
        if currentValue > highestValue:
            highestValue = currentValue
            app.bestMove = state

def mini(app,state,depth):
    legalAIPieceMoves(app,state)
    boardStates = generateAllFutureBoardStates(app,state,app.allLegalAIPieceMoves,False)
    if depth == app.depthLimit:
        return boardWorthHeuristic(app,state)
    else:
        lowestValue = 10**6
        for state in boardStates:
            currentValue = maxi(app,state,depth+1)
            if currentValue < lowestValue:
                lowestValue = currentValue
        return lowestValue

def maxi(app,state,depth):
    legalAIPieceMoves(app,state)
    boardStates = generateAllFutureBoardStates(app,state,app.allLegalAIPieceMoves,True)
    if depth == app.depthLimit:
        return boardWorthHeuristic(app,state)
    else:
        highestValue = -10**6
        for state in boardStates:
            currentValue = mini(app,state,depth+1)
            if currentValue > highestValue:
                highestValue = currentValue
        return highestValue



# Reworked functions for the minimax algorithm
def possibleAIMoves(app,pieceRow,pieceCol,pieces):
    piece = getAIPieceFromCell(app,pieceRow,pieceCol,pieces)
    if getAIPieceFromCell(app,pieceRow,pieceCol,pieces) != 0:
        olerow = pieces[getAIPieceFromCell(app,pieceRow,pieceCol,pieces)][0]
        olecol = pieces[getAIPieceFromCell(app,pieceRow,pieceCol,pieces)][1]
    for row in range(-app.rows,app.rows):
            for col in range(-app.cols,app.cols):
                if AIMoveIsLegal(app,piece,row,col,olerow,olecol,pieces):
                    app.legalAIMoves.append((row,col))
    app.legalAIMoves = list(set(app.legalAIMoves)-set(app.afterAIPieceRowColDiag))
    app.allLegalAIPieceMoves.append([piece,app.legalAIMoves])
    app.legalAIMoves = []
    app.afterAIPieceRowColDiag = []

def getAIPieceFromCell(app,row,col,pieces):
    # returns the piece from the given position
    thePiece = 0
    for piece in pieces:
        if pieces[piece][0] == row and pieces[piece][1] == col:
            thePiece = piece
    return thePiece

def getAIBlackPieceFromCell(app,row,col,pieces):
   # returns the black piece from the given position
    thePiece = 0
    for piece in app.blackPieces:
        if pieces[piece][0] == row and pieces[piece][1] == col:
            thePiece = piece
    if thePiece == 0:
        if app.blackAIEnPassantPawn[0] == row and app.blackAIEnPassantPawn[1] == col:
            thePiece = app.blackAIEnPassantPawn
    return thePiece

def getAIWhitePieceFromCell(app,row,col,pieces):
   # returns the black piece from the given position
    thePiece = 0
    for piece in app.whitePieces:
        if pieces[piece][0] == row and pieces[piece][1] == col:
            thePiece = piece
    if thePiece == 0:
        if app.whiteAIEnPassantPawn[0] == row and app.whiteAIEnPassantPawn[1] == col:
            thePiece = app.whiteAIEnPassantPawn
    return thePiece

def legalAIPieceMoves(app,pieces):
    for row in range(app.rows):
        for col in range(app.cols):
            piece = getAIPieceFromCell(app,row,col,pieces)
            if piece == 0:
                app.allLegalAIPieceMoves.append([None,[row,col]])
            else:
                possibleAIMoves(app,row,col,pieces)

def AIMoveIsLegal(app,piece,newrow,newcol,olerow,olecol,pieces):
    kings =   ['wKing','bKing']
    queens =  ['wQueen','bQueen']
    knights = ['rWKnight','lWKnight','rBKnight','lBKnight']
    bishops = ['rWBishop','lWBishop','rBBishop','lBBishop']
    rooks =   ['rWRook','lWRook','rBRook','lBRook']
    pawns =   ['aWPawn','bWPawn','cWPawn','dWPawn',
               'eWPawn','fWPawn','gWPawn','hWPawn',
               'aBPawn','bBPawn','cBPawn','dBPawn',
               'eBPawn','fBPawn','gBPawn','hBPawn']

    if isInBoard(newrow,newcol):
        if piece in app.blackPieces and getAIPieceFromCell(app,newrow,newcol,pieces) != piece and\
            getAIPieceFromCell(app,newrow,newcol,pieces) in app.blackPieces or\
            piece in app.whitePieces and getAIPieceFromCell(app,newrow,newcol,pieces) != piece and\
            getAIPieceFromCell(app,newrow,newcol,pieces) in app.whitePieces:
            if piece not in knights:
                if newrow > olerow and newcol == olecol:
                    for row in range(newrow,8):
                        app.afterAIPieceRowColDiag.append((row,olecol))
                if newrow < olerow and newcol == olecol:
                    for row in range(0,newrow+1):
                        app.afterAIPieceRowColDiag.append((row,olecol))
                
                # checks whether there are pieces ahead of the current piece in the same col
                if newcol > olecol and newrow == olerow:
                    for col in range(newcol,8):
                        app.afterAIPieceRowColDiag.append((olerow,col))
                if newcol < olecol and newrow == olerow:
                    for col in range(0,newcol+1):
                        app.afterAIPieceRowColDiag.append((olerow,col))

                # checks whether there are pieces ahead of the current piece in the same diagonal
                if newcol>olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol,8):
                        for row in range(newrow,8):
                            app.afterAIPieceRowColDiag.append((row,col))
                if newcol>olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol,8):
                        for row in range(0,newrow+1):
                            app.afterAIPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol+1):
                        for row in range(newrow,8):
                            app.afterAIPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol+1):
                        for row in range(0,newrow+1):
                            app.afterAIPieceRowColDiag.append((row,col))

        if piece in app.blackPieces and getAIPieceFromCell(app,newrow,newcol,pieces) != piece and\
            getAIPieceFromCell(app,newrow,newcol,pieces) in app.whitePieces or\
            piece in app.whitePieces and getAIPieceFromCell(app,newrow,newcol,pieces) != piece and\
            getAIPieceFromCell(app,newrow,newcol,pieces) in app.blackPieces:
            if piece not in knights:
                if newrow > olerow and newcol == olecol:
                    for row in range(newrow+1,8):
                        app.afterAIPieceRowColDiag.append((row,olecol))
                if newrow < olerow and newcol == olecol:
                    for row in range(0,newrow):
                        app.afterAIPieceRowColDiag.append((row,olecol))
                
                # checks whether there are pieces ahead of the current piece in the same col
                if newcol > olecol and newrow == olerow:
                    for col in range(newcol+1,8):
                        app.afterAIPieceRowColDiag.append((olerow,col))
                if newcol < olecol and newrow == olerow:
                    for col in range(0,newcol):
                        app.afterAIPieceRowColDiag.append((olerow,col))

                # checks whether there are pieces ahead of the current piece in the same diagonal
                if newcol>olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol+1,8):
                        for row in range(newrow+1,8):
                            app.afterAIPieceRowColDiag.append((row,col))
                if newcol>olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(newcol+1,8):
                        for row in range(0,newrow):
                            app.afterAIPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow>olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol):
                        for row in range(newrow+1,8):
                            app.afterAIPieceRowColDiag.append((row,col))
                if newcol<olecol and newrow<olerow and abs(newcol-olecol) ==  abs(newrow-olerow):
                    for col in range(0,newcol):
                        for row in range(0,newrow):
                            app.afterAIPieceRowColDiag.append((row,col))

        if piece in app.blackPieces and getAIPieceFromCell(app,newrow,newcol,pieces) != piece and\
            getAIPieceFromCell(app,newrow,newcol,pieces) in app.blackPieces or\
            piece in app.whitePieces and getAIPieceFromCell(app,newrow,newcol,pieces) != piece and\
            getAIPieceFromCell(app,newrow,newcol,pieces) in app.whitePieces:
            return False
        
        # Check to see if the king is in check
        if piece in kings:
            for notKing in range(len(app.allLegalAIPieceMoves)):
                if app.allLegalAIPieceMoves[notKing] != None and\
                     app.allLegalAIPieceMoves[notKing] != 'wKing' and\
                     app.allLegalAIPieceMoves[notKing] != 'bKing':
                    if (newrow,newcol) in app.allLegalAIPieceMoves[notKing][1]:
                        app.illegalAIKingMoves.append((newrow,newcol))
            if piece == 'wKing':
                app.wKingCheck = True
            elif piece == 'bKing':
                app.bKingCheck = True
        
        # check for legal movement
        if piece in kings and\
            ((abs(newcol - olecol) == 1 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 0 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 0) or\
            (abs(newcol - olecol) == 0 and abs(newrow - olerow) == 0)):
            return True
        if piece in kings and\
            (app.canAIWKingCastle and app.canAIlWRookCastle and getAIPieceFromCell(app,7,1,pieces) == 0 and\
            getAIPieceFromCell(app,7,2,pieces) == 0 and getAIPieceFromCell(app,7,3,pieces) == 0 and\
            newcol - olecol == -2 and newrow == olerow and piece == kings[0]):
            return False
        if piece in kings and\
            (app.canAIWKingCastle and app.canAIrWRookCastle and getAIPieceFromCell(app,7,5,pieces) == 0 and\
            getAIPieceFromCell(app,7,6,pieces) == 0 and newcol - olecol == 2 and\
            newrow == olerow and piece == kings[0]):
            return False
        if piece in kings and\
            (app.canAIBKingCastle and app.canAIlBRookCastle and getAIPieceFromCell(app,0,1,pieces) == 0 and\
            getAIPieceFromCell(app,0,2,pieces) == 0 and getAIPieceFromCell(app,0,3,pieces) == 0 and\
            newcol - olecol == -2 and newrow == olerow and piece == kings[1]):
            return True
        if piece in kings and\
            (app.canAIBKingCastle and app.canAIrBRookCastle and getAIPieceFromCell(app,0,5,pieces) == 0 and\
            getAIPieceFromCell(app,0,6,pieces) == 0 and newcol - olecol == 2 and\
            newrow == olerow and piece == kings[1]):
            return True
        elif piece in queens and\
             ((newrow,newcol) not in app.afterAIPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow)) or\
            (newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            return True
        elif piece in pawns and (piece != 0 and (pieces[piece][2] == '\u265B' or pieces[piece][2] == '\u2655')) and\
             ((newrow,newcol) not in app.afterAIPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow)) or\
            (newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            return True
        elif piece in knights and\
            ((abs(newcol - olecol) == 2 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 2)):
            return True
        elif piece in bishops and ((newrow,newcol) not in app.afterAIPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow))):
            return True
        elif piece in rooks and ((newrow,newcol) not in app.afterAIPieceRowColDiag) and\
            ((newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            return True
        elif piece in pawns and piece in app.blackPieces and ((newrow,newcol) not in app.afterAIPieceRowColDiag) and\
            (((newrow - olerow) == 1 and olecol - newcol == 0 and\
            getAIWhitePieceFromCell(app,newrow,newcol,pieces) not in app.whitePieces) or\
            (olerow == 1 and (newrow - olerow) == 2 and olecol - newcol == 0 and\
            getAIWhitePieceFromCell(app,newrow,newcol,pieces) not in app.whitePieces) or\
            (getAIPieceFromCell(app,newrow,newcol,pieces) != 0 and\
            getAIWhitePieceFromCell(app,newrow,newcol,pieces) in app.whitePieces and\
            (newrow - olerow) == 1 and abs(olecol - newcol) == 1)):
            return True
        elif piece in pawns and piece in app.whitePieces and ((newrow,newcol) not in app.afterAIPieceRowColDiag) and\
            (((newrow - olerow) == -1 and olecol - newcol == 0 and\
            getAIBlackPieceFromCell(app,newrow,newcol,pieces) not in app.blackPieces) or\
            (olerow == 6 and (newrow - olerow) == -2 and olecol - newcol == 0 and\
            getAIBlackPieceFromCell(app,newrow,newcol,pieces) not in app.blackPieces) or\
            (getAIPieceFromCell(app,newrow,newcol,pieces) != 0 and\
            getAIBlackPieceFromCell(app,newrow,newcol,pieces) in app.blackPieces and\
            (newrow - olerow) == -1 and abs(olecol - newcol) == 1)):
            return True
        if piece in pawns and piece in app.whitePieces and\
            ((newrow - olerow) == -1 and abs(olecol - newcol) == 1) and\
            getAIBlackPieceFromCell(app,newrow,newcol,pieces) == app.blackEnPassantPawn:
            return True
        if piece in pawns and piece in app.blackPieces and\
            ((newrow - olerow) == 1 and abs(olecol - newcol) == 1) and\
            getAIWhitePieceFromCell(app,newrow,newcol,pieces) == app.whiteEnPassantPawn:
            return True


############## Print 2d Lists ###############
# functions from CMU 15-112 F20
# http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
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

# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
def myDeepCopy(a):
    if (isinstance(a, list) or isinstance(a, tuple)):
        return [myDeepCopy(element) for element in a]
    else:
        return copy.copy(a)

############## U.I. --> Menu ################
def menu(app,canvas):
    rows,cols,cellSize,margin,width,height,pieceSize = gameDimensions()
    canvas.create_rectangle(0,0,700,700,fill = 'green')
    canvas.create_rectangle(20,20,680,680,fill = 'white')
    canvas.create_text(width//2,60, text = 'Chess',font = 'Arial 60 bold')
    canvas.create_text(120,120,text = 'Select a gamemode:',font = 'Arial 15')

    canvas.create_text(160,180,text = 'Two Player',font = 'Arial 30 bold')
    canvas.create_rectangle(580,160,620,200,fill = 'lightblue')
    if not app.twoPlayerMode:
        canvas.create_rectangle(585,165,615,195,fill = 'white')
    canvas.create_text(225,230,text = 'Player vs. Computer',font = 'Arial 30 bold')
    canvas.create_rectangle(580,210,620,250,fill = 'lightblue')
    if not app.playerVsComputer:
        canvas.create_rectangle(585,215,615,245,fill = 'white')

    canvas.create_text(110,270,text = 'Select a difficulty:',font = 'Arial 15')

    canvas.create_text(160,310,text = 'Easy',font = 'Arial 30 bold')
    canvas.create_rectangle(220,290,260,330,fill = 'lightblue')
    if not app.easyMode:
        canvas.create_rectangle(225,295,255,325,fill = 'white')
    canvas.create_text(160,360,text = 'Medium',font = 'Arial 30 bold')
    canvas.create_rectangle(220,340,260,380,fill = 'lightblue')
    if not app.mediumMode:
        canvas.create_rectangle(225,345,255,375,fill = 'white')
    canvas.create_text(160,410,text = 'Hard',font = 'Arial 30 bold')
    canvas.create_rectangle(220,390,260,430,fill = 'lightblue')
    if not app.hardMode:
        canvas.create_rectangle(225,395,255,425,fill = 'white')

    canvas.create_text(140,470,text = 'Select a Version of Chess:',font = 'Arial 15')

    canvas.create_text(180,520,text = 'Classic Chess',font = 'Arial 30 bold')
    canvas.create_rectangle(580,500,620,540,fill = 'lightblue')
    if not app.classicChess:
        canvas.create_rectangle(585,505,615,535,fill = 'white')
    canvas.create_text(190,570,text = 'Fisher Random',font = 'Arial 30 bold')
    canvas.create_rectangle(580,550,620,590,fill = 'lightblue')
    if not app.fisherRandomChess:
        canvas.create_rectangle(585,555,615,585,fill = 'white')
    canvas.create_text(190,620,text = 'Weighted Odds',font = 'Arial 30 bold')
    canvas.create_rectangle(580,600,620,640,fill = 'lightblue')
    if not app.weightedOdds:
        canvas.create_rectangle(585,605,615,635,fill = 'white')

    canvas.create_text(350,690,text = """'Press 'C' to continue!!'""" )
    canvas.create_rectangle(460,70,660,110)
    canvas.create_text(560,80,text = """While in game press 'r' to restart""")
    canvas.create_text(555,100,text = """Press 'm' to return to the menu""")


############### Draw Board ##################
def gameDimensions():
    width = height = 700
    rows = cols = 8
    margin = 70
    pieceSize = cellSize = (width - 2*margin)/8
    return (rows,cols,cellSize,margin,width,height,pieceSize)

def drawPieces(app,canvas):
    # initializes all the pieces on the board
    for piece in app.pieces:
        x,y = getPieceCoords(app,piece)
        canvas.create_text(x,y,text = app.pieces[piece][2],font = f'Arial {int(app.pieceSize)} bold')

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

def redrawAll(app,canvas):
    drawTerminalBoard(app)
    if not app.startGame:
        menu(app,canvas)
    elif app.startGame and (app.twoPlayerMode or app.playerVsComputer) and\
        (app.fisherRandomChess or app.classicChess or app.weightedOdds):
        drawBoard(app,canvas)
        drawPieces(app,canvas)

def playChess():
    rows,cols,cellSize,margin,width,height,pieceSize = gameDimensions()
    runApp(width=width, height=height)

def main():
    playChess()

if __name__ == '__main__':
    main()
