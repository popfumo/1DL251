def setDifficulty():
    pass

def bestMove(board, validMoves):
    return 0

#returns a players/ais longest road
def longestRoad(player, board):
    return 0

#Number of adjecent squares where the player can extend their road
def potentialRoadExtensions(board):
    return 0

#count the number of flat stones
def countFlatStones(board, player):
    return 0

#scoring criterias: 
# Road Potential (RP): Evaluate the length of your longest road and potential extensions.
# Blocking Opponent (BO): Assess how effectively you're blocking the opponent's roads.
# Flat Stone Differential (FSD): Calculate the difference in flat stones on the board between you and your opponent.
# Center control, the amount of control of the center a player has
# Edge control, the amount of edge pieces a player has, the more the better
def score(board, player):

    return 0


#Helper function, obtains a list of neighbors around a given square on the board
def neighbours(board, x, y):
    return 0

# Pseudo code, hard mode = depth 2, medium mode = depth 1
def miniMax(currDepth, nodeIndex, maxTurn, scores, targetDepth):

    # Base case
    if (currDepth == targetDepth):
        return scores[nodeIndex]
    
    # Maxing player turn
    if maxTurn:
        return max(miniMax(currDepth + 1, nodeIndex * 2, False, scores, targetDepth)
                   ,miniMax(currDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth))
    # Min player turn
    else:
        return min(miniMax(currDepth + 1, nodeIndex * 2, False, scores, targetDepth)
                   ,miniMax(currDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth))
    pass