import sys

from csci4342_Part2 import parse_program

def main():
	filename = sys.argv[1]
	parse_program(filename)
	interpreter(filename)

def interpreter(filename):
	
	#Initalizing memory map to store variables
	memory_map = {}
	
	with open(filename) as file:
		
		for line in file:
			line = line.strip() #Removing leading and trailing spaces
			
			if line.startswith("var"):
				line = line.replace("var", "var").strip() #skips the var keyword and continues to the next line
				
			if ":" in line:
				declaration_line = line.split(':')[0].strip() #get the variables
				variables = [var.strip() for var in declaration_line.split(",")]
				#Adding variables to the memory map 
				for var in variables:
					if var not in memory_map:
						memory_map[var] = 0 #Initialize the variables with zeros
						
			if line.startswith("read"):
				var_name = line[line.find("(") + 1 : line.find(")")].strip()
				memory_map[var_name] = int(input(f"Enter value for {var_name}: "))
			
			if ":=" in line:
				var_name, expression = line.split(":=")
				var_name = var_name.strip(";")
				expression = expression.strip(";")
				
				if expression.strip().isdigit():
					memory_map[var_name.strip()] = int(expression.strip())
				else:
					memory_map[var_name.strip()] = evaluate_exp(expression.strip(), memory_map)
			
			if line.startswith("write"):
				var_name = line[line.find("(") + 1 : line.find(")")].strip()
				print(memory_map.get(var_name, "Undefined variable"))
				
	
def evaluate_exp(expression, memory_map):
	expression = expression.replace(" ", "")
	
	#Checking for the addition operation
	if "+" in expression:
		operands = expression.split("+")
		total = 0
		for operand in operands:
			#look up each value in the memory map
			if operand.strip().isdigit(): #if it is a literal number
				total += int(operand.strip())
			if operand in memory_map:
				total += memory_map.get(operand.strip(), 0)
				
		return total
	
	#Checking for the substracton operation
	elif "-" in expression:
		operands = expression.split("-")
		total = 0
		for i, operand in enumerate(operands):
			if operand.strip().isdigit():
				if i == 0:
					total += int(operand.strip())
				else:
					total -= int(operand.strip())
			if operand in memory_map:
				if i == 0:
					total += memory_map.get(operand.strip(), 0)
				else:
					total -= memory_map.get(operand.strip(), 0)		
							
		return total
	
	#Checking for the multiplication operation	
	elif "*" in expression:
		operands = expression.split("*")
		total = 0
		for i, operand in enumerate(operands):
			if operand.strip().isdigit():
				if i == 0:
					total += int(operand.strip())
				else:
					total *= int(operand.strip())
			if operand in memory_map:
				if i == 0:
					total += memory_map.get(operand.strip(), 0)
				else:
					total *= memory_map.get(operand.strip(), 0)		
							
		return total
		
	#Checking for the division operation
	elif "div" in expression:
		operands = expression.split("div")
		total = 0
		for i, operand in enumerate(operands):
			if operand.strip().isdigit():
				if i == 0:
					total += int(operand.strip())
				else:
					total /= int(operand.strip())
			if operand in memory_map:
				if i == 0:
					total += memory_map.get(operand.strip(), 0)
				else:
					total /= memory_map.get(operand.strip(), 0)		
							
		return total

if __name__ == "__main__":
	main()





