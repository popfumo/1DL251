#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation, Color, Location, place_move, move_instruction
from game_logic import placeable, are_adjacent
import copy

num_pieces = 21

# Places a piece in a cell, returns True if the piece was placed, False otherwise
# piece is placed at the front of the array
########################################################################################
#               IMPORTANT NOTE                                                         #                    
#Due to how we have implemented placing a new move the AI will use more then 21 stones #
#either we have to change so the AI can use more then 21 stones or some other option   #                                         
#                                                                                      # 
########################################################################################
def place_piece(player_color:Color, board, location, orientation):     
    if placeable(board, location):
        new_piece = Piece(location, orientation, player_color)  # Use player.color instead of player
        #player.pieces.insert(0, new_piece)
        #player.pieces_placed += 1
        board.get_cell(location).pieces.insert(0, new_piece)
        if board.turn == Color.WHITE:
            board.white_pieces_placed += 1
        else:
            board.black_pieces_placed += 1
        #print(f"Piece placed at {location} with color {player.color}")  # Debug print
        board.turn = board.turn.opposite()
        return True
    else:
        print(f"Cannot place piece at {location}")
        return False
    
"""
def place_piece(player, board, location, orientation):
    if player.pieces_placed < num_pieces: 
        if placeable(board, location):
            new_piece = Piece(location, orientation, player.color)  # Use player.color instead of player
            player.pieces.insert(0, new_piece)
            player.pieces_placed += 1
            board.get_cell(location).pieces.insert(0, new_piece)
            #print(f"Piece placed at {location} with color {player.color}")  # Debug print
            return True
        else:
            print(f"Cannot place piece at {location}")
            return False
    else:    
        print("No more pieces left")
        return False
"""

# Moves a piece to a new location. Returns True if the piece was moved, False otherwise
# Checks if the piece can be placed in the new location by looking at the top piece of the cell at the new location
def move_piece(player_color, board, old_location, new_location):
    if placeable(board, new_location) and not board.get_cell(old_location).is_empty() and old_location != new_location and are_adjacent(old_location, new_location) :
        top_piece = board.get_cell(old_location).get_top_piece()
        if top_piece.orientation == Orientation.VERTICAL and top_piece.color != player_color:
            print("Cannot move piece because the top piece is a vertical piece or the top piece is not the player's piece") 
            return False
        piece_to_move = board.get_cell(top_piece.location).remove_top_piece()
        piece_to_move.location = new_location
        board.get_cell(new_location).pieces.insert(0, piece_to_move)
        board.turn = board.turn.opposite()
        return True
    else:
        return False

# new_locations is an array containing coordinates to place the pieces in, the array is ordered from close to far
def unload_cell(player, board, old_location, new_locations):
    if len(board.get_cell(old_location).pieces) > 0:
        old_x,old_y = old_location.x, old_location.y
        top_piece = (board.cells[old_x][old_y]).get_top_piece()
        if top_piece.color == player.color and top_piece.orientation != Orientation.VERTICAL:
            for location in new_locations:
                if not placeable(board, location):
                    print("unload coordinates not valid")
                    return False 
            for location in new_locations:
                current_piece = board.get_cell(old_location).remove_top_piece()
                board.get_cell(location).pieces.insert(0, current_piece)
            board.turn = board.turn.opposite()
            return True
        else:
            print("Cannot unload piece because the top piece is not the player's piece")
    else:
        print("No pieces to unload")
    return False

def unload_piece_recursive(player, board, num_remove, original_location, current_location):
    print(f"Attempting to unload from location: {original_location}")
    
    cell = board.get_cell(original_location)
    print(f"Cell contents: {cell.pieces}")
    
    if cell.is_empty():
        print("No pieces to unload: The cell is empty.")
        return False

    top_piece = cell.get_top_piece()
    if top_piece is None:
        print("Error: Cell is not empty but get_top_piece() returned None.")
        return False

    print(f"Top piece: Color - {top_piece.color}, Orientation - {top_piece.orientation}") #These are just print statements for bug testing
    print(f"Current player color: {player.color}")

    if top_piece.color != player.color:
        print(f"Cannot unload this piece. Color mismatch: Piece color {top_piece.color}, Player color {player.color}")
        return False
    
    if top_piece.orientation == Orientation.VERTICAL:
        print("Cannot unload this piece. It's vertical.")
        return False

    directions = {"n": (-1, 0), "e": (0, 1), "s": (1, 0), "w": (0, -1)}
    
    while True:
        # Why do we have a function that takes runtime input here? Shouldnt runtime inputs be exclusive to like game.py or something? /edvin
        direction = input(f"Choose direction to place piece {num_remove} (n/e/s/w): ").lower() 
        if direction in directions:
            dx, dy = directions[direction]
            new_location = Location(current_location.x + dx, current_location.y + dy)
            
            if placeable(board, new_location):
                current_piece = cell.remove_top_piece()
                board.get_cell(new_location).pieces.insert(0, current_piece)
                print(f"Piece placed at {new_location}")
                
                if num_remove > 1:
                    return unload_piece_recursive(player, board, num_remove - 1, original_location, new_location)
                else:
                    board.turn = board.turn.opposite()
                    return True
            else:
                print("Cannot place piece in that direction. Try again.")
        else:
            print("Invalid direction. Please choose n, e, s, or w.")

def circle_condtion(player, board, location):
    flag = 0
    target = 4
    for i in range(5):
        if i == 0 and location.x - 1 >= 0:
                new_loc = Location(location.x - 1, location.y)
                board.get_cell(new_loc).get_top_piece.orientation == Orientation.VERTICAL
                flag += 1
        elif i == 1 and location.x + 1 :
            pass
         # any([condition(c) for c in [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)o if is_valid_cell(c) ])
    return 0


