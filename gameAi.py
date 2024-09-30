import random
from game_logic import find_connected_pieces, Location, Orientation
from board import Player, Color

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

def bestMove(board, validMoves, difficulty):
    """
    Determines the best move for the AI based on the selected difficulty.

    Args:
    board: The current state of the game board.
    validMoves: List of valid moves the AI can choose from.
    difficulty: The selected AI difficulty ('easy', 'medium', 'hard').

    Returns:
    The chosen move from validMoves.
    """
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

def longestRoad(player, board):
    """
    Finds and returns the length of the longest road (horizontal or vertical connection) for the player.

    Args:
    player: The player object (Player instance).
    board: The game board (Board instance).

    Returns:
    The length of the longest road (int).
    """
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

def countFlatStones(player):
    """
    Counts the number of pieces the player has placed on the board.

    Args:
    player: The player object (Player instance).

    Returns:
    Number of flat stones placed (int).
    """
    return player.pieces_placed

def flatStoneDiff(player, opponent):
    """
    Calculates the flat stone differential between the player and the opponent.
    FSD criteria.

    Args:
    player: The player object (Player instance).
    opponent: The opponent player object (Player instance).

    Returns:
    The flat stone differential (int).
    """
    return countFlatStones(player) - countFlatStones(opponent)

def centerControl(player, board):
    """
    Calculates how many center squares the player controls. Center control criteria.

    Args:
    player: The player object (Player instance).
    board: The game board (Board instance).

    Returns:
    The number of center squares controlled by the player (int).
    """
    center_squares = [(x, y) for x in range(2, 5) for y in range(2, 5)]  # Generate center square coordinates
    control = 0
    for x, y in center_squares:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == player.color:
            control += 1
    return control

def edgeControl(player, board):
    """
    Calculates how many edge squares the player controls. Edge control criteria.

    Args:
    player: The player object (Player instance).
    board: The game board (Board instance).

    Returns:
    The number of edge squares controlled by the player (int).
    """
    edges = [(0, y) for y in range(5)] + [(4, y) for y in range(5)] + [(x, 0) for x in range(1, 4)] + [(x, 4) for x in range(1, 4)]
    control = 0
    for x, y in edges:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == player.color:
            control += 1
    return control

def score(board, player):
    """
    Evaluates the player's score based on various criteria:
    - Road Potential (RP): Evaluate the length of your longest road and potential extensions.
    - Blocking Opponent (BO) - TODO : Assess how effectively you're blocking the opponent's roads.
    - Flat Stone Differential (FSD): Calculate the difference in flat stones on the board between you and your opponent.
    - Center Control (CC): The amount of control of the center a player has
    - Edge Control (EC): The amount of edge pieces a player has, the more the better

    Args:
    board: The game board (Board instance).
    player: The player object (Player instance).

    Returns:
    The total score for the player (int).
    """
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