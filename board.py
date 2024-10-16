#!/usr/bin/env python3
import copy
from typing import List
from enum import Enum
from dataclasses import dataclass

#The maximum number of pieces that can be placed
NUM_PIECES = 21

class Color(Enum):
    BLACK = 1
    WHITE = 2
    def from_id(id):
        # print("from_id: " + id.__str__())
        if id == 1:
            return Color.BLACK
        elif id == 2:
            return Color.WHITE
        else:
            raise ValueError("Invalid color id")
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE

class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class GameResult(Enum):
    VICTORY_BLACK = Color.BLACK.value
    VICTORY_WHITE = Color.WHITE.value
    NOT_FINISHED = 0
    DRAW = -1
    def victory_from_color(color:Color):    
        return GameResult.VICTORY_BLACK if color == Color.BLACK else GameResult.VICTORY_WHITE


class Cell:
# Initializes a cell with a empty list of pieces
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
    def remove_bottom_piece(self):
        if len(self.pieces) > 0:
            return self.pieces.pop()
    
class Location:
    # x and y both start at 0 and end at 4
    def __init__(self, x, y):
        if x < 0 or x > 4 or y < 0 or y > 4:
            raise IndexError("the coordinate must be within 5*5 boundaries")
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Location({self.x},{self.y})"

    def __eq__(self, other):
        return isinstance(other, Location) and self.x == other.x and self.y == other.y
    
    def __ne__(self, value):
        return self.x != value.x or self.y != value.y
    
    def __hash__(self):
        return hash((self.x, self.y))

# class PlaceMove:
#     def __init__(self, piece_color:Color, location:Location, orientation:Orientation):
#         self.piece_color = piece_color
#         self.location = location
#         self.orientation = orientation
#     
#     def __eq__(self, value):
#         return self.piece_color == value.piece_color and self.location == value.location and self.orientation == value.orientation

class Piece:
    def __init__(self, location: Location, orientation: Orientation, color: Color):
        self.location = location
        self.orientation = orientation
        self.color = color
    def __repr__(self):
        return f"{self.location} {self.orientation}"
    
    def __eq__(self, other):
        if isinstance(other, Piece):
            return (self.location == other.location and
                    self.orientation == other.orientation and
                    self.color == other.color)
    

class MoveType(Enum):
    STACKMOVE = 1
    PLACEMENTMOVE = 2

class MoveInstruction: # used to represent a move, either a placement or a stack move
        move_type: MoveType
        def get_move_type(self) -> MoveType:
            return self.move_type

class StackMove(MoveInstruction):
    def __init__(self, smoves: List[Piece], start_cell):
        assert len(smoves) > 0
        self.stack_moves = smoves
        self.start_cell = start_cell
        self.move_type = MoveType.STACKMOVE
    def __str__(self):
        return f"StackMove: {self.stack_moves} from {self.start_cell}"

class PlacementMove(MoveInstruction):
    def __init__(self, new_placement:Piece):
        self.new_placement: Piece = new_placement
        self.move_type = MoveType.PLACEMENTMOVE
    def is_equal(self, loc:Location, orientation:Orientation):
        return self.new_placement.location.x == loc.x and self.new_placement.location.y == loc.y and self.new_placement.orientation == orientation
    
    def __str__(self):
        return f"PlacementMove: {self.new_placement}"
    # def __eq__(self, value):
    #     return self.new_placement.location.x == value.new_placement.location. and self.move_type == value.move_type 
    
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

        # Only to be used by AI
        self.latest_move = []

    def __str__(self):
        string = ""
        for row in self.cells:
            for cell in row:
                string += f"{cell} "
            string += "\n"
        return string
    # Returns the pieces in a cell
    def get_cell(self, location):        return self.cells[location.x][location.y]
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

