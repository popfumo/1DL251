#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation, Location, Color

# Checks if a piece can be placed in a cell, returns True if there is no standing piece, False otherwise
def placeable(board, location):
    # Placeholder for now 
    curr_cell = board.get_cell(location)
    if curr_cell.is_empty() == False:
        if curr_cell.get_top_piece().orientation == Orientation.VERTICAL:
            return False
    return True


def are_adjacent(loc1, loc2):
    """
    Check if two locations are adjacent on the board.
    """
    if isinstance(loc1, Location) and isinstance(loc2, Location):
        return abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y) == 1
    else:
        raise TypeError("Both arguments must be Location objects")



def check_win(board, player):
    def find_connected_pieces(start_location):
        connected = set()
        to_check = [start_location]
        
        while to_check:
            current_location = to_check.pop(0)
            if current_location in connected:
                continue
            
            connected.add(current_location)
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = current_location.x + dx, current_location.y + dy
                if 0 <= new_x < 5 and 0 <= new_y < 5:
                    new_location = Location(new_x, new_y)
                    cell = board.get_cell(new_location)
                    top_piece = cell.get_top_piece()
                    if (top_piece and 
                        top_piece.color == player.color and 
                        top_piece.orientation == Orientation.HORIZONTAL and
                        new_location not in connected):
                        to_check.append(new_location)
        
        return connected

    # Check for a path from left to right
    for y in range(5):
        start_cell = board.get_cell(Location(0, y))
        start_piece = start_cell.get_top_piece()
        if start_piece and start_piece.color == player.color and start_piece.orientation == Orientation.HORIZONTAL:
            connected = find_connected_pieces(Location(0, y))
            if any(loc.x == 4 for loc in connected):
                return True

    # Check for a path from top to bottom
    for x in range(5):
        start_cell = board.get_cell(Location(x, 0))
        start_piece = start_cell.get_top_piece()
        if start_piece and start_piece.color == player.color and start_piece.orientation == Orientation.HORIZONTAL:
            connected = find_connected_pieces(Location(x, 0))
            if any(loc.y == 4 for loc in connected):
                return True

    return False