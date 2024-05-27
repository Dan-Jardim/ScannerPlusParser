import dfa
import scanner as sc
import sys

BasicER = "BasicRegularExpressions.csv"

def mainTest():
    
    my_regex = ["(((a,b)|,(a,d)|)&)*",
                "((a,b)|,a)|",
                "([0-9])+"]
    
    test_dfa = dfa.createAutomata(my_regex[2])
    test_dfa.print_automata()

    dfas = sc.read_regex_file(BasicER)
    
    print("DONE")

def main(source_code):
    BasicScanner = sc.Scanner(BasicER)

    codeFile = open(source_code, "r")
    
    code = codeFile.read()

    tokens = BasicScanner.run_scanner(text=code)


    parser_input = []
    
    for token in tokens:
        if token.type == "KEY_WORD":
            parser_input.append(token.value)
        else:
            parser_input.append(token.type)

    for entrada in parser_input:
        print(entrada)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        code = input("Enter the source code files: ")
        if code == "":
            code = "SimpleCode.bas"
    else:
        code = sys.argv[1]

    main(code)