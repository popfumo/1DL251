import unittest
from game_ai import AI_get_move, longest_road, center_control, edge_control, flat_stone_diff, score
from board import Board, Player, Color, Location, Orientation, Piece,MoveInstruction, StackMove, PlacementMove, GameResult
from interaction_functions import place_piece, make_move_ai,get_all_possible_moves, undo_move
from game_logic import check_win
from game import check_game_end
import copy 

class TestGameAi(unittest.TestCase):

    def setUp(self):
        # Setup the board and players
        self.board = Board()
        self.player1 = Player(Color.BLACK)
        self.player2 = Player(Color.WHITE)

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
        self.assertEqual(score_value, -18)

    def test_ai_move_place(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        piece = Piece(Location(1, 1),Orientation.HORIZONTAL, player2.color)
        
        new_placementmove = PlacementMove(piece)
        
        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 1)
        make_move_ai(board, new_placementmove)
        assert (board.white_pieces_placed == 1)
        
        assert (board.latest_move.pop() == new_placementmove)


    def test_ai_moving_move(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        start_location = Piece(Location(1, 0),Orientation.HORIZONTAL, player1.color)
        piece1 = Piece(Location(1, 1),Orientation.HORIZONTAL, player2.color)
        piece2 = Piece(Location(1, 2),Orientation.HORIZONTAL, player2.color)
        
        stack_move: StackMove = StackMove([piece1, piece2], start_location)
        make_move_ai(board, stack_move)
        
        assert(board.get_cell(Location(1, 0)).is_empty())
        # print(board.get_cell(Location(1, 1)).get_top_piece())
        # print(piece1)
        assert(board.get_cell(Location(1, 1)).get_top_piece() == piece1)
        assert(board.get_cell(Location(1, 2)).get_top_piece() == piece2)
        assert(board.latest_move.pop() == stack_move)


    def test_place_after_finding_moves(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        possible_moves = get_all_possible_moves(board, player2.color)

        move: MoveInstruction = possible_moves[0]
        make_move_ai(board, move)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move.pop() == move)


    def test_ai_undo_move(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        possible_moves = get_all_possible_moves(board, player2.color)
        move: MoveInstruction = possible_moves[0]
        make_move_ai(board, move)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move[-1] == move)
        undo_move(board)
        assert (board.white_pieces_placed == 0)
        assert (board.get_cell(Location(0, 0)).is_empty())
        
        # print("#### BOARD LATEST MOVE ####")
        # print(board.latest_move)
        # print("#### BOARD LATEST MOVE LENGTH ####")
        # print(board.latest_move.__len__())

        assert(board.latest_move.__len__() == 1)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        move2 = get_all_possible_moves(board, player2.color)
        some_move = move2[move2.__len__()-1]
        make_move_ai(board, some_move)
        assert (board.white_pieces_placed == 1)
        assert (board.latest_move[-1] == some_move)
        undo_move(board)
        assert (board.white_pieces_placed == 0)

        
    def test_simulate_game(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        assert (board.black_pieces_placed == 1)
        # print('board from test:')
        # print(board)
        # print(f'board from test, turn: {board.turn}, should be white')
        possible_moves = get_all_possible_moves(board, player2.color)
        move = AI_get_move(board, possible_moves, 'medium')
        make_move_ai(board, move)
        # print('board from test:')
        # print(board)
        # print(f'board from test, turn: {board.turn}, should be black')

        # print(f'white pieces placed: {board.white_pieces_placed}')

        assert (board.white_pieces_placed == 1)
        assert (board.latest_move.pop() == move)

    
    def test_check_win_path_left_to_right(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(4, 0), Orientation.HORIZONTAL)
        
        assert (check_win(board) == GameResult.VICTORY_BLACK)

    def test_check_win_path_top_to_bottom(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        place_piece(player1.color, board, Location(0,0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,4), Orientation.HORIZONTAL)
        
        assert (check_win(board) == GameResult.VICTORY_BLACK)
        
    def test_check_snake_win_path_top_to_bottom(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        # This is the snake path that is tested in this test
        #  |X| | | | |
        #  |X|X|X|X| |
        #  | | | |X| |
        #  | |X|X|X| |
        #  | |X| | | |
        
        place_piece(player1.color, board, Location(0,0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(0,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3,1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3,2), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,3), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1,4), Orientation.HORIZONTAL)
        assert (check_win(board) == GameResult.VICTORY_BLACK)

    def test_check_snake_win_path_left_to_right(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)

        # This is the snake path that is tested in this test
        #  |X|X| | | |
        #  | |x|x|x|x|
        #  | | | | | |
        #  | | | | | |

        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 0), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(2, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(3, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(4, 1), Orientation.HORIZONTAL)
        
        assert (check_win(board) == GameResult.VICTORY_BLACK)

    def test_ai_tries_to_win_snake(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)


        # This is the snake path that is tested in this test
        #  |x| | | | |
        #  |x|x| | | |
        #  | |x| | | |
        #  | |x| | | |
        #  | | | | | |

        place_piece(player2.color, board, Location(0, 0), Orientation.HORIZONTAL)
        place_piece(player2.color, board, Location(1, 0), Orientation.HORIZONTAL)
        place_piece(player2.color, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player2.color, board, Location(2, 1), Orientation.HORIZONTAL)
        place_piece(player2.color, board, Location(3, 1), Orientation.HORIZONTAL)
        
        #print(board)
        
        all_moves = get_all_possible_moves(board, player2.color)
        victory_found = False
        for move in all_moves:
            if(isinstance(move, PlacementMove)):
                if(move == PlacementMove(Piece(Location(4, 1), Orientation.HORIZONTAL, player2.color))):
                    victory_found = True                    
                    break
                
        assert(victory_found == True)            
    
        
        # return
        move_to_make = AI_get_move(board, all_moves, 'medium')
        #print(move_to_make)
        make_move_ai(board, move_to_make)

        #print(board)
        game_result = check_game_end(board)

        assert (game_result == GameResult.VICTORY_WHITE)

    def test_ai_tries_to_win(self):
        board = Board()
        player1 = Player(Color.BLACK)
        #Piece1 = Piece(Location(0,0), Orientation.HORIZONTAL, player2.color)
        player2 = Player(Color.WHITE)
        Piece2 = Piece(Location(1,0), Orientation.HORIZONTAL, player2.color)
        Piece3 = Piece(Location(2,0), Orientation.HORIZONTAL, player2.color)
        Piece4 = Piece(Location(3,0), Orientation.HORIZONTAL, player2.color)
        Piece5 = Piece(Location(4,0), Orientation.HORIZONTAL, player2.color)
        
        board.get_cell(Piece2.location).pieces.insert(0, Piece2) 
        board.get_cell(Piece3.location).pieces.insert(0, Piece3) 
        board.get_cell(Piece4.location).pieces.insert(0, Piece4) 
        board.get_cell(Piece5.location).pieces.insert(0, Piece5)
        
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)

        all_moves = get_all_possible_moves(board, player2.color)
        
        game_result = check_game_end(board)        
        assert(game_result == GameResult.NOT_FINISHED)
        
        move = AI_get_move(board, all_moves, 'medium')        

        make_move_ai(board, move)
        game_result = check_game_end(board)
        
        assert(game_result == GameResult.VICTORY_WHITE)

    def test_ai_is_surrounded_vertical(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        place_piece(player1.color, board, Location(2, 1), Orientation.VERTICAL)
        place_piece(player1.color, board, Location(2, 3), Orientation.VERTICAL)
        place_piece(player1.color, board, Location(1, 2), Orientation.VERTICAL)
        place_piece(player1.color, board, Location(3, 2), Orientation.VERTICAL)
        place_piece(player2.color, board, Location(2, 2), Orientation.HORIZONTAL)
        moves = get_all_possible_moves(board, player2.color)
        best_move = AI_get_move(board, moves, 'medium')
        make_move_ai(board, best_move)
        #print("test")
        #print(board)    

    def test_undo_placement_move(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        place_piece(player1.color, board, Location(0, 0), Orientation.HORIZONTAL)
        board_copy = copy.deepcopy(board)
        place_piece(player2.color, board, Location(0, 0), Orientation.HORIZONTAL)
        undo_move(board)
        assert(board.get_cell(Location(0,0)).get_top_piece() == board_copy.get_cell(Location(0,0)).get_top_piece())
        
    def test_undo_stack_move(self):
        board = Board()
        player1 = Player(Color.BLACK)
        player2 = Player(Color.WHITE)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        place_piece(player1.color, board, Location(1, 1), Orientation.HORIZONTAL)
        
        stack_move = StackMove([Piece(Location(1, 2), Orientation.HORIZONTAL, player1.color),
                                Piece(Location(1, 3), Orientation.HORIZONTAL, player1.color),
                                Piece(Location(1, 4), Orientation.HORIZONTAL, player1.color)], 
                               Piece(Location(1, 1), Orientation.HORIZONTAL, player1.color))
            
        make_move_ai(board, stack_move) 
        #print(board)
        assert(board.get_cell(Location(1, 1)).is_empty())
        assert(board.get_cell(Location(1, 2)).get_top_piece() == Piece(Location(1, 2), Orientation.HORIZONTAL, player1.color))
        assert(board.get_cell(Location(1, 3)).get_top_piece() == Piece(Location(1, 3), Orientation.HORIZONTAL, player1.color))
        assert(board.get_cell(Location(1, 4)).get_top_piece() == Piece(Location(1, 4), Orientation.HORIZONTAL, player1.color))
        undo_move(board)
        #print(board)
        assert(board.get_cell(Location(1, 2)).is_empty())
        assert(board.get_cell(Location(1, 3)).is_empty())
        assert(board.get_cell(Location(1, 4)).is_empty())



    
if __name__ == '__main__':
    unittest.main()