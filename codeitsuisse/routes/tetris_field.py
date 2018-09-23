def printMatrix(M):
    h,w = len(M),len(M[0])
    for y in range(h):
        for x in range(w):
            print(M[y][x], end='')
            print("  ", end='')
        print('')

    print('==============================')

def getTopBlk(M,colIdx):
    h=len(M)
    for i in range(h):
        if(M[i][colIdx]==1):
            return i

def clearLines(M):
    h,w = len(M),len(M[0])
    rows_removed = 0
    to_remove = []
    for row in range(h):
        if(not(0 in M[row]) and row!=len(M)-1):
            to_remove.append(row)
            rows_removed+=1

    for i in range(rows_removed):
        del M[to_remove[i]]

    for i in range(rows_removed):
        M.insert(0,[0]*w)

    return M

def addPiece(M,piece,rotate,xpos):
    #create piece profiles
    map = getProfile(piece)

    # update matrix with piece
    #pos = left block pos of piece
    profile_h = len(map)
    profile_w = len(map[0])
    topBlk = getTopBlk(M,xpos)
    y_marker = topBlk - profile_h
    x_marker = xpos

    # update map onto tetris map
    for y in range(profile_h):
        for x in range(profile_w):
            print(x_marker,x)
            print(y_marker,y)
            M[y_marker + y][x_marker + x] = map[y][x]

    return M

def rankRot(M,piece):
    maxScore = 0
    final_pos = 0
    final_rot = 0
    #total score with rot & loc
    if(piece=='J' or piece=='L' or piece=='T'):
        rot = 4
    if(piece=='O'):
        rot = 1
    if(piece=='S' or piece=='Z' or piece=='I'):
        rot = 2

    for i in range(rot):
        (totalScore,pos) = rankLoc(M,piece,i)
        if(totalScore>maxScore):
            maxScore=totalScore
            final_pos=pos
            final_rot=i

    return (final_pos,final_rot)

def rankLoc(M,piece,rotate):
    #analyse any 3 blocks at one time; use relative heights
    #compare contour to profile
    h,w = len(M),len(M[0])
    con = getContour(piece,rotate)
    con_width = len(con)
    # Weights
    wFit = 0.3
    wHeight = 0.7
    scoreFit = 0
    scoreHeight = 0
    maxScore = 0
    #pos with highest score
    pos = 0

    if(con_width==0):
        for i in range(0,w):
            heightScore = getHeightScore(getTopBlk(M,i))
            if(heightScore>maxScore):
                maxScore = heightScore
                pos = i


    if(con_width==1):
        for i in range(0,w-1):
            #rel contour (top profile)
            curr_height = getTopBlk(M,i)
            right_height = getTopBlk(M,i+1)
            rel_con = [right_height-curr_height]

            if(rel_con==con):
                scoreFit = 1
            else:
                scoreFit = 0

            scoreHeight = getHeightScore(getTopBlk(M,i))

            totalScore = wFit*scoreFit + wHeight*scoreHeight
            if(totalScore>maxScore):
                maxScore = totalScore
                pos = i

    if(con_width==2):
        for i in range(0,w-2):
            #rel contour (top profile)
            curr_height = getTopBlk(M,i)
            R_height = getTopBlk(M,i+1)
            RR_height = getTopBlk(M,i+2)
            rel_con = [R_height-curr_height,RR_height-R_height]

            if(rel_con==con):
                scoreFit = 1
            else:
                scoreFit = 0

            scoreHeight = getHeightScore(getTopBlk(M,i))

            totalScore = wFit*scoreFit + wHeight*scoreHeight
            if(totalScore>maxScore):
                maxScore = totalScore
                pos = i

    if(con_width==3):
        for i in range(0,w-3):
            #rel contour (top profile)
            curr_height = getTopBlk(M,i)
            R_height = getTopBlk(M,i+1)
            RR_height = getTopBlk(M,i+2)
            RRR_height = getTopBlk(M,i+3)
            rel_con = [R_height-curr_height,RR_height-R_height,RRR_height-RR_height]

            if(rel_con==con):
                scoreFit = 1
            else:
                scoreFit = 0

            scoreHeight = getHeightScore(getTopBlk(M,i))

            totalScore = wFit*scoreFit + wHeight*scoreHeight
            if(totalScore>maxScore):
                maxScore = totalScore
                pos = i

    return (maxScore,pos)

def getHeightScore(h):
    #the lower the higher score
    return h/20

def getProfile(piece,rotate=0):
    if(piece=='O'):
        map = [[1,1],[1,1]]

    elif(piece=='J'):
        if(rotate == 0):
            map = [[0,1],[0,1],[1,1]]
        elif(rotate == 1):
            map = [[1,1],[0,1],[0,1]]
        elif(rotate == 2):
            map = [[1,1],[1,0],[1,0]]
        else:
            map = [[1,0],[1,0],[1,1]]

    elif(piece=='L'):
        if(rotate == 0):
            map = [[1,0],[1,0],[1,1]]
        elif(rotate == 1):
            map = [[1,1],[1,0],[1,0]]
        elif(rotate == 2):
            map = [[1,1],[0,1],[0,1]]
        else:
            map = [[1,0],[1,0],[1,1]]

    elif(piece=='I'):
        if(rotate == 0 or rotate == 2):
            map = [[1],[1],[1],[1]]
        else:
            map = [1,1,1,1]

    elif(piece=='S'):
        if(rotate == 0 or rotate == 2):
            map = [[0,1,1],[1,1,0]]
        else:
            map = [[1,0],[1,1],[1,0]]

    elif(piece=='T'):
        if(rotate == 0):
            map = [[1,1,1],[0,1,0]]
        elif(rotate == 1):
            map = [[0,1],[1,1],[0,1]]
        elif(rotate == 2):
            map = [[0,1,0],[1,1,1]]
        else:
            map = [[1,0],[1,1],[1,0]]

    elif(piece=='Z'):
        if(rotate == 0 or rotate == 2):
            map = [[1,1,0],[0,1,1]]
        else:
            map = [[1,0],[1,1],[1,0]]

    else: {}

    return map

def getContour(piece,rotate):
    if(piece=='O'):
        con = [0]

    elif(piece=='J'):
        if(rotate == 0):
            con = [0]
        elif(rotate == 1):
            con = [0,0]
        elif(rotate == 2):
            con = [-2]
        else:
            con = [0,1]

    elif(piece=='L'):
        if(rotate == 0):
            con = [0]
        elif(rotate == 1):
            con = [-1,0]
        elif(rotate == 2):
            con = [2]
        else:
            con = [0,0]

    elif(piece=='I'):
        if(rotate == 0 or rotate == 2):
            con = []
        else:
            con = [0,0,0]

    elif(piece=='S'):
        if(rotate == 0 or rotate == 2):
            con = [0,-1]
        else:
            con = [1]

    elif(piece=='T'):
        if(rotate == 0):
            con = [1,-1]
        elif(rotate == 1):
            con = [1]
        elif(rotate == 2):
            con = [0,0]
        else:
            con = [-1]

    elif(piece=='Z'):
        if(rotate == 0 or rotate == 2):
            con = [1,0]
        else:
            con = [-1]

    else: {}

    return con
