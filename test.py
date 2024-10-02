import unittest
from unittest.mock import patch
from io import StringIO
from board import Board, Player, Color, Location, Orientation, Piece
from game import game
from interaction_functions import place_piece, unload_piece_recursive, getAllPossibleMoves
from gameAi import longestRoad

class TestGame(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player(Color.BLACK)
        self.player2 = Player(Color.WHITE)

    def test_place_piece(self):
        # Test placing a piece
        result = place_piece(self.player2, self.board, Location(1, 1), Orientation.HORIZONTAL)
        self.assertTrue(result)
        self.assertEqual(len(self.board.get_cell(Location(1, 1)).pieces), 1)
        self.assertEqual(self.board.get_cell(Location(1, 1)).pieces[0].color, Color.WHITE)

    def test_piece_creation(self):
        # Test correct piece creation
        piece = Piece(Location(0, 0), Orientation.HORIZONTAL, self.player1)
        self.assertEqual(piece.color, Color.BLACK)
        self.assertIsInstance(piece.color, Color)

    def test_piece_placement(self):
        # Test piece placement and retrieval
        place_piece(self.player1, self.board, Location(0, 0), Orientation.HORIZONTAL)
        cell = self.board.get_cell(Location(0, 0))
        self.assertEqual(len(cell.pieces), 1)
        top_piece = cell.get_top_piece()
        self.assertIsInstance(top_piece, Piece)
        self.assertEqual(top_piece.color, Color.BLACK)

    def test_multiple_piece_placement(self):
        # Test multiple piece placement
        place_piece(self.player1, self.board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(0, 0), Orientation.HORIZONTAL)
        cell = self.board.get_cell(Location(0, 0))
        self.assertEqual(len(cell.pieces), 2)
        top_piece = cell.get_top_piece()
        self.assertEqual(top_piece.color, Color.WHITE)

    @patch('builtins.input', side_effect=['0', '0', '1'])
    def test_unload_piece_color_check(self, mock_input):
        # Set up the board state
        place_piece(self.player1, self.board, Location(0, 0), Orientation.HORIZONTAL)
        
        # Attempt to unload with the wrong player
        result = unload_piece_recursive(self.player2, self.board, 1, Location(0, 0), Location(0, 0))
        self.assertFalse(result)

    @patch('builtins.input', side_effect=['0', '0', '1', 'e'])
    def test_successful_unload(self, mock_input):
        # Set up the board state
        place_piece(self.player1, self.board, Location(0, 0), Orientation.HORIZONTAL)
        
        # Attempt to unload with the correct player
        result = unload_piece_recursive(self.player1, self.board, 1, Location(0, 0), Location(0, 0))
        self.assertTrue(result)
        self.assertEqual(len(self.board.get_cell(Location(0, 0)).pieces), 0)
        self.assertEqual(len(self.board.get_cell(Location(0, 1)).pieces), 1)

    @patch('builtins.input', side_effect=['3', '0', '0', '1', 'e', 'q'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_game_flow_with_unload(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit):
            game()

        output = mock_stdout.getvalue()
        self.assertIn("Attempting to unload from location: 0, 0", output)
        self.assertNotIn("The top piece in this cell is not yours.", output)

    def test_longest_road_for_WHITE(self):
        # Test longest road calculation
        place_piece(self.player1, self.board, Location(0, 1), Orientation.HORIZONTAL)
        place_piece(self.player1, self.board, Location(0, 2), Orientation.HORIZONTAL)
        place_piece(self.player1, self.board, Location(0, 3), Orientation.HORIZONTAL)
        place_piece(self.player1, self.board, Location(1, 3), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(1, 0), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(2, 0), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(3, 0), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(4, 0), Orientation.HORIZONTAL)

        longest_road_p1 = longestRoad(self.board)
        self.assertEqual(longest_road_p1, 5)

    def test_longest_road_for_BLACK(self):
        # Test longest road calculation
        place_piece(self.player1, self.board, Location(0, 1), Orientation.HORIZONTAL)
        place_piece(self.player1, self.board, Location(0, 2), Orientation.HORIZONTAL)
        place_piece(self.player1, self.board, Location(0, 3), Orientation.HORIZONTAL)
        place_piece(self.player1, self.board, Location(1, 3), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(self.player2, self.board, Location(1, 0), Orientation.HORIZONTAL)

        longest_road_p1 = longestRoad(self.board)
        self.assertEqual(longest_road_p1, -4)
    
    def test_getAllPossibleMoves(self):
        # Create a board with some initial pieces
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player1, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player1, board, Location(0, 0), Orientation.HORIZONTAL)
        
        # Get all possible moves
        possible_moves = getAllPossibleMoves(board, player1)
        
        # Assert the number of possible moves

        assert len(possible_moves) == 53
       



if __name__ == '__main__':
    unittest.main()