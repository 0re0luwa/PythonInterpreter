#import system module for line command arguments
import sys 

def main():
	filename = sys.argv[1]
	tokens = lexical_analyzer(filename)

# Lists of the token rules
reservedToken ={"program", "var", "procedure", "begin", "if", "then", "else", "end", "read", "while", "do", "write", "not", "of", "array"}
specialToken = {";", ",", ":", "(", ")", ".", ".."}
dataTypeToken = {"integer"}
assignmentToken = {":="}
multiplicationToken = {"*", "div", "and"}
relationToken = {"=", "<=", ">=", "<", ">", "<>"}
additionToken = {"+", "-", "or"}
booleanToken = {"true", "false"}

def tokenize_line(line):
	tokens = []
	
	for string in line.split():
	
		if string in reservedToken:
			tokens.append((string, "Reserved Token"))
			
		elif string in specialToken:
			tokens.append((string, "Special Token"))
			
		elif string in dataTypeToken:
			tokens.append((string, "Data Type Token"))
			
		elif string in assignmentToken:
			tokens.append((string, "Assignment Token"))
			
		elif string in multiplicationToken:
			tokens.append((string, "Multiplication Token"))
			
		elif(string.isdigit()):
			tokens.append((string, "Integer Token"))
			
		elif string in relationToken:
			tokens.append((string, "Relation Token"))
			
		elif string in additionToken:
			tokens.append((string, "Addition Token"))
			
		elif(string.isidentifier()):
			tokens.append((string, "Identifier Token"))
			
		elif string in booleanToken:
			tokens.append((string, "Boolean Token"))
			
		elif(string.isalpha()):
			tokens.append((string, "Letter Token"))
			
		else:
			tokens.append((string, "Invalid Token"))
			
	return tokens
			
				
		
def lexical_analyzer(filename):

	tokens = []

	with open(filename) as file:
	
		for line in file:
			tokens = tokenize_line(line)
			for token, token_type in tokens:
				print(f"{token} : {token_type}")
	#return tokens

		
if __name__ == "__main__":
	main()

					
			
					
				
		
        	

