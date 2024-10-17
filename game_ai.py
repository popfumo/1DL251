import random
from typing import List
from game_logic import find_connected_pieces, Location, Orientation, check_win
from board import Piece, Player, Color, Board, GameResult, MoveType, StackMove, PlacementMove, MoveInstruction
from interaction_functions import get_all_possible_moves, make_move_ai, undo_move
import copy


#############################################################################################
# NOTE: Possible buggs and fixed that are needed as of 8/10
# Bug kepping count of pieces placed, origin prob undo_move
# Bug when playing the AI deleted some of there pieces and did not place any new, prob bug in move or undo
# The AI almost always begins with a blocking piece, weird behaviour, fix score function
#############################################################################################

TARGET_DEPTH:int
WIN = 10000
MAX_DEPTH = 2

def set_difficulty():
    """
    Prompts the user to choose the AI difficulty level.
    Returns the selected difficulty as a string: 'easy', 'medium', or 'hard'.
    """
    while True:
        difficulty = input("Choose difficulty (easy (1), medium (2), hard (3)): ").lower()
        match difficulty:
            case "1":
                return "easy"
            case "2":
                return "medium"
            case "3":
                return "hard"
            case _:
                print("Invalid input. Please choose 'easy', 'medium', or 'hard'.")

# Function for AI to choose its move based on the difficulty
# Makes a copy of the board, so dont spam this function
def AI_get_move(board,valid_moves, difficulty):
    
    board_copy = copy.deepcopy(board)
    if difficulty == "easy":
        # Randomly select a move from the valid moves
        return random.choice(valid_moves)
    
    elif difficulty == "medium":
        TARGET_DEPTH = 1
        depth = 1
        #next_move = find_best_move(board_copy, valid_moves,depth, None)
        find_best_move(board_copy, valid_moves)
        
        return next_move
        
    
    elif difficulty == "hard":
        TARGET_DEPTH = 2
        depth = 2
        #next_move = find_best_move(board_copy, valid_moves,depth, None)        
        find_best_move(board_copy, valid_moves)

        return next_move


#################################################
#   NOTE: when scoring, WHITE wants to maximize,#
#   BLACK wants to minimize                     #
#################################################
def longest_road(board):
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
def potential_road_extensions(board, player):
    return 0

def flat_stone_diff(board:Board):
    """
    Counts the top pieces on the board and returns the difference between the white and black pieces.

    Args:
    board: the board to count the flatstones on

    Returns:
    The flat stone differential (int).
    """
    piece_score = 0
    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col))
            if not cell.is_empty():
                top_piece = cell.get_top_piece()
                # TODO: Hard coded that AI is white and not black
                if top_piece.color == Color.WHITE and top_piece.orientation == Orientation.HORIZONTAL:
                    piece_score += 1
                elif top_piece.color == Color.BLACK and top_piece.orientation == Orientation.HORIZONTAL:
                    piece_score -= 1

    return piece_score

# TODO: Also hard coded that AI is white and not black
def center_control(board):
    """
    Calculates how many center squares the player controls. Center control criteria.

    Args:
    board: The game board (Board instance).

    Returns:
    The center score.
    """
    center_squares = [(x, y) for x in range(1, 4) for y in range(1, 4)]  # Generate center square coordinates
    center_score = 0

    for x, y in center_squares:
        cell = board.get_cell(Location(x, y))
        if not cell.is_empty() and cell.get_top_piece().color == Color.WHITE:
            center_score += 1
        elif not cell.is_empty() and cell.get_top_piece().color == Color.BLACK:
            center_score -= 1

    return center_score
