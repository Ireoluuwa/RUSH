#!/usr/bin/env python3
"""A text-based tic-tac-toe game."""

import os
import sys


def clear_screen():
	"""Clear the terminal when possible without affecting redirected output."""
	if sys.stdout.isatty():
		os.system("cls" if os.name == "nt" else "clear")


# Render the 3x3 board as a bordered grid, showing each cell's mark or its number if empty
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


# All 8 index triples (0-based) that make a winning line: 3 rows, 3 columns, 2 diagonals
WINNING_LINES = (
	(0, 1, 2), (3, 4, 5), (6, 7, 8),
	(0, 3, 6), (1, 4, 7), (2, 5, 8),
	(0, 4, 8), (2, 4, 6),
)


# True if the given mark fills every position of any winning line
def has_won(board, mark):
	return any(all(board[position] == mark for position in line)
			   for line in WINNING_LINES)


# Prompt for both player names once per session; returns None if either player types STOP
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


# Play one round on a fresh board, alternating turns until a win, a draw, or a mid-round STOP.
# Returns True if the round finished normally (win/draw) or False if a player stopped.
def play_round(players, score):
	board = [str(position) for position in range(1, 10)]  # cells 1-9 double as their own empty-space labels
	marks = ("X", "O")
	turn = 0  # index into players/marks for whoever moves next

	while True:
		clear_screen()
		draw_board(board)
		name = players[turn]
		mark = marks[turn]
		move = input(f"{name} ({mark}), choose a space: ").strip()

		if move.upper() == "STOP":
			return False
		if not move.isdigit() or not 1 <= int(move) <= 9:
			print("Please enter a number from 1 to 9.")  # invalid input: re-prompt without switching turns
			input("Press Enter to try again...")
			continue

		position = int(move) - 1
		if board[position] in marks:
			print("That space is already taken. Choose another one.")  # occupied cell: re-prompt same player
			input("Press Enter to try again...")
			continue

		board[position] = mark
		if has_won(board, mark):  # current player just completed a line
			clear_screen()
			draw_board(board)
			score[turn] += 1
			print(f"{name} wins this round!")
			print(f"Score: {players[0]} {score[0]} - {score[1]} {players[1]}")
			return True

		if all(cell in marks for cell in board):  # no empty cells left and nobody won
			clear_screen()
			draw_board(board)
			print("It's a draw!")
			print(f"Score: {players[0]} {score[0]} - {score[1]} {players[1]}")
			return True

		turn = 1 - turn  # hand the turn to the other player


# CLI entry point: collect names once, then loop rounds (keeping score) until the user stops
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




# Color palette for the Tkinter GUI (paper-and-ink look; separate colors per mark)
PAPER_BG = "#d3f8a3"
INK = "#4a4a42"
FAINT = "#9a978a"
INK_X = "#1f3b73"
INK_O = "#b23a2e"
WIN_HIGHLIGHT = "#ffe082"


