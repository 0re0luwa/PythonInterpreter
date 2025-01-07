import sys

from csci4342_Part2 import parse_program

def main():
	filename = sys.argv[1]
	interpret_program(filename)
	
def interpret_program(filename):
	#Read the program lines
	with open(filename, 'r') as file:
		lines = [line.strip() for line in file if line.strip()]
		
		
	#Initialize variables 
	memory_map = {}
	procedures = {}
	index = 0
	
	
	program_body = []
	while index < len(lines):
		line = lines[index]
		if line.startswith("procedure"):
			procedure_name = line.split()[1].strip(";")
			procedure_body = []
			index += 1
			while not lines[index].startswith("end ;"):
				procedure_body.append(lines[index])
				index += 1
			procedures[procedure_name] = procedure_body
			
		elif line == "begin":
			index += 1
			while lines[index] != "end .":
				program_body.append(lines[index])
				index += 1
		index += 1
		
	#Interpret the main program
	interpret_block(program_body, memory_map, procedures)
	
	
def interpret_block(lines, memory_map, procedures):
	"""Execute a block of code."""
	index = 0
	while index < len(lines):
		line = lines[index]
		
		#Handle read statement
		if line.startswith("read"):
			var_name = line[line.find("(") + 1:line.find(")")].strip()
			memory_map[var_name] = int(input(f"Enter value for {var_name}: "))
			
		if line.startswith("write"):
			var_name = line[line.find("(") + 1:line.find(")")].strip()
			print(memory_map.get(var_name, "Undefined variable"))
			
		if ":=" in line:
			
			statements = line.split(";")
			for statement in statements:
				statement = statement.strip()
				if statement:
					if ":=" in statement:
						parts = statement.split(":=")
						if len(parts) == 2:
							var_name = parts[0].strip()
							expression = parts[1].strip()
							memory_map[var_name.strip()] = evaluate_expression(expression.strip(), memory_map)
						else:
							raise ValueError(f"Malformed assignment statement: {statement}")
			
		#handle if statement
		if line.startswith("if"):
			codition = line[line.find("(") + 1:line.find(")")].strip()
			then_block = []
			else_block = []
			index += 1
			
			while not lines[index].startswith("else") and not lines[index].startswith("end"):
				then_block.append(lines[index])
				index += 1
			if lines[index].startswith("else"):
				index += 1
				while not lines[index].startwith("end"):
					else_block.append(lines[index])
					index += 1
					
			if evaluate_codition(condition, memory_map):
				interpret_block(then_block, memory_map, procedures)
			else:
				interpret_block(else_block, memory_map, procedures)
				
		#Handle while loops
		if line.startswith("while"):
			condition = line[line.find("(") + 1:line.find(")")].strip()
			loop_block = []
			index += 1
			while not lines[index].startswith("end"):
				loop_block.append(lines[index])
				index += 1
			
			while evaluate_condition(condition, memory_map):
				i = memory_map["i"]
				s = memory_map["s"]
				memory_map["s"] = soma(i, s)
				
				interpret_block(loop_block, memory_map, procedures)
				memory_map["i"] += 1
				
				
		#Handle procedure calls
		if line in procedures:
			procedure_body = procedures[line]
			local_memory = memory_map.copy() #Create a local scope
			interpret_block(procedure_body, local_memory, procedures)
			memory_map.update(local_memory) # Merge changes back to global scope
			
		index += 1
		
		
def evaluate_expression(expression, memory_map):
	"""Evaluate a mathematical expression."""
	expression = expression.replace("div", "//")
	return eval(expression, {}, memory_map)
	

def evaluate_condition(condition, memory_map):
	"""Evaluate a boolean condition."""
	condition = condition.replace("div", "//").replace(":=", "=").strip("do").strip("while")
	
	return eval(condition, {}, memory_map)
	
def soma(i, s):
	q = i * i
	if(i / 2) * 2 == i: 
		s = s + q
	else:
		s = s - q
	print(f"After i = {i}, q = {q}, s = {s}")
	return s

if __name__ == "__main__":
	main()
					
	
	
