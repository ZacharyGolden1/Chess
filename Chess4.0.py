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



from cmu_112_graphics import *
import copy,random

############## Implementing Classes ###############
class King(object):
    def __init__(self,position,canCastleKingSide,canCastleQueenSide,isBlackPiece,character,isInCheck,isMated):
        self.position = position
        self.canCastleKingSide = canCastleKingSide
        self.canCastleQueenSide = canCastleQueenSide
        self.isBlackPiece = isBlackPiece
        self.character = character
        self.isInCheck = isInCheck
        self.isMated = isMated

class Queen(object):
    def __init__(self,position,hasBeenCaptured,isBlackPiece,character):        
        self.position = position
        self.hasBeenCaptured = hasBeenCaptured
        self.isBlackPiece = isBlackPiece
        self.character = character

class Rook(object):
    def __init__(self,position,hasBeenCaptured,isBlackPiece,character):        
        self.position = position
        self.hasBeenCaptured = hasBeenCaptured
        self.isBlackPiece = isBlackPiece
        self.character = character

class Bishop(object):
    def __init__(self,position,hasBeenCaptured,isBlackPiece,character):        
        self.position = position
        self.hasBeenCaptured = hasBeenCaptured
        self.isBlackPiece = isBlackPiece
        self.character = character

class Knight(object):
    def __init__(self,position,hasBeenCaptured,isBlackPiece,character):        
        self.position = position
        self.hasBeenCaptured = hasBeenCaptured
        self.isBlackPiece = isBlackPiece
        self.character = character

class Pawn(object):
    def __init__(self,position,hasBeenCaptured,enpassant,isBlackPiece,hasPromoted,character):        
        self.position = position
        self.hasBeenCaptured = hasBeenCaptured
        self.enpassant = enpassant
        self.isBlackPiece = isBlackPiece
        self.hasPromoted = hasPromoted
        self.character = character

