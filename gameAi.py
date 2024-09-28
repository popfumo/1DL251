import random
from game_logic import find_connected_pieces, Location, Orientation
from board import Player, Color

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
    longestRoad = 0
    for row in range(5):
        for col in range(5):
            cell = board.get_cell(Location(row, col))
            if not cell.is_empty():
                top_piece = cell.get_top_piece()
                if top_piece.color == player.color and top_piece.orientation == Orientation.HORIZONTAL:
                    connected = find_connected_pieces(board, player,Location(row, col))
                    if len(connected) > 0:
                        longestRoad = len(connected)
    return longestRoad

#Number of adjecent squares where the player can extend their road
def potentialRoadExtensions(board):
    return 0

#count the number of flat stones
def countFlatStones(player):
    return player.pieces_placed

# Helper function for the score criteria (FSD)
def flatStoneDiff(player, opponent):
    return countFlatStones(player) - countFlatStones(opponent)

# Center Control: Count how many pieces the player has in the center of the board
def centerControl(player, board):
    center_squares = [(x, y) for x in range(2, 5) for y in range(2, 5)]  # Generate center square coordinates
    control = 0
    for x, y in center_squares:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == player.color:
            control += 1
    return control

# Edge Control: Count how many pieces the player has along the edges of the board
def edgeControl(player, board):
    edges = [(0, y) for y in range(5)] + [(4, y) for y in range(5)] + [(x, 0) for x in range(1, 4)] + [(x, 4) for x in range(1, 4)]
    control = 0
    for x, y in edges:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == player.color:
            control += 1
    return control

#scoring criterias: 
# Road Potential (RP): Evaluate the length of your longest road and potential extensions.
# Blocking Opponent (BO): Assess how effectively you're blocking the opponent's roads.
# Flat Stone Differential (FSD): Calculate the difference in flat stones on the board between you and your opponent.
# Center control, the amount of control of the center a player has
# Edge control, the amount of edge pieces a player has, the more the better
# TODO: Add BO criteria
def score(board, player):
    # Define the opponent (you can add an opponent parameter instead if needed)
    opponent = Player(Color.WHITE if player.color == Color.BLACK else Color.BLACK)
    
    # Calculate each criterion for the player and opponent
    player_longest_road = longestRoad(player, board)
    # TODO: Calculate opponents longest road
    
    player_flat_stones = flatStoneDiff(player, opponent)
    center_control = centerControl(player, board)
    edge_control = edgeControl(player, board)

    # Weights for each criterion (adjust these values as needed)
    weight_longest_road = 5
    weight_flat_stones = 2
    weight_center_control = 3
    weight_edge_control = 1

    # Calculate the score for the player
    player_score = (player_longest_road * weight_longest_road) + \
                   (player_flat_stones * weight_flat_stones) + \
                   (center_control * weight_center_control) + \
                   (edge_control * weight_edge_control)

    return player_score



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