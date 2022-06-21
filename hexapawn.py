import copy

# 1) The function’s purpose is to initial the hexapawn program
# 2) Expected Arguments are: a list of string as start state, an int indicate the size of the board,
# a char 'b' or 'w' to indicate your side, an int on how deep would the program search 
# 3) The function returns a list of string as a next move for hexapawn
def hexapawn(state, boardSize, yourPawn, depth):
    global maxChildlist
    global minChildlist
    internalRepList = []
    for row in state:
        internalRepList.append(convertToList(row))  
    if yourPawn == 'b':
        valueOfNextMove = minimax(internalRepList, boardSize, True, 'b', depth, -99999, 99999)
        print('Heuristic value for this move from minimax(postive for b, negative for w):', 
        valueOfNextMove)
        for ele in maxChildlist:
            if ele.heuristicValue == valueOfNextMove:
                return ele.state
    elif yourPawn == 'w':
        valueOfNextMove = minimax(internalRepList, boardSize, False, 'w', depth, -99999, 99999)
        print('Heuristic value for this move from minimax(postive for b, negative for w):', 
        valueOfNextMove)
        for ele in minChildlist:
            if ele.heuristicValue == valueOfNextMove:
                return ele.state
    else:
        print('You need to choose your pawn.')




# 1) This class is to define a node to associate a state with its heuristicValue
# 2) Expected Arguments are: a list of string as state, an int indicate the heuristicValue
class Node:
   def __init__(self, state, heuristicValue):
      self.state = state
      self.heuristicValue = heuristicValue
    
   def __lt__(self, other):
       return self.heuristicValue < other.heuristicValue