# Windowed version of the same game, reusing WINNING_LINES/has_won from the CLI logic above
class TicTacToeGUI:
	# Build the root window and both frames (name-entry setup screen, then the game screen)
	def __init__(self, root):
		import tkinter as tk
		self.tk = tk

		self.root = root
		root.title("ASCII ARENA: TIC-TAC-TOE")
		root.configure(bg=PAPER_BG)
		root.resizable(False, False)
 
		self.players = ["Player 1", "Player 2"]
		self.score = [0, 0]
		self.board = [None] * 9
		self.turn = 0
		self.round_over = False
		self.buttons = []
 
		self.setup_frame = tk.Frame(root, bg=PAPER_BG, padx=36, pady=36)
		self.game_frame = tk.Frame(root, bg=PAPER_BG, padx=24, pady=24)
 
		self._build_setup_frame()
		self._build_game_frame()
		self.setup_frame.pack()
 
	#---------Tic-Tac-Toe  Screen---------#
 
	# Build the name-entry screen shown before a game starts
	def _build_setup_frame(self):
		tk = self.tk
 
		tk.Label(
			self.setup_frame, text="ASCII ARENA: TIC-TAC-TOE", font=("Georgia", 28, "bold"),
			bg=PAPER_BG, fg=INK,
		).pack(pady=(0, 4))
		
 
		tk.Label(
			self.setup_frame, text="Player 1 : What's your name?", font=("Georgia", 10, "italic"),
			bg=PAPER_BG, fg=INK_X, anchor="w",
		).pack(fill="x")
		self.x_entry = tk.Entry(
			self.setup_frame, font=("Georgia", 13), fg=INK_X,
			relief="flat", highlightthickness=1, highlightbackground=INK_X, highlightcolor=INK_X,
		)
		self.x_entry.pack(fill="x", pady=(2, 16), ipady=4)
 
		tk.Label(
			self.setup_frame, text="Player 2 : What's your name?", font=("Georgia", 10, "italic"),
			bg=PAPER_BG, fg=INK_O, anchor="w",
		).pack(fill="x")
		self.o_entry = tk.Entry(
			self.setup_frame, font=("Georgia", 13), fg=INK_O,
			relief="flat", highlightthickness=1, highlightbackground=INK_O, highlightcolor=INK_O,
		)
		self.o_entry.pack(fill="x", pady=(2, 22), ipady=4)
 
		tk.Button(
			self.setup_frame, text="Start game", font=("Georgia", 12),
			command=self.start_game, bg=PAPER_BG, fg=INK,
			relief="solid", bd=2, padx=10, pady=8,
			activebackground=INK, activeforeground=PAPER_BG,
		).pack(fill="x")
 
		self.x_entry.bind("<Return>", lambda e: self.start_game())
		self.o_entry.bind("<Return>", lambda e: self.start_game())
		self.x_entry.focus_set()
 
	# Read entered names, reset score, and switch from the setup screen to the game screen
	def start_game(self):
		x_name = self.x_entry.get().strip() or "Player 1"
		o_name = self.o_entry.get().strip() or "Player 2"
		self.players = [x_name, o_name]
		self.score = [0, 0]
 
		self.setup_frame.pack_forget()
		self.game_frame.pack()
		self._start_round()
 
	# ---- game screen ----
 
	# Build the game screen: score row, turn label, 3x3 button grid, and next-round/go-back controls
	def _build_game_frame(self):
		tk = self.tk
 
		score_row = tk.Frame(self.game_frame, bg=PAPER_BG)
		score_row.pack(fill="x", pady=(0, 6))
		self.score_label_x = tk.Label(score_row, font=("Georgia", 12, "bold"), bg=PAPER_BG, fg=INK_X)
		self.score_label_x.pack(side="left", expand=True)
		tk.Label(score_row, text="vs", font=("Georgia", 10, "italic"), bg=PAPER_BG, fg=FAINT).pack(side="left", padx=10)
		self.score_label_o = tk.Label(score_row, font=("Georgia", 12, "bold"), bg=PAPER_BG, fg=INK_O)
		self.score_label_o.pack(side="left", expand=True)
 
		self.turn_label = tk.Label(self.game_frame, font=("Georgia", 13), bg=PAPER_BG, fg=INK)
		self.turn_label.pack(pady=(4, 16))
 
		board_frame = tk.Frame(self.game_frame, bg=INK)
		board_frame.pack()
		self.buttons = []
		for i in range(9):
			btn = tk.Button(
				board_frame, text="", font=("Georgia", 28, "bold"),
				width=3, height=1, bg=PAPER_BG, fg=FAINT,
				relief="flat", bd=0,
				activebackground=PAPER_BG,
				command=lambda pos=i: self.handle_move(pos),
			)
			row, col = divmod(i, 3)
			btn.grid(row=row, column=col, padx=1, pady=1, ipadx=14, ipady=10)
			self.buttons.append(btn)
 
		controls = tk.Frame(self.game_frame, bg=PAPER_BG)
		controls.pack(fill="x", pady=(18, 0))
		self.next_round_btn = tk.Button(
			controls, text="Next round", font=("Georgia", 11),
			command=self._start_round, bg=PAPER_BG, fg=INK, relief="solid", bd=1,
		)
		quit_btn = tk.Button(
			controls, text="Go Back", font=("Georgia", 11),
			command=self.goback, bg=PAPER_BG, fg=INK, relief="solid", bd=1,
		)
		self.next_round_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
		quit_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
		self.next_round_btn.pack_forget()
 
		self.result_label = tk.Label(self.game_frame, text="", font=("Georgia", 10, "italic"), bg=PAPER_BG, fg=FAINT)
		self.result_label.pack(pady=(12, 0))
 
	# Reset the board, buttons, and labels for a new round (keeps the running score)
	def _start_round(self):
		self.board = [None] * 9
		self.turn = 0
		self.round_over = False
		for btn in self.buttons:
			btn.config(text="", state="normal", bg=PAPER_BG, fg=FAINT)
		self.next_round_btn.pack_forget()
		self.result_label.config(text="")
		self._update_score_labels()
		self._update_turn_label()
 
	# Refresh the score labels with each player's current win count
	def _update_score_labels(self):
		self.score_label_x.config(text=f"{self.players[0]}: {self.score[0]}")
		self.score_label_o.config(text=f"{self.players[1]}: {self.score[1]}")

	# Refresh the label showing whose turn it is, in that player's color
	def _update_turn_label(self):
		mark = "X" if self.turn == 0 else "O"
		color = INK_X if self.turn == 0 else INK_O
		self.turn_label.config(text=f"{self.players[self.turn]}'s turn ({mark})", fg=color)

	# Handle a click on a board button: place the mark, then check for a win, a draw, or pass the turn
	def handle_move(self, position):
		if self.round_over or self.board[position] is not None:  # ignore clicks once the round is over or the cell is taken
			return
 
		mark = "X" if self.turn == 0 else "O"
		self.board[position] = mark
		color = INK_X if mark == "X" else INK_O
		self.buttons[position].config(text=mark, fg=color, state="disabled", disabledforeground=color)
 
		if has_won(self.board, mark):
			self.round_over = True
			self.score[self.turn] += 1
			self._update_score_labels()
			self._highlight_winning_line(mark)
			self.turn_label.config(text=f"{self.players[self.turn]} wins this round!", fg=color)
			self._end_round()
			return
 
		if all(cell is not None for cell in self.board):
			self.round_over = True
			self.turn_label.config(text="It's a draw!", fg=INK)
			self._end_round()
			return
 
		self.turn = 1 - self.turn
		self._update_turn_label()
 
	# Reveal the Next round button and lock the board once the round has a winner or a draw
	def _end_round(self):
		self.next_round_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
		for btn in self.buttons:
			btn.config(state="disabled")

	# Highlight the three cells of whichever line the given mark just completed
	def _highlight_winning_line(self, mark):
		for line in WINNING_LINES:
			if all(self.board[pos] == mark for pos in line):
				for pos in line:
					self.buttons[pos].config(bg=WIN_HIGHLIGHT)
				break

	# Clear the name entries and return from the game screen to the setup screen
	def goback(self):
		self.game_frame.pack_forget()
		self.x_entry.delete(0, self.tk.END)
		self.o_entry.delete(0, self.tk.END)
		self.setup_frame.pack()
 
 
# Build the Tk root window, mount the GUI, and start the event loop
def run_gui():
	import tkinter as tk
	root = tk.Tk()
	TicTacToeGUI(root)
	root.mainloop()
 
 
# Entry point: run the Tkinter GUI when invoked as `tic_tac_toe.py gui`, otherwise run the CLI game
if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "gui":
		run_gui()
	else:
		main()
