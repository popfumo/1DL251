#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation, Color, Location
from game_logic import placeable, are_adjacent

num_pieces = 21

# Places a piece in a cell, returns True if the piece was placed, False otherwise
# piece is placed at the front of the array
########################################################################################
#               IMPORTANT NOTE                                                         #                    
#Due to how we have implemented placing a new move the AI will use more then 21 stones #
#either we have to change so the AI can use more then 21 stones or some other option   #                                         
#                                               #                                      # 
########################################################################################
def place_piece(player, board, location, orientation):     
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
def move_piece(player, board, old_location, new_location):
    if placeable(board, new_location) and not board.get_cell(old_location).is_empty() and old_location != new_location and are_adjacent(old_location, new_location) :
        top_piece = board.get_cell(old_location).get_top_piece()
        if top_piece.orientation == Orientation.VERTICAL and top_piece.color != player.color:
            print("Cannot move piece because the top piece is a vertical piece or the top piece is not the player's piece") 
            return False
        piece_to_move = board.get_cell(top_piece.location).remove_top_piece()
        piece_to_move.location = new_location
        board.get_cell(new_location).pieces.insert(0, piece_to_move)
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


#############################################################################################
#               IMPORTANT NOTE                                                              #              
#Might have a bug where some stones in a stack dissapear when unloading, lets say we have a #
#stack of 4 stones and we want to move 2, after we move will the stack be 2 or 4?           #
#                                               #                                           #
#  ex: We want 1) to happen but does it?                                                    #
#                                                                                           #                                          
#    [x             what might happen: [x                                                   #
# 1)  x        [x                       x                                                   #
#     x         x                       x                                                   #
#     x] -> [x] x]                      x] -> [x][x]                                        #
#                                                                                           #                                              
# does this happen? IDK? i dont do testing                                                  #                
#############################################################################################

def getAllPossibleMoves(board : Board, player: Player):
    """
    TODO: implement so the roads can turn
    This function will create a list of boards, it will take the current board and make a copy of it, 
    it will then create a new board for each possible move that can be made and append to a list.
    """
    # this new_boards variable holds all the new boards that can be "made" by all the performing all possible moves
    # the idea is that we iterate over this when checking the score for each move, and then picking the board we want depending on the AI difficulty
    # not the most efficient approach with regards to performance, but i think it will do /edvin & viktor
    new_boards = []
    for row in range(board.num_x):
        for col in range(board.num_y):
            cell = board.get_cell(Location(row, col)) # Get the cell at the current location
            
            # Add all possible boards that can be created after placing a new piece.
            # If the cell is empty or has a horizontal piece on top, we can place a piece
            if cell.is_empty() or cell.get_top_piece().orientation == Orientation.HORIZONTAL: 
                new_horizontal_board: Board = board.copy()
                place_piece(player, new_horizontal_board, Location(row,col), Orientation.HORIZONTAL)                
                new_boards.append(new_horizontal_board)

                new_vertical_board: Board = board.copy()
                place_piece(player, new_vertical_board, Location(row,col), Orientation.VERTICAL)                
                new_boards.append(new_vertical_board)
            
            # Add all possible boards that can be created after moving a stack.
            # This is much more complex than placing a new piece, as the ways in which you can move a stack are much greater in numbers
            if not cell.is_empty(): # apparently python does not have lazy evaluation of if statements, hence this is nested
                if cell.get_top_piece().color == player.color:
                    # Our color is on top of this cell, meaning we can move as many pieces as we want in this stack.
                    
                    # How many pieces do we want to move from the stack? This for loop iterates over the different possible amounts
                    for num_pieces_to_move in range(1, len(cell.pieces) + 1):
                        # Where do we want to place the pieces that we move from the stack? This for loop iterates over the different possible placement combinations
                        x,y = cell.location.x, cell.location.y
                        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        for dx, dy in directions: # Check adjacent cells
                            path = []
                            remaining_pieces = num_pieces_to_move
                            new_x, new_y = x + dx, y + dy
                            while (0 <= new_x < board.num_x and 0 <= new_y < board.num_y and remaining_pieces > 0):
                                if placeable(board, Location(new_x, new_y)):
                                    path.append(Location(new_x, new_y))
                                    remaining_pieces -= 1
                                    
                                new_x += dx
                                new_y += dy
                            
                            if path:
                                new_board = board.copy()
                                unload_cell(player, new_board, Location(x, y), path)
                                new_boards.append(new_board)
    
    return new_boards

def test():
    p1_color = Color.BLACK
    p2_color = Color.WHITE
    player1 = Player(p1_color)
    player2 = Player(p2_color)
    b = Board()
    