# 1) The function’s purpose is to minimax search with Alpha–beta pruning
# 2) Expected Arguments are: a list of string as start state, an int indicate the size of the board,
# a bool isMaxLevel indicate if this level is a max level, a char 'b' or 'w' to indicate your side, 
# an int on how deep would the program search, ints alpha and beta for Alpha–beta pruning
# 3) The function returns a int indicating the Heuristic value for this move 
# from minimax(postive for b, negative for w)
def minimax(state, boardSize, isMaxLevel, yourPawn, depth, alpha, beta):
    if depth == 0 or gameOver(state, boardSize, isMaxLevel):
        return staticBoardEvaluator(state, boardSize, isMaxLevel).heuristicValue

    if isMaxLevel:
        maxEval = -9999
        newStates = moveGenerator(state, boardSize, 'b')
        # print(newStates)    
        for s in newStates:
            child = staticBoardEvaluator(s, boardSize, True)
            eval = minimax(child.state, boardSize, False, yourPawn, 
            depth-1, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        stringList = []
        for t in state:
            stringList.append(convertToString(t))
        newNode = Node(stringList,maxEval)
        passOutMinChildrenList(newNode)
        return maxEval
    
    else:
        minEval = 9999
        newStates = moveGenerator(state, boardSize, 'w')
        # print(state) 
        for s in newStates:
            child = staticBoardEvaluator(s, boardSize, False)
            eval = minimax(child.state, boardSize, True, yourPawn, 
            depth-1, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        stringList = []
        for t in state:
            stringList.append(convertToString(t))
        newNode = Node(stringList,minEval)
        passOutMaxChildrenList(newNode)
        return minEval




# 1) The function’s purpose is to update the childlist for minlevel
# 2) Expected Arguments are: a Node from defined above
# 3) The function returns nothing but update the childlist for minlevel
minChildlist = []
def passOutMinChildrenList(child):
    global minChildlist
    minChildlist.append(child)
    # for node in childlist:
    #     print(node.state)




# 1) The function’s purpose is to update the childlist for maxlevel
# 2) Expected Arguments are: a Node from defined above
# 3) The function returns nothing but update the childlist for maxlevel
maxChildlist = []
def passOutMaxChildrenList(child):
    global maxChildlist
    maxChildlist.append(child)
    # for node in maxChildlist:
    #     print(node.state)
    #     print(node.heuristicValue)
    



# 1) The function’s purpose is to determine if a board is game over
# 2) Expected Arguments are: a list of string as state, an int indicate the size of the board,
# a bool isMaxLevel indicate if this level is a max level
# 3) The function returns true if it is game over; false when its not
def gameOver(state, boardSize, isMaxLevel):
    bCords = findCoordinates(state, 'b')
    wCords = findCoordinates(state, 'w')
    stringList = []
    for t in state:
        stringList.append(convertToString(t))
    
    # out of pawns
    if bCords == []:  # w wins
        newNode = Node(stringList,-10)
        passOutMinChildrenList(newNode) 
        return True
    elif wCords == []: # b wins
        newNode = Node(stringList,10)
        passOutMaxChildrenList(newNode) 
        return True
    # reach the other end
    elif 'b' in state[0]:
        newNode = Node(stringList,10)
        passOutMaxChildrenList(newNode) 
        return True
    elif 'w' in state[boardSize-1]:
        newNode = Node(stringList,-10)
        passOutMinChildrenList(newNode) 
        return True
    # out of move
    elif isMaxLevel and moveGenerator(state, boardSize, 'b') == []: # means it is b's turn
        newNode = Node(stringList,-10)
        passOutMinChildrenList(newNode) 
        return True
    elif not isMaxLevel and moveGenerator(state, boardSize, 'w') == []: # w's turn
        newNode = Node(stringList,10)
        passOutMaxChildrenList(newNode) 
        return True
    else:
        return False




# 1) The function’s purpose is to generate new legal states from a state
# 2) Expected Arguments are: a list of string as start state, an int indicate the size of the board,
# a char 'b' or 'w' to indicate the pawn to move, 
# 3) The function returns a list of new states in the type of list of lists         
def moveGenerator(state, boardSize, pawnToMove):
    newStates = []
    if pawnToMove == 'b':
        coordinatesList = findCoordinates(state, pawnToMove)
        for coordinate in coordinatesList:
            if coordinate[1] == 0: #leftmost case
                if state[coordinate[0]-1][coordinate[1]] == '-': #move up
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]] = 'b'
                    newStates.append(newState)
                if state[coordinate[0]-1][coordinate[1]+1] == 'w': #move up dia right
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]+1] = 'b'
                    newStates.append(newState)

            elif coordinate[1] == boardSize-1: #rightmost case
                if state[coordinate[0]-1][coordinate[1]] == '-': #move up
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]] = 'b'
                    newStates.append(newState)
                if state[coordinate[0]-1][coordinate[1]-1] == 'w': #move up dia left
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]-1] = 'b'
                    newStates.append(newState)
            
            else:
                if state[coordinate[0]-1][coordinate[1]-1] == 'w': #move up dia left
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]-1] = 'b'
                    newStates.append(newState)
                if state[coordinate[0]-1][coordinate[1]+1] == 'w': #move up dia right
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]+1] = 'b'
                    newStates.append(newState)
                if state[coordinate[0]-1][coordinate[1]] == '-': #move up
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]-1][coordinate[1]] = 'b'
                    newStates.append(newState)

    elif pawnToMove == 'w':
        coordinatesList = findCoordinates(state, pawnToMove)
        for coordinate in coordinatesList:
            if coordinate[1] == 0: #leftmost case
                if state[coordinate[0]+1][coordinate[1]] == '-': #move down
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]] = 'w'
                    newStates.append(newState)
                if state[coordinate[0]+1][coordinate[1]+1] == 'b': #move down dia right
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]+1] = 'w'
                    newStates.append(newState)
            
            elif coordinate[1] == boardSize-1:
                if state[coordinate[0]+1][coordinate[1]] == '-': #move down
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]] = 'w'
                    newStates.append(newState)
                if state[coordinate[0]+1][coordinate[1]-1] == 'b': #move down dia left
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]-1] = 'w'
                    newStates.append(newState)

            else:
                if state[coordinate[0]+1][coordinate[1]-1] == 'b': #move down dia left
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]-1] = 'w'
                    newStates.append(newState)
                if state[coordinate[0]+1][coordinate[1]+1] == 'b': #move down dia right
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]+1] = 'w'
                    newStates.append(newState)
                if state[coordinate[0]+1][coordinate[1]] == '-': #move down
                    newState = copy.deepcopy(state)
                    newState[coordinate[0]][coordinate[1]] = '-'
                    newState[coordinate[0]+1][coordinate[1]] = 'w'
                    newStates.append(newState)
    else:
        print('You need to choose your pawn to move.')

    return newStates




