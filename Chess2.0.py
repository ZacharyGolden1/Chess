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
class pieces:
    board = dict.from_keys(["pawns","rooks","knights","bishops","queens","kings"])
            #white
    pawns  =  {0b1001100100000,0b1001100100100,0b1001100101000,0b1001100101100,
               0b1001100110000,0b1001100110100,0b1001100111000,0b1001100111100,
               #black
               0b1001011000000,0b1001011000100,0b1001011001000,0b1001011001100,
               0b1001011010000,0b1001011010100,0b1001011011000,0b1001011011100}
    rooks   = {0b1010100000000,0b1010100011100,0b1010011100000,0b1010011111100}
    knights = {0b1011100000100,0b1011100011000,0b1011011100100,0b1011011111000}
    bishops = {0b1100100001000,0b1100100010100,0b1100011101000,0b1100011110100}
    kings   = {0b1101100001100,0b1101011101100}
    queens  = {0b1110100010000,0b1110011110000}
