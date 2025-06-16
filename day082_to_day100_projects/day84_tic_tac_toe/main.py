import random


def print_board(board: list[str]) -> None:
    """Print the current game board"""
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")


def check_winner(board: list[str]) -> str | None:
    """Check if there's a winner or if the game is a tie"""
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != " ":
            return board[i]

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != " ":
            return board[i]

    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]

    # Check for tie
    if " " not in board:
        return "Tie"

    return None


def player_move(board: list[str]) -> int:
    """Get and validate player's move"""
    while True:
        try:
            move: int = int(input("Enter your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == " ":
                return move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")


def computer_move(board: list[str], computer_char: str) -> int:
    """Simple AI for computer's move"""
    player_char = "O" if computer_char == "X" else "X"

    # Check for winning move
    for i in range(9):
        if board[i] == " ":
            board[i] = computer_char
            if check_winner(board) == computer_char:
                board[i] = " "
                return i
            board[i] = " "

    # Block player's winning move
    for i in range(9):
        if board[i] == " ":
            board[i] = player_char
            if check_winner(board) == player_char:
                board[i] = " "
                return i
            board[i] = " "

    # Try to take center
    if board[4] == " ":
        return 4

    # Try to take a corner
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for i in corners:
        if board[i] == " ":
            return i

    # Take any available space
    for i in range(9):
        if board[i] == " ":
            return i


def play_game() -> None:
    """Main game loop"""
    board: list[str] = [" "] * 9
    print("Welcome to Tic Tac Toe!")
    print("Positions are numbered 1-9 from top-left to bottom-right")
    print_board([str(x) for x in range(1, 10)])

    # Choose player's character
    player_char: str = input("Choose X or O: ").upper()
    while player_char not in ["X", "O"]:
        player_char: str = input("Please choose X or O: ").upper()

    computer_char: str = "O" if player_char == "X" else "X"

    # Determine who goes first
    turn: str = "player" if random.choice([True, False]) else "computer"
    print(f"{turn.capitalize()} goes first!")

    while True:
        if turn == "player":
            print_board(board)
            move: int = player_move(board)
            board[move] = player_char
            turn = "computer"
        else:
            print("Computer's turn...")
            move: int = computer_move(board, computer_char)
            board[move] = computer_char
            turn = "player"

        # into match case + result into int?
        result: str | None = check_winner(board)
        if result:
            print_board(board)
            if result == "Tie":
                print("It's a tie!")
            elif result == player_char:
                print("Congratulations! You won!")
            else:
                print("Computer wins!")
            break


def main() -> None:
    """Main function to control game flow"""
    while True:
        play_game()
        play_again: str = input("Play again? (y/n): ").lower()
        while play_again not in ["y", "n"]:
            play_again: str = input("Please enter y or n: ").lower()
        if play_again == "n":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
