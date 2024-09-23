#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation

# Checks if a piece can be placed in a cell, returns True if there is no standing piece, False otherwise
def placeable(board, location):
    # Placeholder for now 
    curr_cell = board.get_cell(location)
    #if (curr_cell.is_empty() == False):
    if curr_cell.get_top_piece().orientation == Orientation.VERTICAL:
        return False
    return True

def check_win(board, player):
    """
    Check if the given player has won the game by finding a path of their pieces
    from one side of the board to the opposite side.
    
    Args:
    board (Board): The game board
    player (Player): The player to check for a win
    
    Returns:
    bool: True if the player has won, False otherwise
    """
    def are_adjacent(piece1, piece2):
        return abs(piece1.location.x - piece2.location.x) + abs(piece1.location.y - piece2.location.y) == 1

    def find_connected_pieces(start_piece):
        connected = set([start_piece])
        to_check = [start_piece]
        
        while to_check:
            current_piece = to_check.pop(0)
            for piece in player.pieces:
                if piece not in connected and are_adjacent(current_piece, piece) and piece.orientation == Orientation.HORIZONTAL:
                    connected.add(piece)
                    to_check.append(piece)
        
        return connected

    # Check for a path from left to right or top to bottom
    for piece in player.pieces:
        if piece.location.x == 0:
            connected = find_connected_pieces(piece)
            if any(p.location.x == 4 for p in connected):
                return True
        if piece.location.y == 0:
            connected = find_connected_pieces(piece)
            if any(p.location.y == 4 for p in connected):
                return True

    return False