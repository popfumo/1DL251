import unittest
from game_ai import AI_get_move, longest_road, center_control, edge_control, flat_stone_diff, score
from board import Board, Player, Color, Location, Orientation, Piece,MoveInstruction
from interaction_functions import place_piece, make_move_ai,get_all_possible_moves, undo_move

class TestGameAi(unittest.TestCase):

    def setUp(self):
        # Setup the board and players
        self.board = Board()
        self.player1 = Player(Color.BLACK)
        self.player2 = Player(Color.WHITE)

    def test_best_move_easy(self):
        # Test best_move for easy difficulty (random move)
        valid_moves = [('place', 1, 1, Orientation.HORIZONTAL), ('place', 2, 2, Orientation.VERTICAL)]
        move = AI_get_move(valid_moves, 'easy')
        self.assertIn(move, valid_moves)

    def test_longest_road(self):
        # Test calculation of the longest road for player1
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 2)).pieces.append(Piece(Location(0, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(0, 3)).pieces.append(Piece(Location(0, 3), Orientation.HORIZONTAL, Color.BLACK))
        
        the_longest_road = longest_road(self.board)
        self.assertEqual(the_longest_road, -3)

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
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 1)
        place_piece(player2.color, board, Location(2, 0), Orientation.HORIZONTAL)
        assert (board.white_pieces_placed == 1)
        place_piece(player1.color, board, Location(1, 0), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 2)

        diff = flat_stone_diff(board)
        self.assertEqual(diff, -1)

    def test_score(self):
        # Test score calculation for player1
        self.board.get_cell(Location(0, 1)).pieces.append(Piece(Location(0, 1), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(2, 2)).pieces.append(Piece(Location(2, 2), Orientation.HORIZONTAL, Color.BLACK))
        self.board.get_cell(Location(3, 3)).pieces.append(Piece(Location(3, 3), Orientation.HORIZONTAL, Color.BLACK))

        score_value = score(self.board)
        self.assertEqual(score_value, -12)

    def test_ai_move_place(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        piece = Piece(Location(1, 1),Orientation.HORIZONTAL, player2.color)

        
        new_instruction = MoveInstruction(piece)
        
        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 1)
        make_move_ai(board, new_instruction)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move_white == new_instruction)

    def test_ai_moving_move(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        start_location = Piece(Location(1, 0),Orientation.HORIZONTAL, player1.color)
        piece1 = Piece(Location(1, 1),Orientation.HORIZONTAL, player2.color)
        piece2 = Piece(Location(1, 2),Orientation.HORIZONTAL, player2.color)

        valid_moves = [start_location, piece1, piece2]
        make_move_ai(board, valid_moves)
        assert(board.get_cell(Location(1, 0)).is_empty())
        print(board.get_cell(Location(1, 1)).get_top_piece())
        print(piece1)
        assert(board.get_cell(Location(1, 1)).get_top_piece() == piece1)
        assert(board.get_cell(Location(1, 2)).get_top_piece() == piece2)
        assert(board.latest_move_white == [piece1, piece2])

    def test_place_after_finding_moves(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        possible_moves = get_all_possible_moves(board, player2.color)
        move = possible_moves[0]
        make_move_ai(board, move)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move_white == move)

    def test_ai_undo_move(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        possible_moves = get_all_possible_moves(board, player2.color)
        move = possible_moves[0]
        make_move_ai(board, move)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move == move)
        undo_move(board)
        assert (board.white_pieces_placed == 0)
        assert (board.get_cell(Location(0, 0)).is_empty())
        assert (board.latest_move == None)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        move2 = get_all_possible_moves(board, player2.color)
        some_move = move2[24]
        make_move_ai(board, some_move)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move == some_move)
        undo_move(board)
        assert (board.white_pieces_placed == 0)
        assert (board.latest_move == None)
        
    def test_simulate_game(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 1)
        print('board from test:')
        print(board)
        print(f'board from test, turn: {board.turn}, should be white')
        possible_moves = get_all_possible_moves(board, player2.color)
        move = AI_get_move(board, possible_moves, 'medium')
        make_move_ai(board, move)
        print('board from test:')
        print(board)
        print(f'board from test, turn: {board.turn}, should be white')

        print(f'white pieces placed: {board.white_pieces_placed}')

        assert (board.white_pieces_placed == 1)
        assert (board.latest_move.pop() == move)
        
if __name__ == '__main__':
    unittest.main()