import re

class non_deterministic_automata:
    def __init__(self, regular_expression):
        # deve haver um preprocessamento para os espaços da expressão regular
        self.regular_expression = regular_expression
        self.states = {"0"}
        self.aphabet = set()
        self.start_state = "0"
        self.final_states = {}
        self.transitions = { 
            "0": { 
                "" : []
            }
        }

        #self.processRegularExpression()
        #self.createStates()

    def processRegularExpression(self):
        # stack e transition não devem ser atributos do nda 
        stack = []
        transition_stack = []
        quantity = 0
        operator_expected = False
        temporary_re = str(self.regular_expression)

        while temporary_re != "":
            re_pattern = r"\(\b[A-Za-z0-9._]+\,\b[A-Za-z0-9._]+\)+[|&]|\(\b[A-Za-z0-9._]+\)+[+*]"
            transition = re.search(re_pattern, temporary_re)

            self.processTransiton(transition)

            temporary_re = re.sub(re_pattern, f"T{quantity}", temporary_re, 1)

            quantity+=1
                
    def createStates(self):
        current_state = 0
        while len(self.transitions) > 0:
            self.states.add(str(current_state))
            break

    def processTransiton(self, transition_string):
        current_state = len(self.states)
        symbol_pattern = r"\b[A-Za-z0-9._]"

        symbols = re.findall(symbol_pattern, transition_string)

        if transition_string[-1] == "|":
            self.createORTransition(symbols)

        elif transition_string[-1] == "&":
            self.createANDTransition(symbols)

        elif transition_string[-1] == "*":
            self.createKleeneStarTransition(symbols)
        
        if transition_string[-1] == "+":
            self.createKleenePlusTransition(symbols)

    def print_transitions(self):
        for transition in self.transitions:
            print(transition)
            #if symbol == ')':
            #    operator_expected = True
                
    def createStates(self):
        pass

    def print_transitions(self):
        for transition in self.transitions:
            print(transition)

    def createORTransition(self, symbols):
        pass    
    
    def createANDTransition(self, symbols):
        pass

    def createKleeneStarTransition(self, symbols):
        pass

    def createKleenePlusTransition(self, symbols):
        pass
