import random

# Set the difficulty for the AI
def setDifficulty():
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            return difficulty
        else:
            print("Invalid input. Please choose 'easy', 'medium', or 'hard'.")

# Function for AI to choose its move based on the difficulty
def bestMove(board, validMoves, difficulty):
    
    if difficulty == "easy":
        # Randomly select a move from the valid moves
        return random.choice(validMoves)
    
    # TODO: return minimax function with depth 1
    elif difficulty == "medium":
        # Use Minimax with depth 1
        #return bestMove(board, validMoves, depth=1)
        pass
    
    # TODO: return minimax function with depth 1
    elif difficulty == "hard":
        # Use Minimax with depth 2
        #return bestMove(board, validMoves, depth=2)
        pass

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