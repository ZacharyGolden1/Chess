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
# rook   kinght bishop king   queen  bishop knight rook
# 000000 000001 000010 000011 000100 000101 000110 000111   0  1  2  3  4  5  6  7 
# 001000 001001 001010 001011 001100 001101 001110 001111   8  9  10 11 12 13 14 15 
# 010000 010001 010010 010011 010100 010101 010110 010111   16 17 18 19 20 21 22 23
# 011000 011001 011010 011011 011100 011101 011110 011111   24 25 26 27 28 29 30 31
# 100000 100001 100010 100011 100100 100101 100110 100111   32 33 34 35 36 37 38 39
# 101000 101001 101010 101011 101100 101101 101110 101111   40 41 42 43 44 45 46 47
# 110000 110001 110010 110011 110100 110101 110110 110111   48 49 50 51 52 53 54 55
# 111000 111001 111010 111011 111100 111101 111110 111111   56 57 58 59 60 61 62 63
# rook   kinght bishop king   queen  bishop knight rook

class Pieces:
        board = dict.fromkeys(["pawns","rooks","knights","bishops","queens","kings"])
                   #white
        pawns  =  [0b10011001000000,0b10011001001000,0b10011001010000,0b10011001011000,
                   0b10011001100000,0b10011001101000,0b10011001110000,0b10011001111000,
                   #black
                   0b10010110000000,0b10010110001000,0b10010110010000,0b10010110011000,
                   0b10010110100000,0b10010110101000,0b10010110110000,0b10010110111000]
        rooks   = [0b10101000000000,0b10101000111000,0b10100111000000,0b10100111111000]
        knights = [0b10111000001000,0b10111000110000,0b10110111001000,0b10110111110000]
        bishops = [0b11001000010000,0b11001000101000,0b11000111010000,0b11000111101000]
        kings   = [0b11011000011000,0b11010111011000]
        queens  = [0b11101000100000,0b11100111100000]

        def initBoard(self):
                self.board["pawns"]   = self.pawns
                self.board["rooks"]   = self.rooks
                self.board["knights"] = self.knights
                self.board["bishops"] = self.bishops
                self.board["kings"]   = self.kings
                self.board["queens"]  = self.queens

                return self.board

class Info:
        def name(self,pc):
                return (pc >> 9) & 0b01111
        
        def position(self,pc):
                return (pc >> 3) & 0b0000111111
        
        def state(self,pc):
                return pc & 0b000000000000111

class Play:
        board = Pieces.board
        pcs = list(board.values())
        def getMoves(self, pcs):
                for pc in pcs:
                        pass
                return




