#!/usr/bin/env python3

import copy
from board import Piece, Cell, Player, Board, Orientation, Location, Color, GameResult
from typing import List

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


# these are the targets when checking for a win from left to right and top to bottom
targets_right: List[Location] = [Location(4, 0), Location(4, 1), Location(4, 2), Location(4, 3), Location(4, 4)]
targets_bottom: List[Location] = [Location(0, 4), Location(1, 4), Location(2, 4), Location(3, 4), Location(4, 4)]

def check_win(board: Board) -> GameResult: 
    """
    Check if the either player has won the game by finding a path of their pieces
    from one side of the board to the opposite side.

    We check for both players since if player A moves a stack it might lead to player B having a winning path,
    thus it is not sufficient to check if player A has won after player A has made a move.

    Also a stack move can also lead to both players having a winning path, in that case the game is a draw. 
    This function needs to handle this as well.
    
    Args:
    board (Board): The game board
    
    Returns:
    bool: True if the player has won, False otherwise
    """
    
    winners = []
    for color in [Color.BLACK, Color.WHITE]:
        winpath_found = False
        # Check if the player has a winning path from left to right
        if not winpath_found:
            for x in range(board.num_x):
                # find a winning path for the player

                start_loc = Location(x, 0)
                if board.get_cell(start_loc).get_top_piece() != None and board.get_cell(start_loc).get_top_piece().color == color: # only check for winpaths if the top piece is the right color
                    winpath_found = check_win_aux(board, [], start_loc, targets_bottom)

                # if a winpath is found,
                if winpath_found:
                    winners.append(GameResult.victory_from_color(color))
                    break

        
        # Check if the player has a winning path from top to bottom
        if not winpath_found:
            for y in range(board.num_y):
                
                start_loc = Location(0, y)

                if board.get_cell(start_loc).get_top_piece() != None and board.get_cell(start_loc).get_top_piece().color == color: # only check for winpaths if the top piece is the right color
                    # This doesn't work, it returns true if a location is part of the target which is a set of locations
                    # So even if the ai or the player has placed only one piece its in the target location, it will return true
                    winpath_found = check_win_aux(board, [], start_loc, targets_right)

                # if a winpath is found,
                if winpath_found:
                    winners.append(GameResult.victory_from_color(color))
                    break

    if len(winners) == 2:
        return GameResult.DRAW
    elif len(winners) == 1:
        return winners[0]
    else:
        return GameResult.NOT_FINISHED
    
def check_win_aux(board:Board, visited: List[Cell], loc:Location, targets: List[Cell]) -> bool:
    if loc in targets:
        return True
    visited.append(loc)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = loc.x + dx, loc.y + dy
        if 0 <= new_x < 5 and 0 <= new_y < 5:  
            new_loc = Location(new_x, new_y)
            if new_loc not in visited:
                cell = board.get_cell(new_loc)
                if not cell.is_empty():
                    top_piece = cell.get_top_piece()
                    if top_piece.color == board.get_cell(loc).get_top_piece().color and top_piece.orientation == Orientation.HORIZONTAL:
                        return check_win_aux(board, visited, new_loc, targets)
                    
    return False