# TODO: Also hard coded that AI is white and not black
def edge_control(board):
    """
    Calculates how many edge squares the player controls. Edge control criteria.

    Args:
    player: The player object (Player instance).
    board: The game board (Board instance).

    Returns:
    The number of edge squares controlled by the player (int).
    """
    edges = [(0, y) for y in range(4)] + [(4, y) for y in range(4)] + [(x, 0) for x in range(0, 4)] + [(x, 4) for x in range(0, 4)]
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

    game_result = check_win(board)
    
    if game_result == GameResult.VICTORY_BLACK:        
        return -WIN
    elif game_result == GameResult.VICTORY_WHITE:        
        return WIN
 
    
    # Calculate each criterion for the player and opponent
    player_longest_road = longest_road(board)
    ##print(f'longest road:{player_longest_road}')
    
    # TODO: Calculate extention potential
    # TODO: blocking opponent
    
    player_flat_stones = flat_stone_diff(board)
    ##print(f'flatstone diff:{player_flat_stones}')
    the_center_control = center_control(board)
    ##print(f'center control:{center_control}')
    the_edge_control = edge_control(board)
    ##print(f'edge_control:{edge_control}')

    # Weights for each criterion (adjust these values as needed)
    weight_longest_road = 5
    weight_flat_stones = 2
    weight_center_control = 3
    weight_edge_control = 1

    #Calculate the score for the player
    board_score = (player_longest_road * weight_longest_road) + \
                   (player_flat_stones * weight_flat_stones) + \
                   (the_center_control * weight_center_control) + \
                   (the_edge_control * weight_edge_control)

    return board_score



# def find_best_move(board: Board, valid_moves: List[MoveInstruction], depth:int, best_move_found:MoveInstruction):
    
#     if depth == 0:
#         score_board = score(board)
#         #print(f'score: {score_board}')
#         return score_board
    
#     max_score:int 
#     if board.turn == Color.white: 
#         max_score = -WIN 
#     else: 
#         max_score = WIN

#     for move in valid_moves: 
#         make_move_ai(board, move)
#         next_moves = get_all_possible_moves(board, Color.BLACK)
#         current_score = find_best_move(board, next_moves, depth - 1,best_move_found) # go into the next depth level

#         if (board.turn == Color.white and current_score > max_score) or (board.turn == Color.black and current_score < max_score):
#             max_score = current_score
#             if depth == TARGET_DEPTH: 
#                 best_move_found = move        
#         undo_move(board)
#         return max_score
        
#     return best_move_found    


#TODO: FIX THE TODO IN FIND_MOVE_MINIMAX
#helper function, it purpose is to make the initial call to the recursive function find_move_minimax and then return the result
def find_best_move(board, valid_moves):
    global next_move
    next_move = None
    find_move_minimax(board, valid_moves, MAX_DEPTH, board.white_to_move())
    #find_move_pruning(board, valid_moves, MAX_DEPTH, -WIN, WIN, 1 if board.white_to_move() else -1)

    return next_move

#recursive function that finds the best move for the player
def find_move_minimax(board, valid_moves, depth, white_to_move):        
    
    ##print(f'valid moves: {valid_moves}')

    global next_move #Needs to be global, cuz it is used in the recursive function
    
    #If the depth is 0, we have reached the end of the search tree    
    if depth == 0:
        score_board = score(board)
        #print(f'score: {score_board}')
        return score_board

    if white_to_move:
        max_score = -WIN

        for move in valid_moves: 
            if isinstance(move, PlacementMove):
                if move == PlacementMove(Piece(Location(4, 1), Orientation.HORIZONTAL, Color.WHITE)):
                    print('found the move')
            make_move_ai(board, move)
            next_moves = get_all_possible_moves(board, Color.BLACK) #TODO THIS TAKES IN A PLAYER OBJECT, NOT A COLOR OBJECT, BUT WE WANT TO FIND ALL MOVES FOR THE WHITE
            #want to find all possible moves based on color cuz we need both our moves and the opponents moves thus taking in only a player is not enough and taking in boath a player and opponent seams execcive
            current_score = find_move_minimax(board, next_moves, depth - 1, not white_to_move) # go into the next depth level
            
            if current_score > max_score:
                max_score = current_score
                if depth == MAX_DEPTH: 
                    next_move = move

            #print('board from minimax from white: ')
            #print(board)
            #print(f'turn: {board.turn}')
            undo_move(board)
        return max_score

    else:
        min_score = WIN

        for move in valid_moves:
            make_move_ai(board, move)
            next_moves = get_all_possible_moves(board, Color.WHITE)
            current_score = find_move_minimax(board, next_moves, depth - 1, white_to_move)
            if current_score == WIN:
                return current_score
            if current_score < min_score:
                min_score = current_score
                if depth == MAX_DEPTH:
                    next_move = move

            #print('bord in minimax from black: ')
            #print(board)
            #print(f'turn: {board.turn}')
            undo_move(board)
        return min_score
