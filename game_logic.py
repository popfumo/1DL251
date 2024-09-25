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
    
def find_connected_pieces(board, player,start_location):
    connected = set([start_location])
    to_check = [start_location]
    
    while to_check:
        current_location = to_check.pop(0)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Check adjacent cells
            new_x, new_y = current_location.x + dx, current_location.y + dy
            if 0 <= new_x < 5 and 0 <= new_y < 5:  # Ensure we're within board boundaries
                new_location = Location(new_x, new_y)
                cell = board.get_cell(new_location)
                top_piece = cell.get_top_piece()
                if (top_piece and 
                    top_piece.color == player.color and 
                    top_piece.orientation == Orientation.HORIZONTAL and
                    new_location not in connected):
                    connected.add(new_location)
                    to_check.append(new_location)
    
    return connected

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

    # Check for a path from left to right
    for y in range(5):
        start_cell = board.get_cell(Location(0, y))
        start_piece = start_cell.get_top_piece()
        if start_piece and start_piece.color == player.color and start_piece.orientation == Orientation.HORIZONTAL:
            connected = find_connected_pieces(board, player, Location(0, y))
            if any(loc.x == 4 for loc in connected):
                return True

    # Check for a path from top to bottom
    for x in range(5):
        start_cell = board.get_cell(Location(x, 0))
        start_piece = start_cell.get_top_piece()
        if start_piece and start_piece.color == player.color and start_piece.orientation == Orientation.HORIZONTAL:
            connected = find_connected_pieces(board, player, Location(x, 0))
            if any(loc.y == 4 for loc in connected):
                return True

    return False

def getAllPossibleMoves(board,player):
    """
    Get all possible moves for a player.
    scenarios:
    cell is empty, place horizontal or vertical
    cell is not empty, is my color ontop? if yes, place horizontal or move
    cell is not empty, is my color ontop? if no, block
    cell is not empty, vertical piece ontop, cant do anything
    """
    moves = []
    for row in range(5):
        for col in range(5):
            cell = board.get_cell(Location(row, col)) # Get the cell at the current location
            if cell.is_empty(): # If the cell is empty, we can place a piece
                moves.append(('place',row, col, Orientation.HORIZONTAL))
                moves.append(('place',row, col, Orientation.VERTICAL))
            elif(cell.get_top_piece().color == player.color): #if the top piece is the same color as the player, we can move that pice or place a new one
                moves.append(('place',row, col, Orientation.HORIZONTAL))
                moves.append(('place',row, col, Orientation.VERTICAL))
                getflatStoneMoves(board, Location(row, col), moves)
            elif(cell.get_top_piece().orientation == Orientation.VERTICAL):#if the pice is vertical we cant do anything
                pass
            else: #if the cell is not empty and the top piece is not our, it is the opponents, we can only block
                moves.append(('place',row, col, Orientation.VERTICAL))
    return moves


"""
Gets all the flatstone moves for a given location and adds it to move list
"""
def getflatStoneMoves(board, location, moves):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #up, down, left, right
        new_x, new_y = location.x + dx, location.y + dy # get the new location
        if 0 <= new_x < 5 and 0 <= new_y < 5: #check if the new location is within the board
            if placeable(board, Location(new_x, new_y)): # check if the new location is placeable
                moves.append(('move', location.x, location.y, new_x, new_y)) # add the move to the list of moves
