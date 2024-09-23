#!/usr/bin/env python3

from enum import Enum

#The maximum number of pieces that can be placed
NUM_PIECES = 21

class Color(Enum):
    BLACK = 1
    WHITE = 2

class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2



# Initializes a cell with a empty list of pieces
class Cell:
    def __init__(self):
        self.pieces = []
    def __repr__(self):
        return f"{self.pieces}"
    def get_top_piece(self):
        if len(self.pieces) > 0:
            return self.pieces[0]
    def is_empty(self):
        return len(self.pieces) == 0
    def remove_top_piece(self):
        if len(self.pieces) > 0:
            return self.pieces.pop(0)

class Location:
    # x and y both start at 0 and end at 4
    def __init__(self, x, y):
        if x < 0 or x > 4 or y < 0 or y > 4:
            raise IndexError("the coordinate must be within 5*5 boundaries")
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{self.x}, {self.y}"
# Initializes a player with 0 pieces placed so far
class Player:
    def __init__(self, color):
        self.pieces = []
        self.pieces_placed = 0
        self.color = color

# Initializes a board with 25 cells
class Board:
    def __init__(self):
        # (0, 0) would be the top left
        self.cells = [[Cell() for _ in range(5)] for _ in range(5)]
        # determine which whose turn is it, black goes first
        # todo: check whose turn it is
        self.turn = 0
    def __str__(self):
        return f"{self.cells}"
    # Returns the pieces in a cell
    def get_cell(self, location):
        return self.cells[location.x][location.y]

class Piece:
    def __init__(self, location, orientation, color):
        self.location = location
        self.orientation = orientation
        self.color = color
    def __repr__(self):
        return f"{self.location} {self.orientation}"



