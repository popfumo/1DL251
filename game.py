from board import Board, Player, Color, Location, Orientation
from interaction_functions import place_piece, move_piece, unload_cell
from game_logic import check_win

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
    current_player = player1  # Black goes first

    # Main game loop
    while True:
        # Display the current board state
        print(board)

        # Get player's move
        move = get_player_move(current_player, board)

        # Execute the move
        if move['type'] == 'place':
            success = place_piece(current_player, board, move['location'], move['orientation'])
        elif move['type'] == 'move':
            success = move_piece(current_player, board, move['old_location'], move['new_location'])
        elif move['type'] == 'unload':
            success = unload_cell(current_player, board, move['old_location'], move['new_locations'])

        # Check if the move was successful
        if not success:
            print("Invalid move. Try again.")
            continue

        # Check for a win
        if check_win(board, current_player):
            print(f"{current_player.color.name} wins!")
            break

        # Check for a stalemate (you'll need to implement this function) TODO
        #if is_stalemate(board):
        #    print("The game is a draw.")
        #    break

        # Switch to the other player
        current_player = player2 if current_player == player1 else player1

def get_player_move(player, board):
    # Prompt player for the type of move they want to make
    print(f"{player.color.name} Player, it's your turn.")
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
        # Get the old location to unload and the new locations
        old_x = int(input("Enter the x-coordinate of the cell to unload: "))
        old_y = int(input("Enter the y-coordinate of the cell to unload: "))
        try:
            old_location = Location(old_x, old_y)
        except IndexError:
            print("Invalid coordinates for unloading. Try again.")
            return get_player_move(player, board)

        num_new_locations = int(input("Enter the number of new locations to unload to: "))
        new_locations = []
        for i in range(num_new_locations):
            new_x = int(input(f"Enter the x-coordinate of new location {i + 1}: "))
            new_y = int(input(f"Enter the y-coordinate of new location {i + 1}: "))
            try:
                new_location = Location(new_x, new_y)
                new_locations.append(new_location)
            except IndexError:
                print("Invalid coordinates for new location. Try again.")
                return get_player_move(player, board)

        return {
            "type": "unload",
            "old_location": old_location,
            "new_locations": new_locations
        }

    else:
        print("Invalid action. Please try again.")
        return get_player_move(player, board)


if __name__ == "__main__":
    game()
