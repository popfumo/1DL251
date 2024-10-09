#!/usr/bin/env python3

from board import Piece, Cell, Player, Board, Orientation, Location, Color
from interaction_functions import getAllPossibleMoves

# Checks if a piece can be placed in a cell, returns True if there is no standing piece, False otherwise
def placeable(board, location):
    curr_cell = board.get_cell(location)
    return curr_cell.is_empty() or curr_cell.get_top_piece().orientation == Orientation.HORIZONTAL
    # i rewrote this function to make it more readable, but the replaced code is below /edvin
    # if not curr_cell.is_empty() and curr_cell.get_top_piece().orientation == Orientation.VERTICAL:
    #     return False
    # return True


def are_adjacent(loc1, loc2):
    """
    Check if two locations are adjacent on the board.
    """
    if isinstance(loc1, Location) and isinstance(loc2, Location):
        return abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y) == 1
    else:
        raise TypeError("Both arguments must be Location objects")

def find_connected_pieces(board, player_color:Color,start_location):
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
                    top_piece.color == player_color and 
                    top_piece.orientation == Orientation.HORIZONTAL and
                    new_location not in connected):
                    connected.add(new_location)
                    to_check.append(new_location)
    
    return connected

def check_win(board, player_color:Color):
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
        if start_piece and start_piece.color == player_color and start_piece.orientation == Orientation.HORIZONTAL:
            connected = find_connected_pieces(board, player_color, Location(0, y))
            if any(loc.x == 4 for loc in connected):
                return True

    # Check for a path from top to bottom
    for x in range(5):
        start_cell = board.get_cell(Location(x, 0))
        start_piece = start_cell.get_top_piece()
        if start_piece and start_piece.color == player_color and start_piece.orientation == Orientation.HORIZONTAL:
            connected = find_connected_pieces(board, player_color, Location(x, 0))
            if any(loc.y == 4 for loc in connected):
                return True

    return False

def game_over(board, player1, player2):
    """
    Check if the game is over (either a win or a stalemate).

    Args:
    board: The current game board state.
    player1: The first player.
    player2: The second player.

    Returns:
    bool: True if the game is over, otherwise False.
    """
    # Check if player1 has won
    if check_win(board, player1):
        return True
    
    # Check if player2 has won
    if check_win(board, player2):
        return True

    # Check if both players have no valid moves left (stalemate)
    if not getAllPossibleMoves(board, player1) and not getAllPossibleMoves(board, player2):
        return True  # No moves left for either player
    
    return False  # Game is not over

# Returns a list containing the possible boards that can be created after each possible move has been made

