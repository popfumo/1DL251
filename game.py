from board import Board, Player, Color, Location, Orientation, GameResult
from interaction_functions import place_piece, move_piece, unload_cell, unload_piece_recursive, get_all_possible_moves, make_move_ai, check_unload
from game_logic import check_win
from game_ai import set_difficulty, AI_get_move

'''
Init:
1. Load board and players

How does a game turn look like? 
1. Player 1 makes a move
2. Check if it's a winning move
3. End game or it's the other players turn.

'''

def game():
    # Initialize the game
    board = Board()
    player1 = Player(Color.BLACK)
    player2 = Player(Color.WHITE)    
    
    difficulty = set_difficulty()

    # Main game loop
    while True:
        # Display the current board state
        print(board)
        # print(board.turn)
        # Get player's move

        move = get_player_move(player1, board)

        # Execute the move
        if move['type'] == 'place':
            success = place_piece(player1, board, move['location'], move['orientation'])
        elif move['type'] == 'move':
            success = move_piece(player1, board, move['old_location'], move['new_location'])
        elif move['type'] == 'unload':
            success = unload_piece_recursive(player1, board, move['num_remove'], move['old_location'], move['old_location'])

        # Check if the move was successful
        if not success:
            print("Invalid move. Try again.")
            continue

        game_result = check_game_end(board)
        if game_result != GameResult.NOT_FINISHED:
            break
        

        # print("### board.turn ###")
        # print(board.turn)
        # Check for a stalemate (you'll need to implement this function) TODO
        #if is_stalemate(board):
        #    print("The game is a draw.")
        #    break

        # Switch to the other player ( the AI )
        possible_moves = get_all_possible_moves(board, player2.color)
        the_best_move = AI_get_move(board, possible_moves, difficulty)
        # print(f'Best move: {the_best_move}')

        make_move_ai(board, the_best_move)

        game_result = check_game_end(board)
        if game_result != GameResult.NOT_FINISHED:
            break
        
        print("(black) player1.pieces_placed: " + player1.pieces_placed.__str__())
        print("(white) player2.pieces_placed: " + player2.pieces_placed.__str__())
        print("end of Game Loop")

def check_game_end(board):
    game_result = check_win(board)
    if game_result == GameResult.VICTORY_BLACK or game_result == GameResult.VICTORY_WHITE:
        winner = Color.from_id(game_result.value)
        print(board)
        print(f"{winner} wins!")
    elif game_result == GameResult.DRAW:
        print("The game is a draw.")
    elif game_result == GameResult.NOT_FINISHED:
        pass
    else: 
        print("Error: Invalid game result.")
    
    return game_result

def get_player_move(player, board):
    # Prompt player for the type of move they want to make
    # print(f"{player.color.name} Player, it's your turn.")
    print("Choose your action: ")
    print("1. Place a piece")
    print("2. Move a piece")
    print("3. Unload a cell")

    action = input("Enter the number corresponding to your action: ")

    if action == "1":  # Place a piece
        # Get the coordinates where the player wants to place the piece
        x = int(input("Enter the x-coordinate (0-4) to place the piece: "))
        y = int(input("Enter the y-coordinate (0-4) to place the piece: "))
        try:
            location = Location(x, y)
        except IndexError:
            print("Invalid coordinates. Try again.")
            return get_player_move(player, board)

         # Get the piece's orientation
        print("Choose orientation:")
        print("1. Horizontal")
        print("2. Vertical")
        orientation_choice = input("Enter 1 for Horizontal or 2 for Vertical: ")
        orientation = Orientation.HORIZONTAL if orientation_choice == "1" else Orientation.VERTICAL


        return {
            "type": "place",
            "location": location,
            "orientation": orientation
        }

    elif action == "2":  # Move a piece
        # Get the old location and new location for the move
        old_x = int(input("Enter the x-coordinate of the piece to move: "))
        old_y = int(input("Enter the y-coordinate of the piece to move: "))
        try:
            old_location = Location(old_x, old_y)
        except IndexError:
            print("Invalid coordinates for old location. Try again.")
            return get_player_move(player, board)

        new_x = int(input("Enter the x-coordinate to move the piece to: "))
        new_y = int(input("Enter the y-coordinate to move the piece to: "))
        try:
            new_location = Location(new_x, new_y)
        except IndexError:
            print("Invalid coordinates for new location. Try again.")
            return get_player_move(player, board)

        return {
            "type": "move",
            "old_location": old_location,
            "new_location": new_location
        }

    elif action == "3":  # Unload a cell
        if (check_unload(board, player)):
            while True:
                try:
                    old_x = int(input("Enter the x-coordinate of the cell to unload: "))
                    old_y = int(input("Enter the y-coordinate of the cell to unload: "))
                    old_location = Location(old_x, old_y)
                    
                    if not (0 <= old_x < 5 and 0 <= old_y < 5):
                        print("Invalid coordinates. Please enter values between 0 and 4.")
                        continue
                    
                    cell = board.get_cell(old_location)
                    print(f"Cell contents at {old_location}: {cell.pieces}")
                    
                    if cell.is_empty():
                        print("This cell is empty. Please choose another cell.")
                        continue
                    
                    top_piece = cell.get_top_piece()
                    if top_piece is None:
                        print("Error: Cell is not empty but get_top_piece() returned None.")
                        continue
                    
                    print(f"Top piece: Color - {top_piece.color}, Orientation - {top_piece.orientation}")
                    print(f"Current player color: {player.color}")
                    
                    if top_piece.color != player.color:
                        print("The top piece in this cell is not yours. Please choose another cell.")
                        continue
                    
                    if top_piece.orientation == Orientation.VERTICAL:
                        print("The top piece in this cell is vertical and cannot be unloaded. Please choose another cell.")
                        continue
                    
                    max_pieces = len(cell.pieces)
                    break
                except IndexError:
                    print("Invalid coordinates. Please enter values between 0 and 4.")
                except ValueError:
                    print("Please enter valid integer coordinates.")
            
            while True:
                try:
                    num_remove = int(input(f"Enter the number of pieces to unload (1-{max_pieces}): "))
                    if 1 <= num_remove <= max_pieces:
                        break
                    else:
                        print(f"Please enter a number between 1 and {max_pieces}.")
                except ValueError:
                    print("Please enter a valid integer.")
        
            return {
                "type": "unload",
                "old_location": old_location,
                "num_remove": num_remove
            }
        else:
            print("There are no cells that can be unloaded")
            return get_player_move(player, board)
    else:
        print("Invalid action. Please try again.")
        return get_player_move(player, board)


if __name__ == "__main__":
    game()
