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
# Chess 2.0:

# optimize for speed so the A.I. algorithm can run as fast as possible:
# best way to represent the board: dictionary of strings for each piece
# dict input is a 16-bit number
# first 3 bits represent the piece:
# 001 - pawn
# 010 - rook
# 011 - knight
# 100 - bishop
# 101 - queen
# 110 - king

# next a bit for which color the piece is
# 0 for black
# 1 for white

# next include four more bits:
# pawns rooks and kings will utilize these bits for their respective
# special moves:

# For pawns:
# the next bit will represent whether or not the piece
# has been promoted
# 0 for no
# 1 for yes

# the next two bits for the pawn will represent 
# what piece it has been promoted to
# 01 for rook
# 10 for knight
# 11 for bishop
# 10 for queen

# the last bit for the pawn will represent whether or not it can 
# En Passant on the current move
# 0 for no
# 1 for yes
