import unittest
from unittest.mock import patch
from io import StringIO
from board import Board, Player, Color, Location, Orientation, Piece
from game import game
from interaction_functions import place_piece, unload_piece_recursive, get_all_possible_moves, check_unload
from game_ai import flat_stone_diff, longest_road, AI_get_move

class TestGame(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player(Color.BLACK)
        self.player2 = Player(Color.WHITE)

    def test_place_piece(self):
        # Test placing a piece
        result = place_piece(self.player2.color, self.board, Location(1, 1), Orientation.HORIZONTAL)
        self.assertTrue(result)
        self.assertEqual(len(self.board.get_cell(Location(1, 1)).pieces), 1)
        self.assertEqual(self.board.get_cell(Location(1, 1)).pieces[0].color, Color.WHITE)

    def test_piece_creation(self):
        # Test correct piece creation
        piece = Piece(Location(0, 0), Orientation.HORIZONTAL, self.player1.color)
        self.assertEqual(piece.color, Color.BLACK)
        self.assertIsInstance(piece.color, Color)

    def test_piece_placement(self):
        # Test piece placement and retrieval
        place_piece(self.player1.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        cell = self.board.get_cell(Location(0, 0))
        self.assertEqual(len(cell.pieces), 1)
        top_piece = cell.get_top_piece()
        self.assertIsInstance(top_piece, Piece)
        self.assertEqual(top_piece.color, Color.BLACK)

    def test_multiple_piece_placement(self):
        # Test multiple piece placement
        place_piece(self.player1.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        cell = self.board.get_cell(Location(0, 0))
        self.assertEqual(len(cell.pieces), 2)
        top_piece = cell.get_top_piece()
        self.assertEqual(top_piece.color, Color.WHITE)

    # @patch('builtins.input', side_effect=['0', '0', '1'])
    # def test_unload_piece_color_check(self, mock_input):
    #     # Set up the board state
    #     place_piece(self.player1.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        
    #     # Attempt to unload with the wrong player
    #     result = unload_piece_recursive(self.player2, self.board, 1, Location(0, 0), Location(0, 0))
    #     self.assertFalse(result)

    # @patch('builtins.input', side_effect=['0', '0', '1', 'e'])
    # def test_successful_unload(self, mock_input):
    #     # Set up the board state
    #     place_piece(self.player1.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        
    #     # Attempt to unload with the correct player
    #     result = unload_piece_recursive(self.player1, self.board, 1, Location(0, 0), Location(0, 0))
    #     self.assertTrue(result)
    #     self.assertEqual(len(self.board.get_cell(Location(0, 0)).pieces), 0)
    #     self.assertEqual(len(self.board.get_cell(Location(0, 1)).pieces), 1)

    # @patch('builtins.input', side_effect=['3', '0', '0', '1', 'e', 'q'])
    # @patch('sys.stdout', new_callable=StringIO)
    

    def test_longest_road_for_white(self):
        # Test longest road calculation
        place_piece(self.player1.color, self.board, Location(0, 1), Orientation.HORIZONTAL)
        place_piece(self.player1.color, self.board, Location(0, 2), Orientation.HORIZONTAL)
        place_piece(self.player1.color, self.board, Location(0, 3), Orientation.HORIZONTAL)
        place_piece(self.player1.color, self.board, Location(1, 3), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(1, 0), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(2, 0), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(3, 0), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(4, 0), Orientation.HORIZONTAL)

        longest_road_p1 = longest_road(self.board)
        self.assertEqual(longest_road_p1, 5)

    def test_longest_road_for_black(self):
        # Test longest road calculation
        place_piece(self.player1.color, self.board, Location(0, 1), Orientation.HORIZONTAL)
        place_piece(self.player1.color, self.board, Location(0, 2), Orientation.HORIZONTAL)
        place_piece(self.player1.color, self.board, Location(0, 3), Orientation.HORIZONTAL)
        place_piece(self.player1.color, self.board, Location(1, 3), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(self.player2.color, self.board, Location(1, 0), Orientation.HORIZONTAL)

        longest_road_p1 = longest_road(self.board)
        self.assertEqual(longest_road_p1, -4)

    def test_longest_road_snake(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        # This is the snake path that is tested in this test
        #  |X|X| | | |
        #  | |x| | | |
        #  | |x| | | |
        #  | |x| | | |
        #  | |x| | | |

        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(4, 1), Orientation.HORIZONTAL)

        longest_road_p1 = longest_road(board)
        self.assertEqual(longest_road_p1, -6)

    def test_snakier_snake(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        # This is the snake path that is tested in this test
        #  |B|B| | | |
        #  | |B|B|B| |
        #  | | | |B| |
        #  | | | |B| |
        #  | | | |B| |
        
        place_piece(player1.color, board, Location(0,0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(4,3), Orientation.HORIZONTAL)


        longest_road_p1 = longest_road(board)
        print(longest_road_p1)
        self.assertEqual(longest_road_p1, -8)

    def test_snake_with_diversions(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
                
        #  |B|B| | | |
        #  | |B|B|B|B|
        #  | |B| |B| |
        #  | | | |B|B|
        #  | | | |B| |
        
        place_piece(player1.color, board, Location(0,0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,4), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(4,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3,4), Orientation.HORIZONTAL)

        longest_road_p1 = longest_road(board)
        self.assertEqual(longest_road_p1, -8)

    def test_get_all_possible_moves_middle_1(self):
        # Create a board with some initial pieces
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        
        
        # Get all possible moves
        possible_moves = get_all_possible_moves(board, player1.color)

        #print(possible_moves[-1])
        
        #print(f'middle test possible moves: {len(possible_moves)}')
        
        assert (len(possible_moves) == (25 +25+ 4)) # 25 flat placements, 25 standing placements, 4 piece-movements available         
        # Assert the number of possible moves
        
    def test_get_all_possible_moves_middle_2(self):
        # Create a board with some initial pieces
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        # place a stack of two pieces of your own color in the middle
        place_piece(player1.color, board, Location(2, 2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2, 2), Orientation.HORIZONTAL)
        
        # Get all possible moves
        possible_moves = get_all_possible_moves(board, player1.color)
        
        assert (len(possible_moves) == (25 + 25 + 4 + 4*4)) # 25 flat placements, 25 standing placements, 4 (move 1) + 4*4 (move 2) piece-movements available
        # Assert the number of possible moves

    def test_get_all_possible_moves_middle_3(self):
        # Create a board with some initial pieces
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(2, 2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2, 2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2, 2), Orientation.HORIZONTAL)
        
        # Get all possible moves
        possible_moves = get_all_possible_moves(board, player1.color)

        #print(f'board: {board}')
        
        # Assert the number of possible moves
        # 25 flat placements, 25 standing placements, 4 (move 1) + 4*4 (move 2) + 4*4*4 (move 3) - 4 because we hit the edge of the board 4 times when moving 3, piece-movements available
        #print(f'middle test possible moves 3: {len(possible_moves)}')
        assert (len(possible_moves) == (25 + 25 + 4 + 4*4 + 4*4*4) - 4)
        
       
    def test_piece_count(self):
        # Test the number of pieces placed
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 1)
        place_piece(player2.color, board, Location(2, 0), Orientation.HORIZONTAL)
        assert (board.white_pieces_placed == 1)
        place_piece(player1.color, board, Location(1, 0), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 2)

    def test_invalid_unload(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        assert(check_unload(board, player1) == True)
        place_piece(player2.color, board, Location(0,0), Orientation.HORIZONTAL)
        assert(check_unload(board, player1) == False)
        assert(check_unload(board, player2) == True)
        place_piece(player1.color, board, Location(0, 0), Orientation.VERTICAL)
        assert(check_unload(board, player1) == False)
        assert(check_unload(board, player2) == False)
        place_piece(player1.color, board, Location(1, 0), Orientation.HORIZONTAL)
        assert(check_unload(board, player1) == True)

    # def test_move(self):
    #     board = Board()
    #     player1 = Player(Color.BLACK)
    #     player2 = Player(Color.WHITE)

    #     Piece2 = Piece(Location(1,0), Orientation.HORIZONTAL, player2.color)
        
    #     board.get_cell(Piece2.location).pieces.insert(0, Piece2) 
    #     board.get_cell(Piece2.location).pieces.insert(0, Piece2) 
    #     board.get_cell(Piece2.location).pieces.insert(0, Piece2) 
    #     board.get_cell(Piece2.location).pieces.insert(0, Piece2)

    #     all_moves = get_all_possible_moves(board, player2.color)

    #     #print(board)
    #     moves_to_test = all_moves[50:]
    #     #print(f'moves_to_test: {moves_to_test}')
    #     #best_moves = AI_get_move(board, moves_to_test, "medium")


    #     print(board)


    def test_flatstone_diff_score(self):
        board = Board()
        player2 = Player(Color.BLACK)
        player1 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(2, 1), Orientation.HORIZONTAL)      
        place_piece(player2.color, board, Location(2, 3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 2), Orientation.HORIZONTAL)
        place_piece(player2.color, board, Location(3, 2), Orientation.HORIZONTAL)   
        place_piece(player1.color, board, Location(2, 2), Orientation.HORIZONTAL)
        place_piece(player2.color, board, Location(2, 4), Orientation.HORIZONTAL)

        Score = flat_stone_diff(board)

        #print(Score)

        assert(Score == 0)

        


if __name__ == '__main__':
    unittest.main()