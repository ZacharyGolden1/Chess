# Step1:  make the board                     -- 
# Step2:  make the pieces                    -- 
# Step3:  create movement                    -- 
# Step4:  check general legality of movement -- 
# Step5:  color possible board moves         -- 
# Step6:  create piece capturing             --  
# Step7:  create castling/En Passant         -- 
# Step8:  detect checks and checkmates       -- 
# Step9:  create A.I. to play against        --  
# Step10: Allow for pawn promotion           --  
# Step11: create turns                       -- 
############ Minimum needed for MVP ################
# Step12: flip the board                     --
# Step13: implement gameover/restart         -- 
# Step14: title screen other UI stuff        -- 
# Step15: immplement different gamemodes     -- 

###################################################
################### VERSIONS ######################
###################################################

# For reference
#       0     1      2     3       4      5      6     7   
#    rook   kinght bishop king   queen  bishop knight rook
# 0  000000 000001 000010 000011 000100 000101 000110 000111   0  1  2  3  4  5  6  7 
# 1  001000 001001 001010 001011 001100 001101 001110 001111   8  9  10 11 12 13 14 15 
# 2  010000 010001 010010 010011 010100 010101 010110 010111   16 17 18 19 20 21 22 23
# 3  011000 011001 011010 011011 011100 011101 011110 011111   24 25 26 27 28 29 30 31
# 4  100000 100001 100010 100011 100100 100101 100110 100111   32 33 34 35 36 37 38 39
# 5  101000 101001 101010 101011 101100 101101 101110 101111   40 41 42 43 44 45 46 47
# 6  110000 110001 110010 110011 110100 110101 110110 110111   48 49 50 51 52 53 54 55
# 7  111000 111001 111010 111011 111100 111101 111110 111111   56 57 58 59 60 61 62 63
#    rook   kinght bishop king   queen  bishop knight rook

class Pieces:
        plr = 1
        dboard = dict.fromkeys(["pawns","rooks","knights","bishops","queens","kings"])
        lboard = list()
        sboard = set()
                   #white
        pawns  =  [0b10001001000000,0b10001001001000,0b10001001010000,0b10001001011000,
                   0b10001001100000,0b10001001101000,0b10001001110000,0b10001001111000,
                   #black
                   0b10000110000000,0b10000110001000,0b10000110010000,0b10000110011000,
                   0b10000110100000,0b10000110101000,0b10000110110000,0b10000110111000]
        rooks   = [0b10101000000001,0b10101000111001,0b10100111000001,0b10100111111001]
        knights = [0b10111000001000,0b10111000110000,0b10110111001000,0b10110111110000]
        bishops = [0b11001000010000,0b11001000101000,0b11000111010000,0b11000111101000]
        kings   = [0b11011000011001,0b11010111011001]
        queens  = [0b11101000100000,0b11100111100000]

        

        def __init__(self):
                self.dboard["pawns"]   = self.pawns
                self.dboard["rooks"]   = self.rooks
                self.dboard["knights"] = self.knights
                self.dboard["bishops"] = self.bishops
                self.dboard["kings"]   = self.kings
                self.dboard["queens"]  = self.queens

                self.lboard.append(self.pawns,self.rooks,self.knights,
                                   self.bishops,self.kings,self.queens)
                
                for pc in self.lboard:
                        self.sboard.add(pc)

class Update:
        def newPosition(self, pc, pos):
                return (pc & 0b11110000001111) + (pos << 4)

class Info:
        def square(self, pc):
                sq = ""
                if self.col(self, pc) == 1:
                        sq + "a" + str(self.row(self,pc))
                if self.col(self, pc) == 2:
                        sq + "b" + str(self.row(self,pc))
                if self.col(self, pc) == 3:
                        sq + "c" + str(self.row(self,pc))
                if self.col(self, pc) == 4:
                        sq + "d" + str(self.row(self,pc))
                if self.col(self, pc) == 5:
                        sq + "e" + str(self.row(self,pc))
                if self.col(self, pc) == 6:
                        sq + "f" + str(self.row(self,pc))
                if self.col(self, pc) == 7:
                        sq + "g" + str(self.row(self,pc))
                if self.col(self, pc) == 8:
                        sq + "h" + str(self.row(self,pc))
                return sq

        def asciiChar(self,pc):
                # pawns
                if (self.name(self,pc) == 0b001 and 
                    self.color(self,pc) == 1):
                        return '\u2659'
                elif (self.name(self,pc) == 0b001 and 
                    self.color(self,pc) == 0):
                        return '\u265F'
                # rooks
                elif (self.name(self,pc) == 0b010 and 
                    self.color(self,pc) == 1):
                        return '\u2656'
                elif (self.name(self,pc) == 0b010 and 
                    self.color(self,pc) == 0):
                        return '\u265C'
                # knights
                elif (self.name(self,pc) == 0b011 and 
                    self.color(self,pc) == 1):
                        return '\u2658'
                elif (self.name(self,pc) == 0b011 and 
                    self.color(self,pc) == 0):
                        return '\u265E'
                # bishops
                elif (self.name(self,pc) == 0b100 and 
                    self.color(self,pc) == 1):
                        return '\u2656'
                elif (self.name(self,pc) == 0b100 and 
                    self.color(self,pc) == 0):
                        return '\u265D'
                # queens
                elif (self.name(self,pc) == 0b101 and 
                    self.color(self,pc) == 1):
                        return '\u2655'
                elif (self.name(self,pc) == 0b101 and 
                    self.color(self,pc) == 0):
                        return '\u265B'
                # kings
                elif (self.name(self,pc) == 0b110 and 
                    self.color(self,pc) == 1):
                        return '\u2654'
                elif (self.name(self,pc) == 0b110 and 
                    self.color(self,pc) == 0):
                        return '\u265A'

        def name(self,pc):
                return (pc >> 10) & 0b0111

        def color(self,pc):
                return (pc >> 10) & 0b00001
        
        def position(self,pc):
                return (pc >> 3) & 0b0000111111
        
        def state(self,pc):
                return pc & 0b000000000000111
        
        def active(self,pc):
                return pc >> 13
        
        def row(self, pc):
                return (self.position(self, pc) & 0b111000) >> 3
        
        def col(self, pc):
                return self.position(self, pc) % 8
        
        def positionColor(self,pc):
                return (self.position(self, pc) << 1) + self.color(self,pc)

