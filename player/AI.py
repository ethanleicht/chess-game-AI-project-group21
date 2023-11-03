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
        piece_value = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000
            }
        positional_value = 0
        value = 0
        king_safety_value = 0
        development_value = 0
        center_control_value = 0
        rook_placement_value = 0
        queen_activity_value = 0
        endgame_value = 0
        central_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # e4, d4, e5, d5
        original_positions = {
            'P': [(x, 1) for x in range(8)],
            'p': [(x, 6) for x in range(8)],
            'N': [(1, 0), (6, 0)],
            'n': [(1, 7), (6, 7)],
            'B': [(2, 0), (5, 0)],
            'b': [(2, 7), (5, 7)],
            }
        bishop_pair_value = 0
        white_bishops = 0
        black_bishops = 0
        

        # Variables for pawn structure evaluation
        white_pawn_files = [0] * 8
        black_pawn_files = [0] * 8
        
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece == 'B':
                    white_bishops += 1
                elif piece == 'b':
                    black_bishops += 1
                if piece in original_positions and (x, y) in original_positions[piece]:
                    # Penalize undeveloped pieces
                    development_value -= 20 if piece.isupper() else 20  
                elif piece and piece.lower() in 'nbp':
                    # Bonus for developed pieces (knights, bishops, pawns)
                    development_value += 40 if piece.isupper() else -40  # Bonus for developed pieces
                if piece and piece in piece_value:
                    # Add material value
                    value += piece_value.get(piece, 0)                    
                    # Add positional values
                    if piece in 'Pp':
                        positional_value += (y * 20) if piece == 'P' else ((7 - y) * 20)
                    elif piece in 'Nn':
                        # Knights are more valuable in the center
                        if 2 <= x <= 5 and 2 <= y <= 5:
                            positional_value += 60 if piece.isupper() else -60
                    elif piece in 'Bb':
                        # Bishops are more valuable when they control long diagonals
                        positional_value += (7 - abs(x - y)) * 20 if piece.isupper() else -(7 - abs(x - y)) * 20
                    elif piece in 'Rr':
                        # Rooks are more valuable on open files or when they are connected
                        is_open_file = all(gametiles[i][x].pieceonTile.tostring() in ' .-' for i in range(8))
                        if is_open_file:
                            positional_value += 50 if piece.isupper() else -50
                    elif piece in 'Qq':
                        # Queens are more powerful when they have mobility
                        mobility = sum(gametiles[i][x].pieceonTile.tostring() in ' .-' for i in range(8))
                        mobility += sum(gametiles[y][j].pieceonTile.tostring() in ' .-' for j in range(8))
                        positional_value += mobility * 10 if piece.isupper() else -mobility * 10
                    elif piece in 'Kk':
                        # Kings are more valuable when they are safe
                        safe_spots = sum(gametiles[i][x].pieceonTile.tostring() in ' .-' for i in range(max(0, y-1), min(7, y+2)))
                        safe_spots += sum(gametiles[y][j].pieceonTile.tostring() in ' .-' for j in range(max(0, x-1), min(7, x+2)))
                        positional_value += safe_spots * 20 if piece.isupper() else -safe_spots * 20
                    # Pawn structure evaluation
                    if piece == 'P':
                        white_pawn_files[x] += 1
                    elif piece == 'p':
                        black_pawn_files[x] += 1
                    # King safety evaluation
                    if piece.lower() == 'k':
                        is_castled = self.is_castled(x, y, gametiles)
                        shielding_pawns = self.count_shielding_pawns(x, y, gametiles, piece.isupper())
                        king_exposed = self.is_king_exposed(x, y, gametiles)
                        # Add or subtract points based on king safety
                        if is_castled:
                            king_safety_value += 100 if piece.isupper() else -100
                        king_safety_value += shielding_pawns * 10 if piece.isupper() else -shielding_pawns * 10
                        if king_exposed:
                            king_safety_value -= 100 if piece.isupper() else 100

        # Bonus for having both bishops
        if white_bishops == 2:
            bishop_pair_value += 40
        if black_bishops == 2:
            bishop_pair_value -= 40
        # Evaluate pawn structure for white
        for x in range(8):
            if white_pawn_files[x] > 1:
                positional_value -= 60 * (white_pawn_files[x] - 1)  # Doubled white pawns penalty
            if white_pawn_files[x] > 0:
                isolated = True
                passed = True
                for adj in range(max(0, x - 1), min(8, x + 2)):  # Check adjacent files
                    if adj != x:
                        if white_pawn_files[adj] > 0:
                            isolated = False
                        if black_pawn_files[adj] > 0:
                            passed = False
                if isolated:
                    positional_value -= 60  # Isolated white pawn penalty
                if passed:
                    positional_value += 120  # Passed white pawn bonus
        
        # Evaluate pawn structure for black
        for x in range(8):
            if black_pawn_files[x] > 1:
                positional_value += 50 * (black_pawn_files[x] - 1)  # Doubled black pawns penalty
            if black_pawn_files[x] > 0:
                isolated = True
                passed = True
                for adj in range(max(0, x - 1), min(8, x + 2)):  # Check adjacent files
                    if adj != x:
                        if black_pawn_files[adj] > 0:
                            isolated = False
                        if white_pawn_files[adj] > 0:
                            passed = False
                if isolated:
                    positional_value += 50  # Isolated black pawn penalty
                if passed:
                    positional_value -= 100  # Passed black pawn bonus

        for x, y in central_squares:
            piece = gametiles[y][x].pieceonTile.tostring()
            if piece:
                # Adjust the value based on the importance of the piece controlling the center
                if piece.lower() in 'pn':
                    control_value = 10
                elif piece.lower() in 'br':
                    control_value = 20
                elif piece.lower() == 'q':
                    control_value = 30
                else:
                    control_value = 0
                
                # Add or subtract points based on which side controls the center
                center_control_value += control_value * 2 if piece.isupper() else -control_value * 2
        for x in range(8):
            has_white_rook = False
            has_black_rook = False
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece == 'R':
                    if not has_white_rook:
                        has_white_rook = True
                        # Rook on open or semi-open file
                        if all(gametiles[i][x].pieceonTile.tostring() in ' .-' for i in range(8) if i != y):
                            rook_placement_value += 50
                    else:
                        # Connected rooks
                        rook_placement_value += 30
                elif piece == 'r':
                    if not has_black_rook:
                        has_black_rook = True
                        # Rook on open or semi-open file
                        if all(gametiles[i][x].pieceonTile.tostring() in ' .-' for i in range(8) if i != y):
                            rook_placement_value -= 50
                    else:
                        # Connected rooks
                        rook_placement_value -= 30
                        
        # Count the number of pieces developed to assess the game stage
        total_pieces_developed = 0
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece in 'NBRnbr':
                    total_pieces_developed += 1

        # Assess the queen's activity based on the game stage
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece == 'Q':
                    # Penalize early queen activity
                    if total_pieces_developed < 6:
                        queen_activity_value -= 20
                elif piece == 'q':
                    # Penalize early queen activity
                    if total_pieces_developed < 6:
                        queen_activity_value += 20

        total_material = 0
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring().lower()
                if piece in 'qrbn':
                    total_material += 1

        # In the endgame, king's centralization and pawn promotion potential become more important
        if total_material <= 8:  # Consider it endgame if there are 8 or fewer pieces on the board
            for x in range(8):
                for y in range(8):
                    piece = gametiles[y][x].pieceonTile.tostring()
                    if piece:
                        if piece.lower() == 'k':
                            # King's centralization is more valuable in the endgame
                            distance_from_center = max(abs(3.5 - x), abs(3.5 - y))
                            endgame_value += (3.5 - distance_from_center) * 40 if piece.isupper() else -(3.5 - distance_from_center) * 40
                        elif piece.lower() == 'p':
                            # Pawn promotion potential becomes more critical
                            distance_to_promotion = 7 - y if piece.isupper() else y
                            endgame_value += (7 - distance_to_promotion) * 20 if piece.isupper() else -(7 - distance_to_promotion) * 20
        # Back-Rank Mate Check
        for y in [0, 7]:
            king_position = next((x for x in range(8) if gametiles[y][x].pieceonTile.tostring().lower() == 'k'), None)
            if king_position is not None:
                back_rank_pieces = [gametiles[y][x].pieceonTile.tostring().lower() for x in range(8)]
                if all(p in 'prnbq.' for p in back_rank_pieces):
                    rook_or_queen_line = [gametiles[i][king_position].pieceonTile.tostring().lower() for i in range(8)]
                    if 'r' in rook_or_queen_line or 'q' in rook_or_queen_line:
                        positional_value += 100 if piece.isupper() else -100  # Large value for checkmate
        # Smothered Mate Check
        for y, x in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            king_position = gametiles[y][x].pieceonTile.tostring().lower() == 'k'
            if king_position:
                surrounding_pieces = [gametiles[i][j].pieceonTile.tostring().lower() for i in range(max(0, y-1), min(7, y+2)) for j in range(max(0, x-1), min(7, x+2))]
                if all(p in 'prnbqk' for p in surrounding_pieces):
                    knight_checks = [gametiles[y + dy][x + dx].pieceonTile.tostring().lower() == 'n' for dx, dy in [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)] if 0 <= x + dx < 8 and 0 <= y + dy < 8]
                    if any(knight_checks):
                        positional_value += 100 if piece.isupper() else -100  # Large value for checkmate

        value += positional_value + king_safety_value + center_control_value + development_value + bishop_pair_value + rook_placement_value + queen_activity_value + endgame_value
        return -value

    def is_castled(self, x, y, gametiles):
        return x == 6 or x == 2

    def count_shielding_pawns(self, x, y, gametiles, is_white):
        pawn_direction = -1 if is_white else 1
        shielding_pawns = 0
        for dx in range(-1, 2):
            nx = x + dx
            ny = y + pawn_direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                if gametiles[ny][nx].pieceonTile.tostring().lower() == ('p' if is_white else 'P'):
                    shielding_pawns += 1
        return shielding_pawns

    def is_king_exposed(self, x, y, gametiles):
        return y in [0, 1, 6, 7] and x in [3, 4]


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
























                        
