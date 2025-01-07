#import sys to take in arguments from the command line
import sys

#import the tokenize_line function from the csci4342_Part1 lexical analyzer to be used in this file
from csci4342_Part1 import tokenize_line 

#This function defining the program stream
def parse_program(stream):
    tokens = []
    for line in stream:
        tokens.extend(tokenize_line(line))  # Tokenize each line and add to the tokens list
    
    current_token = 0  # Pointer to track the current token

    def expect(expected_type):
        nonlocal current_token
        if current_token < len(tokens):
            token, token_type = tokens[current_token]
            if token_type == expected_type:
                current_token += 1
                return token
            else:
                print("Error: Incorrect Syntax")
                sys.exit(1)
        else:
            print("Error: Inccorect Syntax")
            sys.exit(1)

    print("No Syntax Error")

#This function is to check the syntac of blocks
def parse_block():
    expect("Reserved Token")  # Checking for "var"
    parse_variable_declarations()  # calling Parse variable declarations
    parse_procedure_declarations()  # calling Parse procedure declarations
    expect("Reserved Token")  # Checking for "begin"
    parse_statements()  # Parsing the the main statements
    expect("Reserved Token")  # Checking for "end"

#This function is to check the syntax of variable declarations
def parse_variable_declarations():
    while True:
        if tokens[current_token][1] == "Identifier Token":  # Expecting variable names
            expect("Identifier Token")
            while tokens[current_token][0] == "Special Token" and tokens[current_token][1] == ",":
                expect("Special Token")  # Handling commas
                expect("Identifier Token")  # Next variable name
            expect("Special Token")  # Expecting ":"
            expect("Data Type Token")  # Expecting "integer"
            expect("Special Token")  # Expecting ";"
        else:
            break

#this function is to test the syntax of procedure declarations
def parse_procedure_declarations():
    while current_token < len(tokens) and tokens[current_token][1] == "Reserved Token" and tokens[current_token][0] == "procedure":
        expect("Reserved Token")  # Checking for "procedure"
        expect("Identifier Token")  # Checking for procedure name
        expect("Special Token")  # Expecting ";"
        parse_block()  # Parsing the procedure's block
        expect("Special Token")  # Expecting ";"

#This function is to check the syntax of statements
def parse_statements():
    while current_token < len(tokens):
        if tokens[current_token][1] == "Identifier Token":
            expect("Identifier Token")  # Expecting identifier for assignment
            expect("Assignment Token")  # Expecting ":="
            parse_expression()  # Parse the expression after assignment
            expect("Special Token")  # Expecting ";"
        elif tokens[current_token][1] == "Reserved Token" and tokens[current_token][0] == "if":
            parse_if_statement()
        elif tokens[current_token][1] == "Reserved Token" and tokens[current_token][0] == "while":
            parse_while_statement()
        else:
            break

#This function is to check the syntax of expressions
def parse_expression():
    if tokens[current_token][1] == "Integer Token":
        expect("Integer Token")  # Accepting integer token
    elif tokens[current_token][1] == "Identifier Token":
        expect("Identifier Token")  # Accepting identifier token
    else:
        print(f"Error: Invalid expression at {tokens[current_token]}")
        sys.exit(1)

#This function is to check the syntax of if else then statements
def parse_if_statement():
    expect("Reserved Token")  # Expecting "if"
    expect("Special Token")  # Expecting "("
    parse_expression()  # Parsing the condition expression
    expect("Special Token")  # Expecting ")"
    expect("Reserved Token")  # Expecting "then"
    parse_statements()  # Parsing then branch
    if current_token < len(tokens) and tokens[current_token][1] == "Reserved Token" and tokens[current_token][0] == "else":
        expect("Reserved Token")  # Expecting "else"
        parse_statements()  # Parsing else branch

#This function is to check the syntax of a do while statement
def parse_while_statement():
    expect("Reserved Token")  # Expecting "while"
    expect("Special Token")  # Expecting "("
    parse_expression()  # Parsing the condition expression
    expect("Special Token")  # Expecting ")"
    expect("Reserved Token")  # Expecting "do"
    parse_statements()  # Parsing the statements inside the loop

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    with open(filename) as file:
        parse_program(file)
