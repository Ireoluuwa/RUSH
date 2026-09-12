#!/usr/bin/env python3
"""A polished, text-based tic-tac-toe game."""

import os
import sys


RESET = "\033[0m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
DIM = "\033[2m"
WHITE = "\033[97m"

USE_COLOR = sys.stdout.isatty()


def terminal_supports_unicode():
        try:
                "╔".encode(sys.stdout.encoding or "utf-8")
                return True
        except UnicodeEncodeError:
                return False


USE_UNICODE = terminal_supports_unicode()


def clear_screen():
        """Clear the terminal when possible without affecting redirected output."""
        if sys.stdout.isatty():
                os.system("cls" if os.name == "nt" else "clear")


def colour(text, colour_code):
        if not USE_COLOR:
                return text
        return f"{colour_code}{text}{RESET}"


def symbol(name):
        """Return a Unicode decoration, with an ASCII fallback."""
        symbols = {
                "star": ("✦", "*"),
                "diamond": ("◆", ">"),
                "warning": ("⚠", "!"),
                "winner": ("★", "*"),
        }
        unicode_symbol, ascii_symbol = symbols[name]
        return unicode_symbol if USE_UNICODE else ascii_symbol


def print_box(lines, width=52, border_colour=CYAN):
        """Print a centered box that works in both Unicode and ASCII terminals."""
        if USE_UNICODE:
                top, bottom, side = "╔", "╚", "║"
                top_fill, bottom_fill = "═", "═"
                corner_top, corner_bottom = "╗", "╝"
        else:
                top, bottom, side = "+", "+", "|"
                top_fill, bottom_fill = "-", "-"
                corner_top, corner_bottom = "+", "+"

        print(colour(f"{top}{top_fill * width}{corner_top}", border_colour))
        for line in lines:
                print(colour(f"{side}{line.center(width)}{side}", border_colour))
        print(colour(f"{bottom}{bottom_fill * width}{corner_bottom}", border_colour))


def show_welcome():
        clear_screen()
        print()
        print_box([
                "",
                f"{symbol('star')}  TIC-TAC-TOE  {symbol('star')}",
                "",
                "A classic battle of X & O",
                "",
        ], width=52)
        print()
        print(colour("  Two players. One board. One winner.", DIM))
        print(colour("  Type STOP at any time to exit.", DIM))
        print()


def draw_scoreboard(players, score):
        title = f"{symbol('star')}  CURRENT SCORE  {symbol('star')}"
        score_line = f"{players[0]}  [X]   {score[0]}  -  {score[1]}   [O]  {players[1]}"
        print_box([title, "", score_line], width=52, border_colour=WHITE)


def draw_board(board, players=None, score=None, turn=None):
        """Draw the current board with numbered empty spaces and colored marks."""
        if USE_UNICODE:
                top = "┌─────────┬─────────┬─────────┐"
                middle = "├─────────┼─────────┼─────────┤"
                bottom = "└─────────┴─────────┴─────────┘"
                divider = "│"
        else:
                top = "+---------+---------+---------+"
                middle = "+---------+---------+---------+"
                bottom = "+---------+---------+---------+"
                divider = "|"

        print()
        print(colour("                 TIC-TAC-TOE", CYAN))
        print(colour("          Choose an available number from 1 to 9", DIM))
        print()
        if players is not None and score is not None:
                draw_scoreboard(players, score)
                print()

        print(colour(f"             {top}", CYAN))
        for row in range(3):
                cells = []
                for column in range(3):
                        value = board[row * 3 + column]
                        if value == "X":
                                value = colour("X", YELLOW)
                        elif value == "O":
                                value = colour("O", GREEN)
                        cells.append(value.center(9))
                print(colour("             ", CYAN) + divider + divider.join(cells) + divider)
                if row < 2:
                        print(colour(f"             {middle}", CYAN))
        print(colour(f"             {bottom}", CYAN))
        print()
        if players is not None and turn is not None:
                name = players[turn]
                mark = ("X", "O")[turn]
                mark_colour = YELLOW if mark == "X" else GREEN
                turn_text = f"{symbol('diamond')}  {name}'s turn - "
                print(colour(turn_text, WHITE) + colour(mark, mark_colour))
        print()


def has_won(board, mark):
        winning_lines = (
                (0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6),
        )
        return any(all(board[position] == mark for position in line)
                   for line in winning_lines)


def get_names():
        show_welcome()
        player_one = input(colour("  Player 1 name (X): ", YELLOW)).strip()
        if player_one.upper() == "STOP":
                return None
        player_two = input(colour("  Player 2 name (O): ", GREEN)).strip()
        if player_two.upper() == "STOP":
                return None
        return player_one or "Player 1", player_two or "Player 2"


def show_result(title, message, players, score, colour_code=GREEN):
        print()
        print_box(["", title, "", message, ""], width=52, border_colour=colour_code)
        print()
        draw_scoreboard(players, score)
        print()


def play_round(players, score):
        board = [str(position) for position in range(1, 10)]
        marks = ("X", "O")
        turn = 0

        while True:
                clear_screen()
                draw_board(board, players, score, turn)
                name = players[turn]
                mark = marks[turn]
                move = input(colour(f"  {name} ({mark}), choose your next position: ", WHITE)).strip()

                if move.upper() == "STOP":
                        return False
                if not move.isdigit() or not 1 <= int(move) <= 9:
                        print()
                        print(colour(f"  {symbol('warning')} Invalid move", RED))
                        print(colour("  Please choose an available number between 1 and 9.", DIM))
                        input(colour("\n  Press Enter to try again...", DIM))
                        continue

                position = int(move) - 1
                if board[position] in marks:
                        print()
                        print(colour(f"  {symbol('warning')} That position is already occupied.", RED))
                        print(colour("  Please choose another space.", DIM))
                        input(colour("\n  Press Enter to try again...", DIM))
                        continue

                board[position] = mark
                if has_won(board, mark):
                        clear_screen()
                        draw_board(board, players, score)
                        score[turn] += 1
                        show_result(
                                f"{symbol('winner')}  WE HAVE A WINNER!  {symbol('winner')}",
                                f"{name} wins this round!",
                                players,
                                score,
                        )
                        return True

                if all(cell in marks for cell in board):
                        clear_screen()
                        draw_board(board, players, score)
                        show_result(
                                "GAME DRAW!",
                                "Nobody takes this round.",
                                players,
                                score,
                                CYAN,
                        )
                        return True

                turn = 1 - turn


def main():
        names = get_names()
        if names is None:
                print_box(["", "Thanks for playing!", "", "See you next time!", ""], width=52)
                return

        score = [0, 0]
        while play_round(names, score):
                print_box(["", "Ready for another round?", ""], width=52, border_colour=CYAN)
                answer = input(colour("  Press Enter to play again, or type STOP to exit: ", WHITE)).strip()
                if answer.upper() == "STOP":
                        break

        print()
        print_box(["", f"{symbol('star')}  Thanks for playing!  {symbol('star')}", "", "See you next time!", ""], width=52)


if __name__ == "__main__":
        main()
