from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self, gametiles):
        # Initialize material and positional values to zero
        material_value = 0
        positional_value = 0
        development_value = 0

        # Define bonuses and penalties for piece development
        development_bonuses = {
            'N': 30,  # Bonus for developing a knight
            'B': 30,  # Bonus for developing a bishop 
        }
        
        # Squares considered effective for piece development
        effective_squares = {
            'N': [(2, 2), (2, 5), (5, 2), (5, 5)],  # Good squares for knights
            'B': [(2, 2), (2, 5), (5, 2), (5, 5)],  # Good squares for bishops 
        }

        # Penalty for unnecessary pawn moves
        pawn_move_penalty = -10
        
        # Initialize king safety values to zero
        white_king_safety = 0
        black_king_safety = 0

        # Endgame evaluation adjustments
        endgame_value = 0

        # Pawn structure evaluation
        pawn_structure_value = 0

        # Tactical themes evaluation
        tactical_value = 0

        # Define some basic bonuses for tactical opportunitieS
        fork_bonus = 30
        pin_bonus = 20

        # Define some basic penalties or bonuses for pawn structure
        doubled_pawn_penalty = -20
        isolated_pawn_penalty = -20
        passed_pawn_bonus = 30

        # Additional evaluation for opening principles
        opening_bonus = 0

        # Control of center squares (D4, D5, E4, E5)
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        center_control_value = 0
        
        # Values for control of each center square
        center_control_bonus = {
        'P': 20, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 0,
        'p': 20, 'n': 30, 'b': 30, 'r': 50, 'q': 90, 'k': 0
        }

        # Dictionary containing the material value of each piece type
        piece_values = {
            'P': -100, 'N': -320, 'B': -330, 'R': -500, 'Q': -900, 'K': -20000,
            'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000
        }
        # Positional values for pawn
        pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        # Positional values for knight
        knight_table = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]
        # Positional values for bishop
        bishop_table = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]
        # Positional values for rook    
        rook_table = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        # Posititonal values for queen
        queen_table = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]
        # Positional values for kings 
        king_table = [
        20, 30, 10, 0, 0, 10, 30, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30 ]

        king_activity_table = [
        -50, -40, -30, -20, -20, -30, -40, -50,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -20, -10, 0, 0, -10, -20, -30,
        -50, -40, -30, -20, -20, -30, -40, -50 ]

        passed_pawn_bonus = 50
        connected_passed_pawn_bonus = 30

        king_activity_score = 0
        pawn_structure_score = 0

        # Find the king's position
        king_position = self.find_king_position(gametiles) 
    
        # Evaluate king safety
        king_safety_value = self.calculate_king_safety(gametiles, king_position)
    

        for y in range(8):
            for x in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
    
                # King activity
                if piece == 'k':
                    king_activity_score += king_activity_table[y * 8 + x]
                elif piece == 'K':
                    king_activity_score -= king_activity_table[(7 - y) * 8 + x]
    
                # Pawn structure
                if piece in ['p', 'P']:
                    # Check for passed pawns
                    is_passed = True
                    for opponent_y in range(8):
                        opponent_piece = gametiles[opponent_y][x].pieceonTile.tostring()
                        if (piece == 'p' and opponent_piece == 'P') or (piece == 'P' and opponent_piece == 'p'):
                            is_passed = False
                            break
                    if is_passed:
                        pawn_structure_score += passed_pawn_bonus
                        # Check for connected passed pawns
                        for adj_x in range(max(0, x - 1), min(8, x + 2)):
                            adjacent_piece = gametiles[y][adj_x].pieceonTile.tostring()
                            if adjacent_piece == piece:
                                pawn_structure_score += connected_passed_pawn_bonus
    
    
        for square in center_squares:
            x, y = square
            piece = gametiles[y][x].pieceonTile.tostring()
    
            # Add or subtract the control value for the piece occupying the center
            if piece in center_control_bonus:
                center_control_value += center_control_bonus[piece] if piece.islower() else -center_control_bonus[piece]

        # Control the center (e4, d4, e5, d5)
        for square in center_squares:
            piece = gametiles[square[1]][square[0]].pieceonTile.tostring()
            if piece.lower() in ['p', 'n', 'b', 'q']:
                opening_bonus += 10

         # Loop over all tiles in the game board
        for y in range(8):
            for x in range(8):
                # Get the piece on the current tile as a string
                piece = gametiles[y][x].get_piece()
                
                # Evaluate piece development
                if piece in ['N', 'B']:  # Only considering knights and bishops for this example
                    if (x, y) in effective_squares[piece]:
                        development_value += development_bonuses[piece]
                
                # Evaluate pawn moves
                if piece == 'P' and y != 6:  # Assuming white pawns start on row 6
                    development_value += pawn_move_penalty

        

        # Development of knights and bishops
        for y in [0, 7]:
            for x in [1, 2, 5, 6]:
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece.lower() in ['n', 'b'] and not gametiles[y][x].is_piece_initial():
                    opening_bonus += 20

        # King safety (castling)
        for y in [0, 7]:
            if gametiles[y][4].pieceonTile.tostring().lower() == 'k' and not gametiles[y][4].is_piece_initial():
                opening_bonus += 30


        # Check for doubled, isolated, and passed pawns
        for x in range(8):
            col_pawns = [gametiles[y][x].pieceonTile.tostring() for y in range(8)]
            num_pawns = col_pawns.count('P') + col_pawns.count('p')
    
            # Doubled pawns (more than one pawn in a file)
            if num_pawns > 1:
                pawn_structure_value += doubled_pawn_penalty * (num_pawns - 1)
    
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
    
                if piece.lower() == 'p':
                    # Isolated pawns (no friendly pawns on adjacent files)
                    if (x == 0 or 'p' not in [gametiles[y][x-1].pieceonTile.tostring() for y in range(8)]) and \
                       (x == 7 or 'p' not in [gametiles[y][x+1].pieceonTile.tostring() for y in range(8)]):
                        pawn_structure_value += isolated_pawn_penalty if piece.islower() else -isolated_pawn_penalty
    
                    # Passed pawns (no opposing pawns ahead on the same or adjacent files)
                    opposing_pawns_ahead = False
                    for ahead_y in range(y+1, 8) if piece.islower() else range(y-1, -1, -1):
                        if 'P' in [gametiles[ahead_y][file].pieceonTile.tostring() for file in range(max(0, x-1), min(7, x+1) + 1)]:
                            opposing_pawns_ahead = True
                            break
    
                    if not opposing_pawns_ahead:
                        pawn_structure_value += passed_pawn_bonus if piece.islower() else -passed_pawn_bonus


        # Loop over all tiles in the game board
        for y in range(8):
            for x in range(8):
                # Get the piece on the current tile as a string
                piece = gametiles[y][x].pieceonTile.tostring()
                
                # If the piece is black (lowercase), add its positional value from the respective table
                if piece.islower():
                    positional_value += pawn_table[(7-y)*8+x] if piece == 'p' else 0
                    positional_value += knight_table[(7-y)*8+x] if piece == 'n' else 0
                    positional_value += bishop_table[(7-y)*8+x] if piece == 'b' else 0
                    positional_value += rook_table[(7-y)*8+x] if piece == 'r' else 0
                    positional_value += queen_table[(7-y)*8+x] if piece == 'q' else 0
                    positional_value += king_table[(7-y)*8+x] if piece == 'k' else 0

                # If the piece is white (uppercase), subtract its positional value from the respective table
                elif piece.isupper():
                    positional_value -= pawn_table[y*8+x] if piece == 'P' else 0
                    positional_value -= knight_table[y*8+x] if piece == 'N' else 0
                    positional_value -= bishop_table[y*8+x] if piece == 'B' else 0
                    positional_value -= rook_table[y*8+x] if piece == 'R' else 0
                    positional_value -= queen_table[y*8+x] if piece == 'Q' else 0
                    positional_value -= king_table[y*8+x] if piece == 'K' else 0
                    
                # Add or subtract the material value of the piece, if it exists in the dictionary
                if piece in piece_values:
                    material_value += piece_values[piece]

                # Check if the piece is a king and evaluate its safety
                if piece == 'k':
                    black_king_safety = evaluate_pawn_shield(gametiles, x, y, 'black')
                elif piece == 'K':
                    white_king_safety = evaluate_pawn_shield(gametiles, x, y, 'white')

        # Check for forks and pins
        for y in range(8):
            for x in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece.lower() in ['n', 'q', 'r', 'b']:  # Pieces capable of forks or pins
                    piece_is_white = piece.isupper()
                    
                    # Check for forks (a piece attacks two or more valuable enemy pieces)
                    attacked_squares = self.get_attacked_squares(x, y, gametiles)
                    enemy_pieces_attacked = [gametiles[ay][ax].pieceonTile.tostring() for ax, ay in attacked_squares if gametiles[ay][ax].pieceonTile.tostring().isupper() != piece_is_white and gametiles[ay][ax].pieceonTile.tostring() != '']
                    if len(enemy_pieces_attacked) >= 2:
                        tactical_value += fork_bonus if piece_is_white else -fork_bonus
    
                    # Check for pins (an enemy piece cannot move without exposing a more valuable piece)
                    # This is a simplified version that only checks for direct lines of attack
                    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
                    for dx, dy in directions:
                        pinned_piece = None
                        pinning_piece = None
                        for i in range(1, 8):
                            nx, ny = x + dx * i, y + dy * i
                            if 0 <= nx < 8 and 0 <= ny < 8:
                                current_piece = gametiles[ny][nx].pieceonTile.tostring()
                                if current_piece != '':
                                    if pinned_piece is None and current_piece.isupper() != piece_is_white:
                                        pinned_piece = (nx, ny)
                                    elif pinned_piece and current_piece.isupper() == piece_is_white:
                                        pinning_piece = (nx, ny)
                                        break
                                    else:
                                        break
                        if pinned_piece and pinning_piece:
                            tactical_value += pin_bonus if piece_is_white else -pin_bonus

        # Adjustments based on the reduced number of pieces 
        if self.is_endgame(gametiles):
            for y in range(8):
                for x in range(8):
                    piece = gametiles[y][x].pieceonTile.tostring()
    
                    # King activity in the endgame is important
                    if piece == 'k':
                        endgame_value += self.king_endgame_table[(7-y)*8+x]
                    elif piece == 'K':
                        endgame_value -= self.king_endgame_table[y*8+x]
                    
                    # Encourage pawns to advance in the endgame
                    if piece == 'p':
                        endgame_value += (7-y) * 10
                    elif piece == 'P':
                        endgame_value -= y * 10
                        


        # Adjust the total evaluation based on king safety
        total_evaluation = material_value + positional_value + center_control_value + pawn_structure_value + tactical_value + endgame_value + king_activity_score + pawn_structure_score + opening_bonus + development_value + king_safety_value
 
                    
        # Return the negative of the evaluation if playing as black
        return total_evaluation
    
    def find_king_position(self, gametiles):
        for y in range(8):
            for x in range(8):
                if gametiles[y][x].pieceonTile.tostring() == 'K':  # Assuming 'K' is the king
                    return (x, y)
        return None  # If the king is not found, which shouldn't happen in a legal chess position

    def calculate_king_safety(self, gametiles, king_position):
        king_safety_score = 0
        
        # Define the squares around the king
        king_zone_offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        # Count defenders and attackers
        defenders = 0
        attackers = 0
        
        for offset in king_zone_offsets:
            x, y = king_position[0] + offset[0], king_position[1] + offset[1]
            # Ensure the square is within the bounds of the board
            if 0 <= x < 8 and 0 <= y < 8:
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece.islower(): # Assuming lower case are your opponent's pieces
                    attackers += 1
                elif piece.isupper(): # Assuming upper case are your pieces
                    defenders += 1
        
        # Calculate safety score based on the number of defenders and attackers
        king_safety_score += (defenders - attackers) * 10
                
        return king_safety_score



    def evaluate_pawn_shield(gametiles, king_x, king_y, color):
        pawn_shield_value = 0
        directions = [-1, 0, 1]
        
        for dx in directions:
            for dy in [-1, 1]:  # Only look ahead of the king
                x, y = king_x + dx, king_y + (dy if color == 'white' else -dy)
                
                if 0 <= x < 8 and 0 <= y < 8:
                    piece_str = gametiles[y][x].pieceonTile.tostring()
                    if (piece_str == 'P' and color == 'white') or (piece_str == 'p' and color == 'black'):
                        pawn_shield_value += 50  # Assign a value for each shielding pawn
    
        return pawn_shield_value

    def is_endgame(self, gametiles):
        # Define conditions for an endgame (e.g., reduced number of pieces)
        piece_count = sum(1 for row in gametiles for tile in row if tile.pieceonTile is not None)
        return piece_count <= 12  #  condition
        king_endgame_table = [
            -50, -40, -30, -20, -20, -30, -40, -50,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -50, -40, -30, -20, -20, -30, -40, -50 ]



    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
