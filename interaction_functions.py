#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation, Color, Location
from game_logic import placeable, are_adjacent

num_pieces = 21

# Places a piece in a cell, returns True if the piece was placed, False otherwise
# piece is placed at the front of the array
def place_piece(player, board, location, orientation):
    if player.pieces_placed < num_pieces:  # Use the constant NUM_PIECES instead of num_pieces
        if placeable(board, location):
            new_piece = Piece(location, orientation, player)  # Use player.color instead of player
            player.pieces.insert(0, new_piece)
            player.pieces_placed += 1
            board.get_cell(location).pieces.insert(0, new_piece)
            print(f"Piece placed at {location} with color {player.color}")  # Debug print
            return True
        else:
            print(f"Cannot place piece at {location}")
            return False
    else:    
        print("No more pieces left")
        return False

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
        top_piece = board.cells[old_location].get_top_piece()
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

    print(f"Top piece: Color - {top_piece.color}, Orientation - {top_piece.orientation}")
    print(f"Current player color: {player.color}")

    if top_piece.color != player.color:
        print(f"Cannot unload this piece. Color mismatch: Piece color {top_piece.color}, Player color {player.color}")
        return False
    
    if top_piece.orientation == Orientation.VERTICAL:
        print("Cannot unload this piece. It's vertical.")
        return False

    directions = {"n": (-1, 0), "e": (0, 1), "s": (1, 0), "w": (0, -1)}
    
    while True:
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

# TODO: Decide who implements this function, AI team or Board team? 

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

def test():
    p1_color = Color.BLACK
    p2_color = Color.WHITE
    player1 = Player(p1_color)
    player2 = Player(p2_color)
    b = Board()
    