class Board(object):
    def __init__(self,board):
        self.board = board

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
    app.legalMoves = set()

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

    # White then Black
    # Creating all Pieces
    app.aWPawn = Pawn((6,0),False,False,False,False,'\u2659')
    app.bWPawn = Pawn((6,1),False,False,False,False,'\u2659')
    app.cWPawn = Pawn((6,2),False,False,False,False,'\u2659')
    app.dWPawn = Pawn((6,3),False,False,False,False,'\u2659')
    app.eWPawn = Pawn((6,4),False,False,False,False,'\u2659')
    app.fWPawn = Pawn((6,5),False,False,False,False,'\u2659')
    app.gWPawn = Pawn((6,6),False,False,False,False,'\u2659')
    app.hWPawn = Pawn((6,7),False,False,False,False,'\u2659')

    app.lWRook = Rook((7,0),False,False,'\u2656')
    app.lWKnight = Knight((7,1),False,False,'\u2658')
    app.lWBishop = Bishop((7,2),False,False,'\u2657')
    app.wKing = King((7,3),True,True,False,'\u2654')
    app.wQueen = Queen((7,4),False,False,'\u2655')
    app.rWBishop = Bishop((7,5),False,False,'\u2657')
    app.rWKnight = Knight((7,6),False,False,'\u2658')
    app.rWRook = Rook((7,7),False,False,'\u2656')
    
    app.aBPawn = Pawn((1,0),False,False,True,False,'\u265F')
    app.bBPawn = Pawn((1,1),False,False,True,False,'\u265F')
    app.cBPawn = Pawn((1,2),False,False,True,False,'\u265F')
    app.dBPawn = Pawn((1,3),False,False,True,False,'\u265F')
    app.eBPawn = Pawn((1,4),False,False,True,False,'\u265F')
    app.fBPawn = Pawn((1,5),False,False,True,False,'\u265F')
    app.gBPawn = Pawn((1,6),False,False,True,False,'\u265F')
    app.hBPawn = Pawn((1,7),False,False,True,False,'\u265F')

    app.lBRook = Rook((0,0),False,False,'\u2656')
    app.lBKnight = Knight((0,1),False,False,'\u2658')
    app.lBBishop = Bishop((0,2),False,False,'\u2657')
    app.bKing = King((0,3),True,True,False,'\u2654')
    app.bQueen = Queen((0,4),False,False,'\u2655')
    app.rBBishop = Bishop((0,5),False,False,'\u2657')
    app.rBKnight = Knight((0,6),False,False,'\u2658')
    app.rBRook = Rook((0,7),False,False,'\u2656')

    # All Pieces
    app.pieces = [
        app.lWRook,app.lWKnight,app.lWBishop,app.wKing,app.wQueen,app.rWBishop,app.rWKnight,app.rWRook,
        app.aWPawn,app.bWPawn,app.cWPawn,app.dWPawn,app.eWPawn,app.fWPawn,app.gWPawn,app.hWPawn,
        
        app.aBPawn,app.bBPawn,app.cBPawn,app.dBPawn,app.eBPawn,app.fBPawn,app.gBPawn,app.hBPawn,
        app.lBRook,app.lBKnight,app.lBBishop,app.bKing,app.bQueen,app.rBBishop,app.rBKnight,app.rBRook
        ]

    # Piece by Color
    app.blackPieces = [
        app.aBPawn,app.bBPawn,app.cBPawn,app.dBPawn,app.eBPawn,app.fBPawn,app.gBPawn,app.hBPawn,
        app.lBRook,app.lBKnight,app.lBBishop,app.bKing,app.bQueen,app.rBBishop,app.rBKnight,app.rBRook
        ]
    
    app.whitePieces = [
        app.lWRook,app.lWKnight,app.lWBishop,app.wKing,app.wQueen,app.rWBishop,app.rWKnight,app.rWRook,
        app.aWPawn,app.bWPawn,app.cWPawn,app.dWPawn,app.eWPawn,app.fWPawn,app.gWPawn,app.hWPawn
    ]

    # Pieces by Name:
    app.rooks = [app.lWRook,app.rWRook,app.lBRook,app.rBRook]
    app.knights = [app.lWKnight,app.rWKnight,app.lBKnight,app.rBKnight]
    app.bishops = [app.lWBishop,app.rWBishop,app.lBBishop,app.rBBishop]
    app.queens = [app.wQueen,app.bQueen]
    app.kings = [app.wKing,app.bKing]
    app.pawns = [app.aWPawn,app.bWPawn,app.cWPawn,app.dWPawn,app.eWPawn,app.fWPawn,app.gWPawn,app.hWPawn,
                 app.aBPawn,app.bBPawn,app.cBPawn,app.dBPawn,app.eBPawn,app.fBPawn,app.gBPawn,app.hBPawn]
    
    # Legal Moves of pieces
    app.allLegalPieceMoves = []

    # All Possible Moves:
    app.wKingMoves = {'wKa1','wKa2','wKa3','wKa4','wKa5','wKa6','wKa7','wKa8',
                     'wKb1','wKb2','wKb3','wKb4','wKb5','wKb6','wKb7','wKb8',
                     'wKc1','wKc2','wKc3','wKc4','wKc5','wKc6','wKc7','wKc8',
                     'wKd1','wKd2','wKd3','wKd4','wKd5','wKd6','wKd7','wKd8',
                     'wKe1','wKe2','wKe3','wKe4','wKe5','wKe6','wKe7','wKe8',
                     'wKf1','wKf2','wKf3','wKf4','wKf5','wKf6','wKf7','wKf8',
                     'wKg1','wKg2','wKg3','wKg4','wKg5','wKg6','wKg7','wKg8',
                     'wKh1','wKh2','wKh3','wKh4','wKh5','wKh6','wKh7','wKh8'}
    
    app.bKingMoves = {'bKa1','bKa2','bKa3','bKa4','bKa5','bKa6','bKa7','bKa8',
                      'bKb1','bKb2','bKb3','bKb4','bKb5','bKb6','bKb7','bKb8',
                      'bKc1','bKc2','bKc3','bKc4','bKc5','bKc6','bKc7','bKc8',
                      'bKd1','bKd2','bKd3','bKd4','bKd5','bKd6','bKd7','bKd8',
                      'bKe1','bKe2','bKe3','bKe4','bKe5','bKe6','bKe7','bKe8',
                      'bKf1','bKf2','bKf3','bKf4','bKf5','bKf6','bKf7','bKf8',
                      'bKg1','bKg2','bKg3','bKg4','bKg5','bKg6','bKg7','bKg8',
                      'bKh1','bKh2','bKh3','bKh4','bKh5','bKh6','bKh7','bKh8',}

    app.wQueenMoves = {'wQa1','wQa2','wQa3','wQa4','wQa5','wQa6','wQa7','wQa8',
                     'wQb1','wQb2','wQb3','wQb4','wQb5','wQb6','wQb7','wQb8',
                     'wQc1','wQc2','wQc3','wQc4','wQc5','wQc6','wQc7','wQc8',
                     'wQd1','wQd2','wQd3','wQd4','wQd5','wQd6','wQd7','wQd8',
                     'wQe1','wQe2','wQe3','wQe4','wQe5','wQe6','wQe7','wQe8',
                     'wQf1','wQf2','wQf3','wQf4','wQf5','wQf6','wQf7','wQf8',
                     'wQg1','wQg2','wQg3','wQg4','wQg5','wQg6','wQg7','wQg8',
                     'wQh1','wQh2','wQh3','wQh4','wQh5','wQh6','wQh7','wQh8'}
    
    app.bQueenMoves = {'bQa1','bQa2','bQa3','bQa4','bQa5','bQa6','bQa7','bQa8',
                      'bQb1','bQb2','bQb3','bQb4','bQb5','bQb6','bQb7','bQb8',
                      'bQc1','bQc2','bQc3','bQc4','bQc5','bQc6','bQc7','bQc8',
                      'bQd1','bQd2','bQd3','bQd4','bQd5','bQd6','bQd7','bQd8',
                      'bQe1','bQe2','bQe3','bQe4','bQe5','bQe6','bQe7','bQe8',
                      'bQf1','bQf2','bQf3','bQf4','bQf5','bQf6','bQf7','bQf8',
                      'bQg1','bQg2','bQg3','bQg4','bQg5','bQg6','bQg7','bQg8',
                      'bQh1','bQh2','bQh3','bQh4','bQh5','bQh6','bQh7','bQh8',}

    app.wRookMoves = {'wRa1','wRa2','wRa3','wRa4','wRa5','wRa6','wRa7','wRa8',
                     'wRb1','wRb2','wRb3','wRb4','wRb5','wRb6','wRb7','wRb8',
                     'wRc1','wRc2','wRc3','wRc4','wRc5','wRc6','wRc7','wRc8',
                     'wRd1','wRd2','wRd3','wRd4','wRd5','wRd6','wRd7','wRd8',
                     'wRe1','wRe2','wRe3','wRe4','wRe5','wRe6','wRe7','wRe8',
                     'wRf1','wRf2','wRf3','wRf4','wRf5','wRf6','wRf7','wRf8',
                     'wRg1','wRg2','wRg3','wRg4','wRg5','wRg6','wRg7','wRg8',
                     'wRh1','wRh2','wRh3','wRh4','wRh5','wRh6','wRh7','wRh8'}
    
    app.bRookMoves = {'bRa1','bRa2','bRa3','bRa4','bRa5','bRa6','bRa7','bRa8',
                      'bRb1','bRb2','bRb3','bRb4','bRb5','bRb6','bRb7','bRb8',
                      'bRc1','bRc2','bRc3','bRc4','bRc5','bRc6','bRc7','bRc8',
                      'bRd1','bRd2','bRd3','bRd4','bRd5','bRd6','bRd7','bRd8',
                      'bRe1','bRe2','bRe3','bRe4','bRe5','bRe6','bRe7','bRe8',
                      'bRf1','bRf2','bRf3','bRf4','bRf5','bRf6','bRf7','bRf8',
                      'bRg1','bRg2','bRg3','bRg4','bRg5','bRg6','bRg7','bRg8',
                      'bRh1','bRh2','bRh3','bRh4','bRh5','bRh6','bRh7','bRh8',}

    app.wBishopMoves = {'wBa1','wBa2','wBa3','wBa4','wBa5','wBa6','wBa7','wBa8',
                     'wBb1','wBb2','wBb3','wBb4','wBb5','wBb6','wBb7','wBb8',
                     'wBc1','wBc2','wBc3','wBc4','wBc5','wBc6','wBc7','wBc8',
                     'wBd1','wBd2','wBd3','wBd4','wBd5','wBd6','wBd7','wBd8',
                     'wBe1','wBe2','wBe3','wBe4','wBe5','wBe6','wBe7','wBe8',
                     'wBf1','wBf2','wBf3','wBf4','wBf5','wBf6','wBf7','wBf8',
                     'wBg1','wBg2','wBg3','wBg4','wBg5','wBg6','wBg7','wBg8',
                     'wBh1','wBh2','wBh3','wBh4','wBh5','wBh6','wBh7','wBh8'}
    
    app.bBishopMoves = {'bBa1','bBa2','bBa3','bBa4','bBa5','bBa6','bBa7','bBa8',
                      'bBb1','bBb2','bBb3','bBb4','bBb5','bBb6','bBb7','bBb8',
                      'bBc1','bBc2','bBc3','bBc4','bBc5','bBc6','bBc7','bBc8',
                      'bBd1','bBd2','bBd3','bBd4','bBd5','bBd6','bBd7','bBd8',
                      'bBe1','bBe2','bBe3','bBe4','bBe5','bBe6','bBe7','bBe8',
                      'bBf1','bBf2','bBf3','bBf4','bBf5','bBf6','bBf7','bBf8',
                      'bBg1','bBg2','bBg3','bBg4','bBg5','bBg6','bBg7','bBg8',
                      'bBh1','bBh2','bBh3','bBh4','bBh5','bBh6','bBh7','bBh8',}

    app.wKnightMoves = {'wNa1','wNa2','wNa3','wNa4','wNa5','wNa6','wNa7','wNa8',
                     'wNb1','wNb2','wNb3','wNb4','wNb5','wNb6','wNb7','wNb8',
                     'wNc1','wNc2','wNc3','wNc4','wNc5','wNc6','wNc7','wNc8',
                     'wNd1','wNd2','wNd3','wNd4','wNd5','wNd6','wNd7','wNd8',
                     'wNe1','wNe2','wNe3','wNe4','wNe5','wNe6','wNe7','wNe8',
                     'wNf1','wNf2','wNf3','wNf4','wNf5','wNf6','wNf7','wNf8',
                     'wNg1','wNg2','wNg3','wNg4','wNg5','wNg6','wNg7','wNg8',
                     'wNh1','wNh2','wNh3','wNh4','wNh5','wNh6','wNh7','wNh8'}
    
    app.bKnightMoves = {'bNa1','bNa2','bNa3','bNa4','bNa5','bNa6','bNa7','bNa8',
                      'bNb1','bNb2','bNb3','bNb4','bNb5','bNb6','bNb7','bNb8',
                      'bNc1','bNc2','bNc3','bNc4','bNc5','bNc6','bNc7','bNc8',
                      'bNd1','bNd2','bNd3','bNd4','bNd5','bNd6','bNd7','bNd8',
                      'bNe1','bNe2','bNe3','bNe4','bNe5','bNe6','bNe7','bNe8',
                      'bNf1','bNf2','bNf3','bNf4','bNf5','bNf6','bNf7','bNf8',
                      'bNg1','bNg2','bNg3','bNg4','bNg5','bNg6','bNg7','bNg8',
                      'bNh1','bNh2','bNh3','bNh4','bNh5','bNh6','bNh7','bNh8',}

    app.wPawnMoves = {'wa1','wa2','wa3','wa4','wa5','wa6','wa7','wa8',
                     'wb1','wb2','wb3','wb4','wb5','wb6','wb7','wb8',
                     'wc1','wc2','wc3','wc4','wc5','wc6','wc7','wc8',
                     'wd1','wd2','wd3','wd4','wd5','wd6','wd7','wd8',
                     'we1','we2','we3','we4','we5','we6','we7','we8',
                     'wf1','wf2','wf3','wf4','wf5','wf6','wf7','wf8',
                     'wg1','wg2','wg3','wg4','wg5','wg6','wg7','wg8',
                     'wh1','wh2','wh3','wh4','wh5','wh6','wh7','wh8'}
    
    app.bPawnMoves = {'ba1','ba2','ba3','ba4','ba5','ba6','ba7','ba8',
                      'bb1','bb2','bb3','bb4','bb5','bb6','bb7','bb8',
                      'bc1','bc2','bc3','bc4','bc5','bc6','bc7','bc8',
                      'bd1','bd2','bd3','bd4','bd5','bd6','bd7','bd8',
                      'be1','be2','be3','be4','be5','be6','be7','be8',
                      'bf1','bf2','bf3','bf4','bf5','bf6','bf7','bf8',
                      'bg1','bg2','bg3','bg4','bg5','bg6','bg7','bg8',
                      'bh1','bh2','bh3','bh4','bh5','bh6','bh7','bh8',}


    # Legal Moves of AI pieces
    app.allLegalAIPieceMoves = []

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
    newrow,newcol = getCell(app,app.yy,app.xx)
    olerow,olecol = getCell(app,app.y,app.x)
    elementsOfPiece = 0
    if getPieceFromCell(app,olerow,olecol) != 0:
        elementsOfPiece = app.pieces[getPieceFromCell(app,olerow,olecol)]

    for piece in app.pieces:
        if (app.isBlackTurn and piece.isBlackPiece == True) or\
           (not app.isBlackTurn and piece.isBlackPiece == False):
            if piece.position == elementsOfPiece and isInBoard(olerow,olecol):
                if not ((piece == 'wKing' or piece == 'bKing') and abs(newcol - olecol == 2)):
                    piece.position[0] = newrow
                    piece.position[1] = newcol
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == False:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == True:
                    app.isBlackTurn = False
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol):
                    if piece in pawns and piece.isBlackPiece == False and newrow == 0:
                        piece.position[3] = True
                    if piece in pawns and piece.isBlackPiece == True and newrow == 7:
                        piece.position[3] = True
                if not moveIsLegal(app,piece,newrow,newcol,olerow,olecol) or\
                    passedPiece(app,newrow,newcol,olerow,olecol):
                    piece.position[0] = olerow
                    piece.position[1] = olecol

            # Castling
            if piece == 'wKing' and newcol-olecol == 2 and\
                piece.position == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleKingSideWhite(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == False:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == True:
                    app.isBlackTurn = False
                    app.wKingCheck = False
                    app.bKingCheck = False
                if piece == 'wKing':
                    app.canWKingCastle = False
                if piece == 'lWRook':
                    app.canlWRookCastle = False
            elif piece == 'wKing' and newcol-olecol == -2 and\
                piece.position == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleQueenSideWhite(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == False:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if piece == 'wKing':
                    app.canWKingCastle = False
                if piece == 'rWRook':
                    app.canrWRookCastle = False
            if piece == 'bKing' and newcol-olecol == 2 and\
                piece.position == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleKingSideBlack(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == False:
                    app.isBlackTurn = True
                    app.wKingCheck = False
                    app.bKingCheck = False
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == True:
                    app.isBlackTurn = False
                if piece == 'bKing':
                    app.canBKingCastle = False
                if piece == 'lBRook':
                    app.canlWRookCastle = False
            elif piece == 'bKing' and newcol-olecol == -2 and\
                piece.position == elementsOfPiece and isInBoard(olerow,olecol) and\
                moveIsLegal(app, piece, newrow, newcol, olerow, olecol):
                castleQueenSideBlack(app)
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == False:
                    app.isBlackTurn = True
                if moveIsLegal(app,piece,newrow,newcol,olerow,olecol) and piece.isBlackPiece == True:
                    app.isBlackTurn = False
                if piece == 'bKing':
                    app.canBKingCastle = False
                if piece == 'rBRook':
                    app.canrBRookCastle = False
        
            # En Passant
            if piece in pawns and piece.isBlackPiece == True and newrow - olerow == 2:
                if piece.position[0] == newrow and piece.position[1] == newcol:
                    app.blackEnPassantPawn[0] = newrow - 1
                    app.blackEnPassantPawn[1] = newcol
            if piece in pawns and piece.isBlackPiece == False and newrow - olerow == -2:
                if piece.position[0] == newrow and piece.position[1] == newcol:
                    app.whiteEnPassantPawn[0] = newrow + 1
                    app.whiteEnPassantPawn[1] = newcol


    # Pawn Promotion
    for piece in app.pieces:
        if piece.position == elementsOfPiece and isInBoard(olerow,olecol) and piece in pawns:
            if elementsOfPiece[3] and getPieceFromCell(app,olerow,olecol) != 0 and\
                 newrow == 0 and piece.position[0] == newrow and piece.isBlackPiece == False:
                app.pieces[getPieceFromCell(app,olerow,olecol)][2] = '\u2655' 
            if elementsOfPiece[3] and getPieceFromCell(app,olerow,olecol) != 0 and\
                 piece.position[0] == 7 and piece.isBlackPiece == True:
                app.pieces[getPieceFromCell(app,olerow,olecol)][2] = '\u265B'

def passedPiece(app,newrow,newcol,olerow,olecol):
    for piece in app.pieces:
        # rows and columns
        if piece.position[0] > newrow and piece.position[1] == newcol and\
            piece.position[0] < olerow and newcol == olecol:
            return True
        if piece.position[0] < newrow and piece.position[1] == newcol and\
            piece.position[0] > olerow and newcol == olecol:
            return True
        if piece.position[1] < newcol and piece.position[0] == newrow and\
            piece.position[1] > olecol and newrow == olerow:
            return True
        if piece.position[1] > newcol and piece.position[0] == newrow and\
            piece.position[1] < olecol and newrow == olerow:
            return True
        # diagonals
        # Right Down
        if abs(newrow - piece.position[0]) == abs(newcol - piece.position[1]) and\
             abs(olerow - piece.position[0]) == abs(olecol - piece.position[1]) and\
             olecol < piece.position[1] and olerow > piece.position[0] and\
             newcol > piece.position[1] and newrow < piece.position[0]:
             return True
        # Right Up
        if newrow - piece.position[0] == newcol - piece.position[1] and\
             olerow - piece.position[0] == olecol - piece.position[1] and\
             olecol < piece.position[1] and olerow < piece.position[0] and\
             newcol > piece.position[1] and newrow > piece.position[0]:
             return True
        # Left Down
        if newrow - piece.position[0] == newcol - piece.position[1] and\
             olerow - piece.position[0] == olecol - piece.position[1] and\
             olecol > piece.position[1] and olerow > piece.position[0] and\
             newcol < piece.position[1] and newrow < piece.position[0]:
             return True
        # Left Up
        if abs(newrow - piece.position[0]) == abs(newcol - piece.position[1]) and\
             abs(olerow - piece.position[0]) == abs(olecol - piece.position[1]) and\
             olecol > piece.position[1] and olerow < piece.position[0] and\
             newcol < piece.position[1] and newrow > piece.position[0]:
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
        if piece.isBlackPiece == True and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.blackPieces or\
            piece.isBlackPiece == False and getPieceFromCell(app,newrow,newcol) != piece and\
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

        if piece.isBlackPiece == True and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.whitePieces or\
            piece.isBlackPiece == False and getPieceFromCell(app,newrow,newcol) != piece and\
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

        if piece.isBlackPiece == True and getPieceFromCell(app,newrow,newcol) != piece and\
            getPieceFromCell(app,newrow,newcol) in app.blackPieces or\
            piece.isBlackPiece == False and getPieceFromCell(app,newrow,newcol) != piece and\
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
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in pawns and (piece != 0 and (piece.position[2] == '\u265B' or piece.position[2] == '\u2655')) and\
             ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow)) or\
            (newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in knights and\
            ((abs(newcol - olecol) == 2 and abs(newrow - olerow) == 1) or\
            (abs(newcol - olecol) == 1 and abs(newrow - olerow) == 2)):
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in bishops and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newcol - olecol == newrow - olerow) or\
            (newcol - olecol == -(newrow - olerow))):
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in rooks and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            ((newrow - olerow == 0) or\
            (newcol - olecol == 0)):
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in pawns and piece.isBlackPiece == True and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            (((newrow - olerow) == 1 and olecol - newcol == 0 and\
            getWhitePieceFromCell(app,newrow,newcol) not in app.whitePieces) or\
            (olerow == 1 and (newrow - olerow) == 2 and olecol - newcol == 0 and\
            getWhitePieceFromCell(app,newrow,newcol) not in app.whitePieces) or\
            (getPieceFromCell(app,newrow,newcol) != 0 and\
            getWhitePieceFromCell(app,newrow,newcol) in app.whitePieces and\
            (newrow - olerow) == 1 and abs(olecol - newcol) == 1)):
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        elif piece in pawns and piece.isBlackPiece == False and ((newrow,newcol) not in app.afterPieceRowColDiag) and\
            (((newrow - olerow) == -1 and olecol - newcol == 0 and\
            getBlackPieceFromCell(app,newrow,newcol) not in app.blackPieces) or\
            (olerow == 6 and (newrow - olerow) == -2 and olecol - newcol == 0 and\
            getBlackPieceFromCell(app,newrow,newcol) not in app.blackPieces) or\
            (getPieceFromCell(app,newrow,newcol) != 0 and\
            getBlackPieceFromCell(app,newrow,newcol) in app.blackPieces and\
            (newrow - olerow) == -1 and abs(olecol - newcol) == 1)):
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        if piece in pawns and piece.isBlackPiece == False and\
            ((newrow - olerow) == -1 and abs(olecol - newcol) == 1) and\
            getBlackPieceFromCell(app,newrow,newcol) == app.blackEnPassantPawn:
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True
        if piece in pawns and piece.isBlackPiece == True and\
            ((newrow - olerow) == 1 and abs(olecol - newcol) == 1) and\
            getWhitePieceFromCell(app,newrow,newcol) == app.whiteEnPassantPawn:
            if app.wKingCheck and piece.isBlackPiece == False and not app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif app.bKingCheck and piece.isBlackPiece == True and app.isBlackTurn and\
               (newrow,newcol) in app.illegalKingMoves:
               return True
            elif not (app.bKingCheck or app.wKingCheck):
                return True

