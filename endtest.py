import unittest
from board import Board, Player, Color, Location, Orientation, Piece
from game import game, get_player_move
from interaction_functions import place_piece, unload_piece_recursive
from game_logic import check_win

#I just wanted to test the win function, couldn't be bothered to run all the tests at the same time.

class TestGame(unittest.TestCase):
    # ... [previous test methods remain unchanged] ...

    def test_check_win_horizontal(self):
        board = Board()
        player = Player(Color.BLACK)
        
        # Place a horizontal line of pieces from left to right
        for x in range(5):
            place_piece(player, board, Location(x, 2), Orientation.HORIZONTAL)
        
        self.assertTrue(check_win(board, player))

    def test_check_win_vertical(self):
        board = Board()
        player = Player(Color.WHITE)
        
        # Place a vertical line of pieces from top to bottom
        for y in range(5):
            place_piece(player, board, Location(2, y), Orientation.HORIZONTAL)
        
        self.assertTrue(check_win(board, player))

    def test_no_win(self):
        board = Board()
        player = Player(Color.BLACK)
        
        # Place some pieces but not in a winning configuration
        place_piece(player, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player, board, Location(2, 2), Orientation.HORIZONTAL)
        
        self.assertFalse(check_win(board, player))

    def test_win_with_gaps(self):
        board = Board()
        player = Player(Color.WHITE)
        
        # Place pieces with gaps, but still forming a winning path
        place_piece(player, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player, board, Location(2, 0), Orientation.HORIZONTAL)
        place_piece(player, board, Location(3, 1), Orientation.HORIZONTAL)
        place_piece(player, board, Location(4, 0), Orientation.HORIZONTAL)
        
        self.assertTrue(check_win(board, player))

    def test_vertical_piece_blocking(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        
        # Place a horizontal line for player1
        for x in range(5):
            place_piece(player1, board, Location(x, 2), Orientation.HORIZONTAL)
        
        # Place a vertical piece in the middle to block the path
        place_piece(player2, board, Location(2, 2), Orientation.VERTICAL)
        
        self.assertFalse(check_win(board, player1))

if __name__ == '__main__':
    unittest.main()