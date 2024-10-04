#!/usr/bin/env python3
import copy


from enum import Enum

#The maximum number of pieces that can be placed
NUM_PIECES = 21

class Color(Enum):
    BLACK = 1
    WHITE = 2
    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE

class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2



# Initializes a cell with a empty list of pieces
class Cell:
    def __init__(self, x, y):
        self.pieces = []
        self.location = Location(x, y)
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

    def __eq__(self, other):
        return isinstance(other, Location) and self.x == other.x and self.y == other.y
    
    def __ne__(self, value):
        return self.x != value.x or self.y != value.y
    
    def __hash__(self):
        return hash((self.x, self.y))


# Initializes a player with 0 pieces placed so far
class Player:
    def __init__(self, color):
        # self.pieces = []
        self.pieces_placed = 0
        self.color = color

# Initializes a board with 25 cells
class Board:
    num_x: int
    num_y: int
    def __init__(self):
        # (0, 0) would be the top left
        self.num_x = 5
        self.num_y = 5
        self.cells = [[Cell(row, col) for col in range(self.num_x)] for row in range(self.num_y)]
        # determine which whose turn is it, black goes first
        # todo: check whose turn it is

        # As per game requirment, black goes first
        self.turn = Color.BLACK
        self.white_pieces_placed = 0
        self.black_pieces_placed = 0

    def __str__(self):
        string = ""
        for row in self.cells:
            for cell in row:
                string += f"{cell} "
            string += "\n"
        return string
    # Returns the pieces in a cell
    def get_cell(self, location):
        return self.cells[location.x][location.y]
    def copy(self):
        return copy.deepcopy(self)
    def white_to_move(self):
        return self.turn == Color.WHITE
    def switch_turn(self):
        self.turn = self.turn.opposite()
    
    def __eq__(self, value: object) -> bool:
        rval:bool = isinstance(value, Board)
        for x in range(self.num_x):
            for y in range(self.num_y):
                rval = rval and self.cells[x][y].pieces == value.cells[x][y].pieces
        return rval         

class Piece:
    def __init__(self, location, orientation, color):
        self.location = location
        self.orientation = orientation
        self.color = color
    def __repr__(self):
        return f"{self.location} {self.orientation}"