class Heuristic:
        def boardWorth (self,board: dict):
                return

class Play:
        def move(self, mv : str):
                return

class GenerateMoves:
        # current board at this move
        UIboard = Pieces.dboard
        AIboard = Pieces.sboard
        board   = Pieces.lboard
        plr     = Pieces.plr
        positions = set()
        for pc in Pieces.lboard:
                positions.append(Info.position(Info, pc))
        moves = set()

        def getMovesFromBoard(self,pc,board : list):
                for pc in board:
                        # white pawn
                        if ((Info.name(Info, pc) == 0b001 or Info.name(Info, pc) == 0b000) and
                             Info.color(Info, pc) == 1):
                                if (Info.name(Info, pc) == 0b000 and 
                                   Info.position(Info, pc) - 16 not in self.positions):
                                        self.moves.add("p" + Info.square(Info, Update.newPosition(Update, pc, (Info.position(Info, pc) - 16))))
                                elif (Info.name(Info, pc) == 0b001 and 
                                   Info.position(Info, pc) - 8 not in self.positions):
                                        self.moves.add("p" + Info.square(Info, Update.newPosition(Update, pc, (Info.position(Info, pc) - 8))))
                        # black pawn
                        if ((Info.name(pc) == 0b001 or Info.name(Info, pc) == 0b000) and 
                             Info.color == 0):
                                if (Info.name(Info, pc) == 0b000 and 
                                   Info.position(Info, pc) + 16 not in self.positions):
                                        self.moves.add("p" + Info.square(Info, Update.newPosition(Update, pc, (Info.position(Info, pc) + 16))))
                                elif (Info.name(Info, pc) == 0b001 and 
                                   Info.position(Info, pc) + 8 not in self.positions):
                                        self.moves.add("p" + Info.square(Info, Update.newPosition(Update, pc, (Info.position(Info, pc) + 8))))
                        # white rook
                        if Info.name(pc) == 0b010 and Info.color == 1:
                                pass
                        # black rook
                        if Info.name(pc) == 0b010 and Info.color == 0:
                                pass
                        # white knight
                        if Info.name(pc) == 0b001:
                                pass
                        # black knight
                        if Info.name(pc) == 0b001:
                                pass
                        # white bishop
                        if Info.name(pc) == 0b001:
                                pass
                        # black bishop
                        if Info.name(pc) == 0b001:
                                pass
                        # white queen
                        if Info.name(pc) == 0b001:
                                pass
                        # black queen
                        if Info.name(pc) == 0b001:
                                pass
                        # white king
                        if Info.name(pc) == 0b001:
                                pass
                        # black king
                        if Info.name(pc) == 0b001:
                                pass
                return # list of all sets of moves

        def getMoves(self, board, plr):
                newBoards = dict()
                mv = 0
                for pc in board:
                        if Info.color(pc) == plr:
                                newBoards.update({mv : self.makeMove(pc,board)})
                        mv += 1
                return newBoards

class TerminalUI:
        def showTBoard(self, board: set):
                pcLocs = dict()
                b = list()

                for key in board:
                        for el in board[key]:
                                b.append(el)

                for pc in b:
                        pcLocs.update({pc : (Info.row(Info, pc), Info.col(Info, pc))} )
                
                chck = False
                for row in range(8):
                        for col in range(8):
                                chck = False
                                for pc in pcLocs:
                                        if pcLocs[pc] == (row,col):
                                                print(Info.asciiChar(Info, pc),end='  ')
                                                chck = True

                                if col == 7:
                                        if chck == False:
                                                print('.',end='  ')
                                        print(f'{row+1}\n')
                                elif chck == False:
                                        print('.',end='  ')

                print('A  B  C  D  E  F  G  H')

class Tstart:
        def start(self,board):
                TerminalUI.showTBoard(TerminalUI, board)

class TkinterUI:
        def showUIBoard(self,board):
                return

class MinimaxAB:
        depth = 0
        # boards = Play.getMoves(Play, Play.board, Pieces.plr)
        def minimax(self,depth,boards):
                return
        
        def mini(self):
                return
        
        def maxi(self):
                return

# test
# Pieces.initBoard
# Tstart.start(Tstart, Pieces.board)
# c = Pieces()
# TerminalUI.showTBoard(TerminalUI, Pieces.board)