def pawnPromotion(app,piece):
    piece.position[3] = True
    if piece.isBlackPiece == False:
        piece.position[2] = '\u2655'
    elif piece.isBlackPiece == True:
        piece.position[2] = '\u265B'

def selectPiece(app):
    if getCell(app,app.y,app.x) == getCell(app,app.yy,app.xx):
        row,col = getCell(app,app.y,app.x)
        if getPieceFromCell(app,row,col) != 0:
            return True

def showPossibleMoves(app,pieceRow,pieceCol):
    app.blueRowCol = [(pieceRow,pieceCol)]
    piece = getPieceFromCell(app,pieceRow,pieceCol)
    if getPieceFromCell(app,pieceRow,pieceCol) != 0:
        olerow = piece.position[0]
        olecol = piece.position[1]
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
        olerow = piece.position[0]
        olecol = piece.position[1]
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
        if piece.position[0] == row and piece.position[1] == col:
            thePiece = piece
    return thePiece

def getCell(app,y,x):
    row = int(((y-app.margin)/(app.height - 2*app.margin)*app.rows))
    col = int(((x-app.margin)/(app.width - 2*app.margin)*app.cols))
    return row,col

def getPieceCoords(app,piece):
    # gets coordinates of Pieces
    x = app.margin + piece.position[1]*app.cellSize + app.cellSize/2
    y = app.margin + piece.position[piece][0]*app.cellSize + app.cellSize/2
    return x,y