def getAllPossibleMoves(board : Board, player_color: Color):
    """
    This function will create a list of boards, it will take the current board and make a copy of it, 
    it will then create a new board for each possible move that can be made and append to a list.
    """
    # this new_boards variable holds all the new boards that can be "made" by all the performing all possible moves
    # the idea is that we iterate over this when checking the score for each move, and then picking the board we want depending on the AI difficulty
    # not the most efficient approach with regards to performance, but i think it will do /edvin & viktor
    valid_moves:move_instruction = []
    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col)) # Get the cell at the current location
            
            # Add all possible boards that can be created after placing a new piece.
            # If the cell is empty or has a horizontal piece on top, we can place a piece
            if cell.is_empty() or cell.get_top_piece().orientation == Orientation.HORIZONTAL: 

                new_horizontal_move = place_move(player_color, Location(row, col), Orientation.HORIZONTAL)
                new_horizontal_instruction = move_instruction(new_horizontal_move)
                valid_moves.append(new_horizontal_instruction)
                
                new_vertical_move = place_move(player_color, Location(row, col), Orientation.VERTICAL)
                new_vertical_instruction = move_instruction(new_vertical_move)
                valid_moves.append(new_vertical_instruction)

            # Add all possible boards that can be created after moving a stack.
            # This is much more complex than placing a new piece, as the ways in which you can move a stack are much greater in numbers
            if not cell.is_empty(): # apparently python does not have lazy evaluation of if statements, hence this is nested
                if cell.get_top_piece().color == player_color and cell.get_top_piece().orientation == Orientation.HORIZONTAL:
                    
                    # Our color is on top of this cell, meaning we can move as many pieces as we want in this stack.
                    # How many pieces do we want to move from the stack? This for loop iterates over the different possible amounts
                    x,y = cell.location.x, cell.location.y
                    #print(f"finding moves for Cell location: {x}, {y}")
                    start_location = Location(x,y)

                    for num_pieces_to_move in range(1, len(cell.pieces) + 1):
                        #print(f"num_pieces_to_move: {num_pieces_to_move}")
                        valid_moves.extend(get_all_possible_boards_after_stack_move(board, player_color, start_location, num_pieces_to_move))
                        #print(f"new_boards length: {len(new_boards)}")
    return valid_moves


# Returns a list of all possible boards that can be created after moving a stack of pieces
# num_pieces_to_move is the number of pieces to move from the stack
# This function is called by getAllPossibleMoves()
def get_all_possible_boards_after_stack_move(board:Board, player_color,start_location: Location, num_pieces_to_move: int):
    assert num_pieces_to_move > 0
    start_cell: Cell = board.get_cell(start_location)
    assert not start_cell.is_empty()
    assert start_cell.get_top_piece().color == player_color
    assert start_cell.get_top_piece().orientation == Orientation.HORIZONTAL
    assert num_pieces_to_move <= len(start_cell.pieces)

    colors_of_pieces_to_move = []
    copy_start_cell = copy.deepcopy(start_cell)
    for i in range(num_pieces_to_move):
        piece_to_move = copy_start_cell.remove_top_piece()
        colors_of_pieces_to_move.append(piece_to_move.color)
    # cell now has its pieces to move removed. The pieces are put in the list pieces_to_move

    assert len(colors_of_pieces_to_move) == num_pieces_to_move
    
    instructions = []
    aux_get_all_PBASM(board, start_location, colors_of_pieces_to_move, instructions)
    return instructions

aux_inst_list = []

# This is an auxilary function that is used in get_all_possible_boards_after_stack_move() 
# This function will call itself recursively until there are no pieces to move
def aux_get_all_PBASM(board: Board, loc: Location, colors_of_pieces_to_move: list, instructions: list):
    # Base case: If there are no more pieces to move, save the instruction sequence and return
    if not colors_of_pieces_to_move:
        instructions.append(aux_inst_list[:])  # Save a deep copy of the current move list
        return

    # Loop through possible directions (up, down, left, right)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = loc.x + dx, loc.y + dy
        if 0 <= new_x < 5 and 0 <= new_y < 5:  # Ensure the move is within boundaries
            new_loc = Location(new_x, new_y)
            if placeable(board, new_loc):  # Check if placing a piece is allowed
                # Create a new piece and add it to the board
                new_piece = Piece(new_loc, Orientation.HORIZONTAL, colors_of_pieces_to_move[0])  
                piece_to_save = place_move(new_piece.color, new_loc, new_piece.orientation)
                
                # Insert the piece into the board cell and update the move list
                board.get_cell(new_loc).pieces.insert(0, new_piece)
                aux_inst_list.append(piece_to_save)
                
                # Recursive call with the remaining pieces (excluding the one just placed)
                aux_get_all_PBASM(board, new_loc, colors_of_pieces_to_move[1:], instructions)
                
                # Backtrack: Remove the last piece and undo the move
                aux_inst_list.pop()
                board.get_cell(new_loc).pieces.remove(new_piece)

# This is an auxilary function that is used in get_all_possible_boards_after_stack_move(), instead 
# of copying the board for each move, we will use this function to make the move and then undo it
def aux_undo(board: Board, instruction: place_move):
    if instruction != None:
        board.get_cell(instruction.location).remove_top_piece()
        return True
    else:
        to_remove = board.latest_move
        for i in range(len(to_remove)):
            board.get_cell(to_remove[i].location).remove_top_piece()
        return True 