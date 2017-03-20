import random
import os
class Sudoku:
	def __init__(self):
		self.puzzle = []
		for x in range(0,9):
			self.puzzle.append([])
			for y in range(0, 9):
				self.puzzle[x].append(-1)
		self.visible_p = self.puzzle
				
	def __str__(self):
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
		# second row creation
		#for x in range(0,9):
		# test for x = 1 - 1, row before or second row
		for y in range(1,9):
			cur_col[self.puzzle[0][y]] = 1
			# 1 so current row
			used_num[self.puzzle[1][y - 1]] = 1
			while(cur_col[buff] != 0 or used_num[buff] != 0):
				print(str(cur_col) + "::::::" + str(used_num) + "::::" + str(buff))
				buff = random.randrange(1,10)
			self.puzzle[1][y] = buff
			# reset column checker
			for x in range(0,10):
				cur_col[x] = 0



test = Sudoku()
test.generate()
'''
if(os.name is "nt"):
	os.system("cls")
else:
	os.system("clear")
'''
print(test)
