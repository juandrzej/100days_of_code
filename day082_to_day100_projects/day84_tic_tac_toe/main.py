import os


def main() -> None:
    draw_board()


def draw_board() -> None:
    """Function to draw the game board."""
    width = os.get_terminal_size().columns
    print(
        """
       | O |   
    -----------
     X | O | X
    -----------
       | X |
    """.center(width)
    )


if __name__ == "__main__":
    main()
