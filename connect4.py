# connect4.py

from dataclasses import dataclass
from typing import List, Optional

def clear_screen() -> None:
    # Cross-platform-ish terminal clear (simple)
    print("\n" * 50)

@dataclass
class Player:
    name: str
    game_piece: str
    wins: int = 0

    def print_won(self) -> None:
        print(f"Player: {self.name} won!")

    def print_wins(self) -> None:
        print(f"Player: {self.name} has {self.wins} wins")

    def get_name(self) -> None:
        # Matches your logic: prompt while length > 20
        while True:
            entered = input(f"{self.name} enter name: ").strip()
            if len(entered) == 0:
                # keep simple: don't allow empty
                print("Invalid name: cannot be empty.")
                continue
            if len(entered) > 20:
                print("Invalid name: Please enter name with 20 characters or less.")
                continue
            self.name = entered
            return

    def get_game_piece(self) -> None:
        while True:
            entered = input(f"Player **{self.name}** enter game piece: ").strip()
            if len(entered) != 1:
                print(f"Invalid game piece: **{self.name}** Please enter 1 keyboard character for game piece.")
                continue
            self.game_piece = entered
            return


class Board:
    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        self.row = rows
        self.column = cols
        self.board: List[List[str]] = [["-" for _ in range(cols)] for _ in range(rows)]

    def reset(self) -> None:
        for r in range(self.row):
            for c in range(self.column):
                self.board[r][c] = "-"

    def print_board(self) -> None:
        for r in range(self.row):
            print(" ".join(f" {self.board[r][c]} " for c in range(self.column)))
        # Column labels
        labels = " ".join(f" {i} " for i in range(1, self.column + 1))
        print(labels + " : Column")

    def check_draw(self) -> bool:
        # If top row has no "-" -> draw
        return all(self.board[0][c] != "-" for c in range(self.column))

    def drop_piece(self, col_index_0_based: int, token: str) -> bool:
        """Returns True if placed, False if column is full."""
        if self.board[0][col_index_0_based] != "-":
            return False

        # Place from bottom up
        for r in range(self.row - 1, -1, -1):
            if self.board[r][col_index_0_based] == "-":
                self.board[r][col_index_0_based] = token
                return True
        return False  # shouldn't happen due to top check

    def check_win_token(self) -> Optional[str]:
        """Return the winning token if there is a win, else None."""
        b = self.board
        R, C = self.row, self.column

        # Horizontal
        for r in range(R):
            for c in range(C - 3):
                t = b[r][c]
                if t != "-" and t == b[r][c+1] == b[r][c+2] == b[r][c+3]:
                    return t

        # Vertical
        for c in range(C):
            for r in range(R - 3):
                t = b[r][c]
                if t != "-" and t == b[r+1][c] == b[r+2][c] == b[r+3][c]:
                    return t

        # Diagonal top-left -> bottom-right
        for r in range(R - 3):
            for c in range(C - 3):
                t = b[r][c]
                if t != "-" and t == b[r+1][c+1] == b[r+2][c+2] == b[r+3][c+3]:
                    return t

        # Diagonal bottom-left -> top-right
        for r in range(3, R):
            for c in range(C - 3):
                t = b[r][c]
                if t != "-" and t == b[r-1][c+1] == b[r-2][c+2] == b[r-3][c+3]:
                    return t

        return None


class State:
    def new_match(self, player1: Player, player2: Player) -> None:
        player1.name = "Player 1"
        player2.name = "Player 2"
        player1.game_piece = ""
        player2.game_piece = ""
        player1.wins = 0
        player2.wins = 0


def central_menu() -> int:
    clear_screen()
    print("XOXOXOXOXOXOXOOXOXO")
    print("O                 X")
    print("X     Connect 4   O")
    print("O                 X")
    print("XOXOXOXOXOXOXOOXOXO\n")
    while True:
        selection = input("Welcome to connect 4. Type 1 to start a game, or type 2 to quit the program: ").strip()
        if selection in ("1", "2"):
            return int(selection)
        print("please type either 1 or 2")


def connect_4(option: int, player1: Player, player2: Player) -> None:
    """
    option == 2: ask for names + tokens
    option == 1: rematch (keep names + tokens)
    """
    board = Board(rows=6, cols=7)

    if option == 2:
        player1.get_name()
        player2.get_name()
        while player2.name == player1.name:
            print("\nError: Same name as player 1")
            player2.name = "Player 2"
            player2.get_name()

        player1.get_game_piece()
        player2.get_game_piece()
        while player2.game_piece == player1.game_piece:
            print("\nERROR: Same game piece as player 1")
            player2.get_game_piece()

    clear_screen()
    board.print_board()

    swap_counter = 0  # counts placed tokens
    quit_game = False

    while swap_counter < board.row * board.column:
        current = player1 if (swap_counter % 2 == 0) else player2

        # Get valid input
        while True:
            print(f"{current.name}'s turn.")
            s = input("Enter a valid column number, or type 'resign' to resign: ").strip()

            if s.lower() == "resign":
                print(f"{current.name} resigned")
                other = player2 if current is player1 else player1
                other.wins += 1
                other.print_wins()
                quit_game = True
                break

            if not s.isdigit():
                print("Invalid Input. Please try again.\n")
                continue

            col = int(s)
            if col < 1 or col > board.column:
                print("Invalid number. Please enter a column in range.\n")
                continue

            # Try to place
            placed = board.drop_piece(col - 1, current.game_piece)
            if not placed:
                print("That column is full. Pick another.\n")
                continue

            break

        if quit_game:
            return

        clear_screen()
        board.print_board()

        winner_token = board.check_win_token()
        if winner_token is not None:
            if winner_token == player1.game_piece:
                player1.print_won()
                player1.wins += 1
                player1.print_wins()
            else:
                player2.print_won()
                player2.wins += 1
                player2.print_wins()
            print("Win detected")
            return

        if board.check_draw():
            print("Draw detected")
            return

        swap_counter += 1
        tokens_left = (board.row * board.column) - swap_counter
        print(f"There are {tokens_left} tokens left")


def main() -> None:
    player1 = Player(name="Player 1", game_piece="")
    player2 = Player(name="Player 2", game_piece="")
    game_state = State()

    cursor = central_menu()
    if cursor == 2:
        print("Quitting Connect 4")
        return

    connect_4(option=2, player1=player1, player2=player2)

    while True:
        choice = input(
            "Type 1 for Rematch, Type 2 for New Match, Type 3 to go the main menu, Type 4 to End Program: "
        ).strip()

        if choice not in ("1", "2", "3", "4"):
            print("Invalid Input. Try again.")
            continue

        option = int(choice)

        if option == 1:
            print("Rematch!")
            connect_4(option=1, player1=player1, player2=player2)

        elif option == 2:
            print("New Match!")
            game_state.new_match(player1, player2)
            connect_4(option=2, player1=player1, player2=player2)

        elif option == 3:
            cursor = central_menu()
            if cursor == 1:
                game_state.new_match(player1, player2)
                connect_4(option=2, player1=player1, player2=player2)
            else:
                print("Quitting Connect 4. Thanks for Playing!")
                return

        elif option == 4:
            print("Quitting Connect 4. Thanks for Playing!")
            return


if __name__ == "__main__":
    main()
