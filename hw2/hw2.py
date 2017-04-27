from pltrue import *

# Main Method
print("Has support for the following symbols: &|~ no support for >>\n\n")
values = {"S": False, "P": False, "Z": False}
sentence = "S & P | Z"
print("Testing: (" + sentence + ") with values " + str(values))
print("Result: " + str(PLTrue(sentence, values)))

sentence = "S | P & Z"
print("Testing: (" + sentence + ") with values " + str(values))
print("Result: " + str(PLTrue(sentence, values)))

sentence = "S | ~P | Z"
print("Testing: (" + sentence + ") with values " + str(values))
print("Result: " + str(PLTrue(sentence, values)))