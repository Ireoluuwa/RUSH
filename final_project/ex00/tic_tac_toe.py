#!/usr/bin/env python3
"""A text-based tic-tac-toe game."""

import os
import sys


def clear_screen():
	"""Clear the terminal when possible without affecting redirected output."""
	if sys.stdout.isatty():
		os.system("cls" if os.name == "nt" else "clear")


def draw_board(board):
	print()
	print("                 TIC-TAC-TOE")
	print("          Choose a number from 1 to 9")
	print()
	print("                 +---+---+---+")
	for row in range(3):
		cells = []
		for column in range(3):
			position = row * 3 + column
			cells.append(board[position])
		print(f"                 | {cells[0]} | {cells[1]} | {cells[2]} |")
		print("                 +---+---+---+")
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
	print("Welcome to the board!")
	print("Type STOP at any time to leave the game.\n")
	player_one = input("Player 1 name (X): ").strip()
	if player_one.upper() == "STOP":
		return None
	player_two = input("Player 2 name (O): ").strip()
	if player_two.upper() == "STOP":
		return None
	return player_one or "Player 1", player_two or "Player 2"


def play_round(players, score):
	board = [str(position) for position in range(1, 10)]
	marks = ("X", "O")
	turn = 0

	while True:
		clear_screen()
		draw_board(board)
		name = players[turn]
		mark = marks[turn]
		move = input(f"{name} ({mark}), choose a space: ").strip()

		if move.upper() == "STOP":
			return False
		if not move.isdigit() or not 1 <= int(move) <= 9:
			print("Please enter a number from 1 to 9.")
			input("Press Enter to try again...")
			continue

		position = int(move) - 1
		if board[position] in marks:
			print("That space is already taken. Choose another one.")
			input("Press Enter to try again...")
			continue

		board[position] = mark
		if has_won(board, mark):
			clear_screen()
			draw_board(board)
			score[turn] += 1
			print(f"{name} wins this round!")
			print(f"Score: {players[0]} {score[0]} - {score[1]} {players[1]}")
			return True

		if all(cell in marks for cell in board):
			clear_screen()
			draw_board(board)
			print("It's a draw!")
			print(f"Score: {players[0]} {score[0]} - {score[1]} {players[1]}")
			return True

		turn = 1 - turn


def main():
	names = get_names()
	if names is None:
		print("Goodbye!")
		return

	score = [0, 0]
	while play_round(names, score):
		answer = input("Press Enter for another round, or type STOP to exit: ").strip()
		if answer.upper() == "STOP":
			break

	print("Thanks for playing!")


if __name__ == "__main__":
	main()

