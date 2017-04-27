import re
def PLTrue(s, m):
	operand_alph = "&|>><<"
	def parse(inp):
		tokens = re.split("\s+", inp)
		return tokens
	def and_op(bool1, bool2):
		if(bool1 and bool2):
			return True
		else:
			return False
	def or_op(bool1, bool2):
		if(bool1 or bool2):
			return True
		else:
			return False

	tokens = parse(s)
	arguments = []
	symbols = []
	symbol_status = {}
	current_status = True
	previous_status= True
	for x in tokens:
		if(operand_alph.find(x) != -1):
			symbols.append(x)
		else:
			arguments.append(x)

	#print("Arguments: " + str(arguments))
	#print("Symbols: " + str(symbols))

	# Solve using the defined lists and dicts
	for x in range(0, len(arguments)):
		current_status = m.get(arguments[x].replace("~", ""))
		if(arguments[x].find("~") != -1):
			current_status = not current_status
		if(x == 0 and len(arguments) > 1):
			previous_status = m.get(arguments[x + 1])
		if(current_status == None):
			raise Exception("Symbol used, not contained")

		if(symbols[x - 1] == "&"):
			previous_status = and_op(current_status, previous_status)
		elif(symbols[x - 1] == "|"):
			previous_status = or_op(current_status, previous_status)

	if(current_status and previous_status):
		pass
	else:
		current_status = previous_status
	return current_status