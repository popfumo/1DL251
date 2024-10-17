#!/usr/bin/env python3

from board import Piece, Cell, PlacementMove, StackMove, MoveType, Player, Board, Orientation, Color, Location, MoveInstruction
from game_logic import placeable, are_adjacent
import copy

NUM_PIECES = 21

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
        if player_color == Color.WHITE:
            board.white_pieces_placed += 1
        else:
            board.black_pieces_placed += 1
        #print(f"Piece placed at {location} with color {player.color}")  # Debug print
        move_instruction = PlacementMove(new_piece)
        board.latest_move.append(move_instruction)
        board.turn = board.turn.opposite()
        return True
    else:
        print(f"Cannot place piece at {location}")
        return False
    
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
# TODO: Dead code, remove 
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

#takes in a move_instruction, this instruction can either be a place instruction or a move instruction
#if valid_move is a list it is a move instruction, otherwise it is a place instruction
def make_move_ai(board: Board, move_to_make: MoveInstruction):
    if isinstance(move_to_make, StackMove): # It is a stack move instruction
        #inst = []
        start_piece = move_to_make.start_cell
        for piece in move_to_make.stack_moves:
            board.get_cell(piece.location).pieces.insert(0, piece)
            #inst.append(piece)
            board.get_cell(start_piece.location).remove_bottom_piece()         
        
        board.turn = board.turn.opposite()
        board.latest_move.append(move_to_make)
        return True
    
    else: # It is a place instruction
        #print (type(move_to_make))
        location = move_to_make.new_placement.location
        color = move_to_make.new_placement.color
        orientation = move_to_make.new_placement.orientation
        place_piece(color, board, location, orientation)
        
        # Tror den tar bara en instruktion
        return False
    

def get_all_possible_moves(board : Board, player_color: Color):
    """
    This function will create a list of boards, it will take the current board and make a copy of it, 
    it will then create a new board for each possible move that can be made and append to a list.
    """
    # this new_boards variable holds all the new boards that can be "made" by all the performing all possible moves
    # the idea is that we iterate over this when checking the score for each move, and then picking the board we want depending on the AI difficulty
    # not the most efficient approach with regards to performance, but i think it will do /edvin & viktor
    valid_moves:MoveInstruction = []
    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col)) # Get the cell at the current location
            
            # Add all possible boards that can be created after placing a new piece.
            # If the cell is empty or has a horizontal piece on top, we can place a piece
            if cell.is_empty() or cell.get_top_piece().orientation == Orientation.HORIZONTAL: 

                new_horizontal_move = Piece(Location(row, col), Orientation.HORIZONTAL, player_color)
                new_horizontal_instruction = PlacementMove(new_horizontal_move)
                valid_moves.append(new_horizontal_instruction)
                
                new_vertical_move = Piece(Location(row, col), Orientation.VERTICAL, player_color)
                new_vertical_instruction = PlacementMove(new_vertical_move)
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
                        #print(f"num_pieces_to_move: {num_pieces_to_move}")
                        #print(range(1, len(cell.pieces) + 1))
                        valid_moves.extend(get_all_possible__stack_moves(board, player_color, start_location, num_pieces_to_move))
                        #print(f"new_boards length: {len(new_boards)}")
    return valid_moves

# Returns a list of all possible boards that can be created after moving a stack of pieces
# num_pieces_to_move is the number of pieces to move from the stack
# This function is called by get_all_possible_moves()
def get_all_possible__stack_moves(board:Board, player_color,start_location: Location, num_pieces_to_move: int):
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

    assert len(colors_of_pieces_to_move) == num_pieces_to_move
    
    instructions = []
    
    aux_get_all_psm(board, start_location, colors_of_pieces_to_move, instructions, start_cell.get_top_piece(), recursive_move_list=[])    
    
    # instructions = [element for element in instructions if element.stack_moves.__len__() != 0]
    # for i in instructions:
    #     print("in get_all_possible_stack_moves" + str(i))
    return instructions

# aux_inst_list = []

# This is an auxilary function that is used in get_all_possible_boards_after_stack_move() 
# This function will call itself recursively until there are no pieces to move
#it will return a list with first the stacks start piece and then the instructions to move the pieces
def aux_get_all_psm(board: Board, loc: Location, colors_of_pieces_to_move: list, instructions: list, top_piece: Piece, recursive_move_list: list):
    
    if not colors_of_pieces_to_move:
        if len(recursive_move_list)  == 0:
            return
        
        move_instruction = StackMove(recursive_move_list, top_piece)
        # print("move_instruction in aux_get_all_psm " + str(move_instruction))
        instructions.append(move_instruction)
        return
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = loc.x + dx, loc.y + dy
        if 0 <= new_x < 5 and 0 <= new_y < 5:  
            new_loc = Location(new_x, new_y)
            if placeable(board, new_loc):  
                new_piece = Piece(new_loc, Orientation.HORIZONTAL, colors_of_pieces_to_move[0])  
                #piece_to_save = place_move(new_piece.color, new_loc, new_piece.orientation)
                
                board.get_cell(new_loc).pieces.insert(0, new_piece)
                new_recursive_move_list = copy.deepcopy(recursive_move_list)
                new_recursive_move_list.append(new_piece)
                # aux_inst_list.append(new_piece)
                
                aux_get_all_psm(board, new_loc, colors_of_pieces_to_move[1:], instructions, top_piece, new_recursive_move_list)
                                
                # new_recursive_move_list.pop()
                board.get_cell(new_loc).pieces.remove(new_piece)

#This function is used to undo the latest move the AI has made.
def undo_move(board: Board):
    #print(f'undo turn, current turn: {board.turn}')
    instruction = board.latest_move.pop()
    if isinstance(instruction, StackMove): #if it is a list it is a move instruction
        instruction: StackMove
        start_piece = instruction.start_cell
        for i in range(len(instruction.stack_moves)):
            piece:Piece = instruction.stack_moves[i]
            # print(f'removing piece: {piece.location}')
            board.get_cell(piece.location).remove_top_piece()
            # print(f'inserting piece: {start_piece.location}')
            board.get_cell(start_piece.location).pieces.insert(0, piece)
            #print(f"Undoing move: {piece.location}")

        return True 
    else: #otherwise it is a placementmove        
        instruction: PlacementMove
        piece:Piece = instruction.new_placement        
        board.get_cell(piece.location).remove_top_piece()
        color = piece.color
        # print(f"color: {color}")
        if color == Color.WHITE:
            board.white_pieces_placed -= 1
        else:    
            board.black_pieces_placed -= 1
        
        return True
#This function check if the player can actually unload a cell in the current board state. This function is called every time the player wants to unload a cell
# on the board.     
def check_unload(board: Board, player:Player):
    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col))
            curr_piece = cell.get_top_piece()
            if not cell.is_empty() and curr_piece.color == player.color and curr_piece.orientation != Orientation.VERTICAL:
                return True
    return False