# 1) The function’s purpose is to evaluator a board's heuritic value using the sample
# evaluation metric
# 2) Expected Arguments are: a list of string as start state, an int indicate the size of the board,
# a bool isMaxLevel indicate if this level is a max level, 
# 3) The function returns a Node containing the state and the heuristic value of it
def staticBoardEvaluator(state, boardSize, isMaxLevel):
    bCords = findCoordinates(state, 'b')
    wCords = findCoordinates(state, 'w')
    # w wins
    if bCords == [] or 'w' in state[boardSize-1]:
        myNode = Node(state,-10)
    # b wins
    elif wCords == [] or 'b' in state[0]:
        myNode = Node(state, 10)
    # out of move
    elif isMaxLevel and moveGenerator(state, boardSize, 'b') == []: # means it is b's turn
        myNode = Node(state,-10)
    elif not isMaxLevel and moveGenerator(state, boardSize, 'w') == []: # w's turn
        myNode = Node(state, 10)
    else:
        myNode = Node(state,len(bCords)-len(wCords))
    return myNode




# 1) The function’s purpose is to find all coordinates of a given alphabet in a board
# 2) Expected Arguments are: a list of string as state, an char indicating the pawn to look for
# 3) The function returns a list of Coordinates(type: list) of given alphabet
def findCoordinates(state,alphabet):
    coordinatesList = []
    xCord,yCord = -1,-1
    for y in range(len(state)): 
        for x in range(len(state[y])): 
            if(state[y][x] == alphabet): 
                xCord, yCord = x,y
                coordinate = []
                coordinate.append(y)
                coordinate.append(x)
                coordinatesList.append(coordinate)
    return coordinatesList





# 1) The function’s purpose is to convert a string to a list
# 2) Expected Arguments are: a string
# 3) The function returns a list of char
def convertToList(string):
    list1=[]
    list1[:0]=string
    return list1




# 1) The function’s purpose is to convert a list to a string
# 2) Expected Arguments are: a list of char
# 3) The function returns a string
def convertToString(l):
    str1 = ""
    for x in l:
        str1 += x 
    return str1





print(hexapawn(['--w','bw-','b-b'], 3, 'b', 2))

# test cases:
# 1) hexapawn(['--w','bw-','b-b'], 3, 'b', 2) 
# prints:  
# Heuristic value for this move from minimax(postive for b, negative for w):  10
# ['b-w', '-w-', 'b-b']
#
# 2) hexapawn(['-ww','w--','bbb'], 3, 'w', 2) 
# prints:  
# Heuristic value for this move from minimax(postive for b, negative for w): -10
# ['-ww', '---', 'bwb']
#
# 3) hexapawn(['w-w','bwb','-b-'], 3, 'b', 3)
# No legal move case
# prints:
# Heuristic value for this move from minimax(postive for b, negative for w): -10
# None
#
# 4) hexapawn(['w-ww','bwb-','----','-b-b'], 4, 'b', 5)
# Increase board size
# prints:
# Heuristic value for this move from minimax(postive for b, negative for w): 10
# ['w-wb', 'bw--', '----', '-b-b']
