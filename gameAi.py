import random
from game_logic import find_connected_pieces, Location, Orientation
from board import Player, Color, Board 

def setDifficulty():
    """
    Prompts the user to choose the AI difficulty level.
    Returns the selected difficulty as a string: 'easy', 'medium', or 'hard'.
    """
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            return difficulty
        else:
            print("Invalid input. Please choose 'easy', 'medium', or 'hard'.")

# Function for AI to choose its move based on the difficulty
def bestMove(validMoves, difficulty):
    
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


#################################################
#   NOTE: when scoring, WHITE wants to maximize,#
#   BLACK wants to minimize                     #
#################################################

def longestRoad(board):
    """
    Finds and returns the length of the longest road (horizontal or vertical connection).

    Args:
    board: The game board (Board instance).

    Returns:
    The length of the longest road (int).
    """
    longest_road_score = 0
    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col))
            if not cell.is_empty():
                top_piece = cell.get_top_piece()
                if top_piece.color == Color.WHITE and top_piece.orientation == Orientation.HORIZONTAL:
                    connected = find_connected_pieces(board, Color.WHITE,Location(row, col))
                    if len(connected) > 0 and len(connected) > longest_road_score:
                        longest_road_score = len(connected)
                elif top_piece.color == Color.BLACK and top_piece.orientation == Orientation.HORIZONTAL:
                    connected = find_connected_pieces(board, Color.BLACK,Location(row, col))
                    if len(connected) > 0 and len(connected) > longest_road_score:
                        longest_road_score = -len(connected)

    return longest_road_score

#Number of adjecent squares where the player can extend their road
def potentialRoadExtensions(board, player):
    return 0
                    
def flatStoneDiff(board):
    """
    Calculates the flat stone differential between the player and the opponent.
    FSD criteria.

    Args:
    board: the board to count the flatstones on

    Returns:
    The flat stone differential (int).
    """
    placement_score = 0

    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col))
            if not cell.is_empty():
                top_piece = cell.get_top_piece()
                if top_piece.color == Color.WHITE:
                    placement_score += 1
                elif top_piece.color == Color.BLACK:
                    placement_score -= 1

    return placement_score

def centerControl(board):
    """
    Calculates how many center squares the player controls. Center control criteria.

    Args:
    board: The game board (Board instance).

    Returns:
    The center score.
    """
    center_squares = [(x, y) for x in range(2, 5) for y in range(2, 5)]  # Generate center square coordinates
    center_score = 0

    for x, y in center_squares:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == Color.WHITE:
            center_score += 1
        elif not cell.is_empty() and cell.get_top_piece().color == Color.BLACK:
            center_score -= 1

    return center_score

def edgeControl(board):
    """
    Calculates how many edge squares the player controls. Edge control criteria.

    Args:
    player: The player object (Player instance).
    board: The game board (Board instance).

    Returns:
    The number of edge squares controlled by the player (int).
    """
    edges = [(0, y) for y in range(5)] + [(4, y) for y in range(5)] + [(x, 0) for x in range(1, 4)] + [(x, 4) for x in range(1, 4)]
    edge_score = 0
    for x, y in edges:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == Color.WHITE:
            edge_score += 1
        elif not cell.is_empty() and cell.get_top_piece().color == Color.BLACK:
            edge_score -= 1

    return edge_score

def score(board):
    """
    Evaluates the player's score based on various criteria:
    - Road Potential (RP): Evaluate the length of your longest road and potential extensions.
    - Blocking Opponent (BO) - TODO : Assess how effectively you're blocking the opponent's roads.
    - Flat Stone Differential (FSD): Calculate the difference in flat stones on the board between you and your opponent.
    - Center Control (CC): The amount of control of the center a player has
    - Edge Control (EC): The amount of edge pieces a player has, the more the better

    Args:
    board: The game board to be scored

    Returns:
    The total score for the board (int).
    """

    board_score = 0
    
    # Calculate each criterion for the player and opponent
    player_longest_road = longestRoad(board)
    print(f'longest road:{player_longest_road}')
    
    # TODO: Calculate extention potential
    # TODO: blocking opponent
    
    player_flat_stones = flatStoneDiff(board)
    print(f'flatstone diff:{player_flat_stones}')
    center_control = centerControl(board)
    print(f'center control:{center_control}')
    edge_control = edgeControl(board)
    print(f'edge_control:{edge_control}')

    # Weights for each criterion (adjust these values as needed)
    weight_longest_road = 5
    weight_flat_stones = 2
    weight_center_control = 3
    weight_edge_control = 1

    # Calculate the score for the player
    board_score = (player_longest_road * weight_longest_road) + \
                   (player_flat_stones * weight_flat_stones) + \
                   (center_control * weight_center_control) + \
                   (edge_control * weight_edge_control)

    return board_score


def miniMax(currDepth, nodeIndex, maxTurn, scores, targetDepth):
    """
    Recursive implementation of the Minimax algorithm.

    Args:
    currDepth: The current depth of the tree.
    nodeIndex: The index of the current node in the scores list.
    maxTurn: True if it's the maximizing player's turn, False otherwise.
    scores: List of scores for the terminal nodes.
    targetDepth: The depth limit for the Minimax algorithm.

    Returns:
    The score of the optimal move for the current player.
    """

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