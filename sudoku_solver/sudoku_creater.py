import random
import os
from copy import deepcopy
import re
class Sudoku:
	def __init__(self):
		self.puzzle = []
		for x in range(0,9):
			self.puzzle.append([])
			for y in range(0, 9):
				self.puzzle[x].append(-1)
		self.generate()
				
	def __str__(self):
		str_p = "   "
		tmp_c = ""
		for x in range(0, 9):
			str_p = str_p + str(x) + " "
		str_p = str_p + "    " + "\n"  + "   "
		for x in range(0, 9):
			str_p = str_p + "_ "
		str_p = str_p + "\n"
		for x in range(0,9):
			str_p = str_p + str(x) + "| "
			for y in range(0, 9):
				tmp_c = self.visible_p[x][y]
				if(tmp_c < 0 or tmp_c >= 10):
					str_p += "."
				else:
					str_p += str(tmp_c)
				str_p += " "
			str_p += "\n"
		return str_p
	def __repr__(self):
		return self.__str__()

	def generate(self):
		# Create first square
		avail_num = [0] * 11
		sequence = [0] * 10
		for y in range(0,9):
			while(1):
				tmp = random.randrange(1,10)
				if(avail_num[tmp] == 0):
					self.puzzle[0][y] = tmp
					avail_num[tmp] = 1
					sequence[y] = tmp
					break
		for y in range(0,9):
			self.puzzle[1][(y + 3) % 9] = sequence[y]
		for y in range(0,9):
			self.puzzle[2][(y + 6) % 9] = sequence[y]
		
		for y in range(0,9):
			self.puzzle[3][(y + 1) % 9] = sequence[y]
		for y in range(0,9):
			self.puzzle[4][(y + 4) % 9] = sequence[y]
		for y in range(0,9):
			self.puzzle[5][(y + 7) % 9] = sequence[y]

		for y in range(0,9):
			self.puzzle[6][(y + 2) % 9] = sequence[y]
		for y in range(0,9):
			self.puzzle[7][(y + 5) % 9] = sequence[y]
		for y in range(0,9):
			self.puzzle[8][(y + 8) % 9] = sequence[y]

		self.visible_p = deepcopy(self.puzzle)

	def check_row(self, row, a):
		for y in range(0,9):
			if(self.puzzle[row][y] == a):
				return False
		return True

	def check_column(self, column, a):
		for x in range(0,9):
			if(self.puzzle[x][column] == a):
				return False
		return True

	def check_square(self, square, a):
		if(square < 3):
			for x in range(0,3):
				for y in range(0,3):
					if(self.puzzle[x + square*3][y] == a):
						return False
		elif(square < 6):
			for x in range(0,3):
				for y in range(3,6):
					if(self.puzzle[x + square*3][y] == a):
						return False
		return True


	def print_square(self, square):
		str_t = ""
		for x in range(0,3):
			for y in range(0,3):
				str_t = str_t + str(self.puzzle[x + square*3][y]) + " "
			str_t += "\n"
		print("Square: " + str_t)

	def verify(self):
		used_num = [0] * 10
		#check rows
		for x in range (0,9):
			for y in range (0,9):
				if(used_num[self.puzzle[x][y]] == 1):
					return (False, y + 1, x + 1, self.puzzle[x][y])
				else:
					used_num[self.puzzle[x][y]] = 1
			#reset used numbers
			for r in range(0,10):
				used_num[r] = 0
		# check columns
		for y in range (0,9):
			for x in range (0,9):
				if(used_num[self.puzzle[x][y]] == 1):
					return (False, y + 1, x + 1, self.puzzle[x][y])
				else:
					used_num[self.puzzle[x][y]] = 1
			#reset used numbers
			for r in range(0,10):
				used_num[r] = 0

		# check squares
		for c in range(0,3):
			for y in range (0,9):
				for x in range (0,3):
					if(used_num[self.puzzle[x + (c*3)][y]] == 1):
						return (False, x + c*3, y, self.puzzle[x + (c*3)][y])
					else:
						used_num[self.puzzle[x + (c*3)][y]] = 1
				if((y + 1) % 3 == 0):
					for r in range(0,10):
						used_num[r] = 0
		return True

	def hide_solution(self):
		obfus_place = 0
		reserved_placed = [0] * 9
		for x in range(0,9):
			for y in range(0,3):
				while(reserved_placed[obfus_place] == 1):
					obfus_place = random.randrange(0, 9)
				reserved_placed[obfus_place] = 1
			for y in range(0,9):
				if(reserved_placed[y] != 1):
					self.visible_p[x][y] = -1
			for r in range(0,9):
				reserved_placed[r] = 0
		self.reset_puzzle = deepcopy(self.visible_p)

	def get_solution(self):
		str_p = ""
		tmp_c = ""
		for x in range(0,9):
			for y in range(0, 9):
				tmp_c = self.puzzle[x][y]
				if(tmp_c < 0 or tmp_c >= 10):
					str_p += "."
				else:
					str_p += str(tmp_c)
				str_p += " "
			str_p += "\n"
		return str_p

	def get_prompt(self):
		return "Type the place of the number to change - e.g. 0 0 2.\nThis will change the number at 0 0 to 2, if possible\nUse 0 as the number entered to reset that space.\nEnter \"quit\" to exit\nEnter \"submit\" to reveal and check answer\nEnter Command: "

	def execute(self, arg):
		tokens = re.split(r"-|\s+", arg)
		if(int(tokens[2]) == 0):
			tokens[2] = -1
		if(self.reset_puzzle[int(tokens[0])][int(tokens[1])] == -1):
			self.visible_p[int(tokens[0])][int(tokens[1])] = int(tokens[2])

	def submit(self):
		correct = 0
		pre_placed = 0
		for x in range(0,9):
			for y in range(0,9):
				if(self.visible_p[x][y] == self.puzzle[x][y]):
					correct = correct + 1
				if(self.reset_puzzle[x][y] != -1):
					pre_placed += 1
		self.visible_p = self.puzzle
		return (correct - pre_placed, (81 - pre_placed))

puzzle = Sudoku()

#puzzle.hide_solution()
submitted = False

while(1):
	if(os.name is "nt"):
		os.system("cls")
	else:
		os.system("clear")
	print(puzzle)
	print(puzzle.verify())
	raw_input()

	print(puzzle.verify())
	break

	if(submitted == False):
		command = raw_input(puzzle.get_prompt())
		if(command == "quit"):
			break
		elif(command == "submit"):
			results = puzzle.submit()
			print("you got: " + str(results[0]) + " correct out of " + str(results[1]))
			raw_input("press enter to see solution...")
			submitted = True
		else:
			try:
				puzzle.execute(command)
			except:
				pass
	else:
		raw_input("press any key to start a new game")
		puzzle.generate()
		puzzle.hide_solution()
		submitted = False
if(os.name is "nt"):
	os.system("cls")
else:
	os.system("clear")