def getCellBounds(app,row,col):
    # gets cell bounds
    x0 = app.margin + app.cellSize*col
    y0 = app.margin + app.cellSize*row
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    return x0,y0,x1,y1


########## Legal Moves For Pieces ###########
def legalKnightMoves(app):
    moves = [(2,1),(1,2),(2,-1),(-1,2),(-2,1),(1,-2),(-2,-1),(-1,-2)]
    for knight in app.knights:
        for move in moves:
            if isInBoard(knight.position[0]+move[0],knight.position[1]+move[1]) and\
                :
                if knight in app.blackPieces:





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
                if piece.isBlackPiece == False:
                    legalWhiteMoves += len(legalMove[1])
                elif piece.isBlackPiece == True:
                    legalBlackMoves += len(legalMove[1])
            if legalMove[0] == piece and\
                (pieces[piece][0],pieces[piece][1]) in legalMove[1]:
                legalMoveSet = set(legalMove[1])
                list(legalMoveSet)
                legalMoveSet.remove((pieces[piece][0],pieces[piece][1]))
                if piece.isBlackPiece == False:
                    legalWhiteMoves += len(legalMoveSet)
                elif piece.isBlackPiece == True:
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
    # Draws the pieces 
    for piece in app.pieces:
        x,y = getPieceCoords(app,piece)
        canvas.create_text(x,y,text = piece.character,font = f'Arial {int(app.pieceSize)} bold')

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
        pieceLocations.append((piece.position[0],piece.position[1]))

    for row in range(app.rows):
        for col in range(app.cols):
            if (row,col) in pieceLocations:
                piecePositionInList = pieceLocations.index((row,col))
                piece = app.pieceNames[piecePositionInList]
                print(piece.position[2],end='  ')
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