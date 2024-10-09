import unittest
from game_ai import best_move, longest_road, center_control, edge_control, flat_stone_diff, score
from board import Board, Player, Color, Location, Orientation, Piece

class TestGameAi(unittest.TestCase):

    def setUp(self):
        # Setup the board and players
        self.board = Board()
        self.player1 = Player(Color.BLACK)
        self.player2 = Player(Color.WHITE)

    def test_best_move_easy(self):
        # Test bestMove for easy difficulty (random move)
        valid_moves = [('place', 1, 1, Orientation.HORIZONTAL), ('place', 2, 2, Orientation.VERTICAL)]
        move = best_move(valid_moves, 'easy')
        self.assertIn(move, valid_moves)

    def test_longest_road(self):
        # Test calculation of the longest road for player1
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 2)).pieces.append(Piece(Location(0, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 3)).pieces.append(Piece(Location(0, 3), Orientation.HORIZONTAL, Color.BLACK))
        
        longest_road = longest_road(self.board)
        self.assertEqual(longest_road, -3)

    def test_center_control(self):
        # Test center control calculation for player1
        self.board.get_cell(Location(2, 2)).pieces.append(Piece(Location(2, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(3, 3)).pieces.append(Piece(Location(3, 3), Orientation.HORIZONTAL, Color.BLACK))
        
        control = center_control(self.board)
        self.assertEqual(control, -2)

    def test_edge_control(self):
        # Test edge control calculation for player1
        self.board.get_cell(Location(0, 0)).pieces.append(Piece(Location(0, 0), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(4, 4)).pieces.append(Piece(Location(4, 4), Orientation.HORIZONTAL, Color.BLACK))
        
        control = edge_control(self.board)
        self.assertEqual(control, -2)

    def test_flat_stone_diff(self):
        # Test flat stone differential calculation between two players
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 2)).pieces.append(Piece(Location(0, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 3)).pieces.append(Piece(Location(0, 3), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 4)).pieces.append(Piece(Location(0, 4), Orientation.HORIZONTAL, Color.WHITE))
        
        diff = flat_stone_diff(self.board)
        self.assertEqual(diff, -2)

    def test_score(self):
        # Test score calculation for player1
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(2, 2)).pieces.append(Piece(Location(2, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(3, 3)).pieces.append(Piece(Location(3, 3), Orientation.HORIZONTAL, Color.BLACK))

        score_value = score(self.board)
        self.assertEqual(score_value, -18)

if __name__ == '__main__':
    unittest.main()