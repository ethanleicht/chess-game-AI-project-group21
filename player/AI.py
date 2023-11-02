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

    def calculate_king_safety(self, gametiles, x, y):
        # Assign a penalty for each open file, open rank, and open diagonal near the king
        open_file_penalty = 20
        open_rank_penalty = 20
        open_diagonal_penalty = 20
        safety_penalty = 0

        # Check for open files (no pawns on the king's file)
        if all(gametiles[i][x].pieceonTile.tostring().lower() != 'p' for i in range(8)):
            safety_penalty += open_file_penalty

        # Check for open ranks (no pawns on the king's rank)
        if all(gametiles[y][i].pieceonTile.tostring().lower() != 'p' for i in range(8)):
            safety_penalty += open_rank_penalty

        # Check for open diagonals (no pawns on the diagonals adjacent to the king)
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            cx, cy = x, y
            while 0 <= cx < 8 and 0 <= cy < 8:
                if gametiles[cy][cx].pieceonTile.tostring().lower() == 'p':
                    break
                cx += dx
                cy += dy
            else:
                safety_penalty += open_diagonal_penalty

        return safety_penalty

    def calculateb(self,gametiles):
        material_value = 0
        positional_value = 0
        king_safety_score = 0
        piece_values = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
                        'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000}

        # Penalties for pawn structure weaknesses
        doubled_pawn_penalty = -20
        isolated_pawn_penalty = -20
        backward_pawn_penalty = -20

        # Control of the center evaluation
        center_control_score = 0
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # D4, D5, E4, E5

        # Positional values for pawn
        pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0 ]
        
        # Positional values for knight
        knight_table = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50 ]
        
        # Positional values for bishop
        bishop_table = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20 ]

        # Positional values for rook    
        rook_table = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0 ]
        # Posititonal values for queen
        queen_table = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20 ]
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

        # Helper function to check if a tile is occupied by a pawn
        def is_pawn(tile):
            # Check if the piece on the tile is a pawn of the specified color
            return tile.pieceonTile.tostring().lower() == 'p'

        def is_controlled_by(tile, gametiles):
            # Find the position of the tile in the gametiles list
            for y, row in enumerate(gametiles):
                for x, current_tile in enumerate(row):
                    if current_tile == tile:
                        # Once we find the tile, we can proceed with the original logic
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                if dx == 0 and dy == 0:
                                    continue
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < 8 and 0 <= ny < 8:
                                    neighbor_piece = gametiles[ny][nx].pieceonTile.tostring()
                                    # Pawn control
                                    if neighbor_piece.isalpha():
                                        if dx in [-1, 1] and neighbor_piece.lower() == 'p' and (
                                                (neighbor_piece.isupper() and dy == -1) or
                                                (neighbor_piece.islower() and dy == 1)):
                                            return 'upper' if neighbor_piece.islower() else 'lower'
                                    # Knight control
                                    if ((abs(dx) == 1 and abs(dy) == 2) or (abs(dx) == 2 and abs(dy) == 1)):
                                        if neighbor_piece.lower() == 'n':
                                            return 'upper' if neighbor_piece.islower() else 'lower'
            return None  # Return None or an appropriate value if the tile is not found

            # Rook control (horizontal and vertical)
            for d in range(-1, 2, 2):
                for nx, ny in [(x + d, y), (x, y + d)]:
                    while 0 <= nx < 8 and 0 <= ny < 8:
                        neighbor_piece = gametiles[ny][nx].pieceonTile.tostring()
                        if neighbor_piece.isalpha():
                            if neighbor_piece.lower() == 'r' or neighbor_piece.lower() == 'q':  # Considering queen as well
                                return 'upper' if neighbor_piece.islower() else 'lower'
                            break  # Blocked by another piece
                        nx, ny = nx + d, ny + d

            # Bishop and queen (diagonal) control
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    neighbor_piece = gametiles[ny][nx].pieceonTile.tostring()
                    if neighbor_piece.isalpha():
                        if neighbor_piece.lower() in ['b', 'q']:  # Bishop or Queen
                            return 'upper' if neighbor_piece.islower() else 'lower'
                        break  # Blocked by another piece
                    nx, ny = nx + dx, ny + dy

            # King control
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        neighbor_piece = gametiles[ny][nx].pieceonTile.tostring()
                        if neighbor_piece.lower() == 'k':
                            return 'upper' if neighbor_piece.islower() else 'lower'

            return None  # Not controlled by any piece

        for x, y in center_squares:
            controlled_by = is_controlled_by(gametiles[y][x], gametiles)
            if controlled_by == 'upper':
                center_control_score -= 10  # Subtract points if controlled by white (uppercase)
            elif controlled_by == 'lower':
                center_control_score += 10  # Add points if controlled by black (lowercase)

        # Loop over all tiles in the game board
        for y in range(8):
            for x in range(8):
                # Get the piece on the current tile as a string
                piece = gametiles[y][x].pieceonTile.tostring()

                if piece in piece_values:
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

                    # Add king safety to the evaluation
                    if piece == 'k':
                        king_safety_score += self.calculate_king_safety(gametiles, x, y)
                    elif piece == 'K':
                        king_safety_score -= self.calculate_king_safety(gametiles, x, y)


                    # Check for doubled pawns (two pawns of the same color on the same file)
                    if is_pawn(gametiles[y][x]) or is_pawn(gametiles[y][x]):
                        for offset in range(y + 1, 8):
                            if is_pawn(gametiles[offset][x]):
                                positional_value += doubled_pawn_penalty if piece.islower() else -doubled_pawn_penalty
                    # Check for isolated pawns (no friendly pawns on adjacent files)
                    if (is_pawn(gametiles[y][x]) or is_pawn(gametiles[y][x])) and \
                            not any(is_pawn(gametiles[y][i]) for i in range(max(0, x - 1), min(8, x + 2)) if i != x):
                         positional_value += isolated_pawn_penalty if piece.islower() else -isolated_pawn_penalty
                    # Check for backward pawns (a pawn that is behind all pawns of the same color on the adjacent files)
                    if (is_pawn(gametiles[y][x]) or is_pawn(gametiles[y][x])):
                        is_backward = True
                        for offset in range(y - 1, -1, -1):
                            if any(is_pawn(gametiles[offset][i]) for i in range(max(0, x - 1), min(8, x + 2))):
                                is_backward = False
                                break
                        if is_backward:
                            positional_value += backward_pawn_penalty if piece.islower() else -backward_pawn_penalty

                    material_value += piece_values[piece]
                
        total_evaluation = material_value + positional_value + king_safety_score #+ center_control_score
        return -total_evaluation


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
























                        
