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
		used_num = [0] * 11
		used_num[10] = 1
		buff = 10
		# first row permutation of 1-9
		for y in range(0,9):
			while(used_num[buff] != 0):
				buff = random.randrange(1, 10)
			self.puzzle[0][y] = buff
			used_num[buff] = 1

		for x in range(0, 10):
			used_num[x] = 0

		buff = 10
		used_num[self.puzzle[0][0]] = 1

		for x in range(1,9):
			while(used_num[buff] != 0):
				buff = random.randrange(1, 10)
			self.puzzle[x][0] = buff
			used_num[buff] = 1

		for x in range(0, 10):
			used_num[x] = 0

		# need to make this an array
		cur_col = [0] * 11
		cur_col[10] = 1
		count = 0
		retry_row = False
		# second row creation
		#for x in range(0,9):
		# test for x = 1 - 1, row before or second row
		# custom x range variable
		x = 0
		while(x < 8):
			x = x + 1
			if(retry_row == True):
				x = x - 1
				retry_row = False
			for y in range(1, 9):
				for z in range(0,x):
					cur_col[self.puzzle[z][y]] = 1

				used_num[self.puzzle[x][y - 1]] = 1
				count = 0
				while(cur_col[buff] != 0 or used_num[buff] != 0 and retry_row == False):
					buff = random.randrange(1,10)
					count = count + 1
					if(count > 100):
						retry_row = True
				self.puzzle[x][y] = buff
				# reset column checker
				for r in range(0,10):
					cur_col[r] = 0
				if(retry_row):
					#print("Retry row")
					for z in range(1,9):
						self.puzzle[x][z] = -1
					break
			for r in range(0,10):
				used_num[r] = 0
		self.visible_p = deepcopy(self.puzzle)

	def verify(self):
		used_num = [0] * 10
		for x in range (0,9):
			for y in range (0,9):
				if(used_num[self.puzzle[x][y]] == 1):
					return (False, y + 1, x + 1, self.puzzle[x][y])
				else:
					used_num[self.puzzle[x][y]] = 1
			#reset used numbers
			for r in range(0,10):
				used_num[r] = 0
		for y in range (0,9):
			for x in range (0,9):
				if(used_num[self.puzzle[x][y]] == 1):
					return (False, y + 1, x + 1, self.puzzle[x][y])
				else:
					used_num[self.puzzle[x][y]] = 1
			#reset used numbers
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
puzzle.generate()
puzzle.hide_solution()
submitted = False
while(1):

	if(os.name is "nt"):
		os.system("cls")
	else:
		os.system("clear")
	print(puzzle)
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