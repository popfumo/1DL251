#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation, Color, Location
from game_logic import placeable

num_pieces = 21

# Places a piece in a cell, returns True if the piece was placed, False otherwise
# piece is placed at the front of the array
def place_piece(player, board, location, orientation):
    if player.pieces_placed < num_pieces:
        if placeable(board, location):
            new_piece = Piece(location, orientation, player)
            player.pieces.insert(0, new_piece)
            player.pieces_placed += 1
            board.get_cell(location).pieces.insert(0, new_piece)
            return True
        else:
            print("Cannot place piece")
            return False
    else:    
        print("No more pieces left")
        return False

# Moves a piece to a new location. Returns True if the piece was moved, False otherwise
# Checks if the piece can be placed in the new location by looking at the top piece of the cell at the new location
def move_piece(player, board, old_location, new_location):
    if(placeable(board, new_location)) and not board.get_cell(old_location).is_empty():
        top_piece = board.get_cell(old_location).get_top_piece()
        if(top_piece.orientation == Orientation.VERTICAL and top_piece.color != player.color):
            print("Cannot move piece because the top piece is a vertical piece or the top piece is not the player's piece") 
            return False
        piece_to_move = board.get_cell(top_piece.location).remove_top_piece()
        board.get_cell(new_location).pieces.insert(0, piece_to_move)
    else:
        print("Cannot move piece")


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

def test():
    p1_color = Color.BLACK
    p2_color = Color.WHITE
    player1 = Player(p1_color)
    player2 = Player(p2_color)
    b = Board()
    

