import unittest
from gameAi import bestMove, longestRoad, centerControl, edgeControl, flatStoneDiff, score
from board import Board, Player, Color, Location, Orientation, Piece

class TestGameAi(unittest.TestCase):

    def setUp(self):
        # Setup the board and players
        self.board = Board()
        self.player1 = Player(Color.BLACK)
        self.player2 = Player(Color.WHITE)

    def test_bestMove_easy(self):
        # Test bestMove for easy difficulty (random move)
        valid_moves = [('place', 1, 1, Orientation.HORIZONTAL), ('place', 2, 2, Orientation.VERTICAL)]
        move = bestMove(valid_moves, 'easy')
        self.assertIn(move, valid_moves)

    def test_longestRoad(self):
        # Test calculation of the longest road for player1
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 2)).pieces.append(Piece(Location(0, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 3)).pieces.append(Piece(Location(0, 3), Orientation.HORIZONTAL, Color.BLACK))
        
        longest_road = longestRoad(self.board)
        self.assertEqual(longest_road, -3)

    def test_centerControl(self):
        # Test center control calculation for player1
        self.board.get_cell(Location(2, 2)).pieces.append(Piece(Location(2, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(3, 3)).pieces.append(Piece(Location(3, 3), Orientation.HORIZONTAL, Color.BLACK))
        
        control = centerControl(self.board)
        self.assertEqual(control, -2)

    def test_edgeControl(self):
        # Test edge control calculation for player1
        self.board.get_cell(Location(0, 0)).pieces.append(Piece(Location(0, 0), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(4, 4)).pieces.append(Piece(Location(4, 4), Orientation.HORIZONTAL, Color.BLACK))
        
        control = edgeControl(self.board)
        self.assertEqual(control, -2)

    def test_flatStoneDiff(self):
        # Test flat stone differential calculation between two players
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 2)).pieces.append(Piece(Location(0, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 3)).pieces.append(Piece(Location(0, 3), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 4)).pieces.append(Piece(Location(0, 4), Orientation.HORIZONTAL, Color.WHITE))
        
        diff = flatStoneDiff(self.board)
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