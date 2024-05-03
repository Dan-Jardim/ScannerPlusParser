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

        self.processRegularExpression()
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

            if not transition:
                break

            start = len(self.states)

            ends = self.processTransiton(transition.group())

            temporary_re = re.sub(re_pattern, 
                                  f"TRANSITION.{start}_{"_".join(str(i) for i in ends)}", 
                                  temporary_re, 
                                  1)

            quantity+=1
                
    def createStates(self):
        current_state = 0
        while len(self.transitions) > 0:
            self.states.add(str(current_state))
            break

    def processTransiton(self, transition_string):
        symbol_pattern = r"\b[A-Za-z0-9._]+" 
        symbols = re.findall(symbol_pattern, transition_string)

        ends = []

        if transition_string[-1] == "|":
            ends = self.createORTransition(symbols)

        elif transition_string[-1] == "&":
            ends = self.createANDTransition(symbols)

        elif transition_string[-1] == "*":
            ends = self.createKleeneStarTransition(symbols)
        
        if transition_string[-1] == "+":
            ends = self.createKleenePlusTransition(symbols)

        return ends

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
        #esse caso só ocorre quando não há transição
        current_state = len(self.states)
        equivalent_state = -1

        if "TRANSITION." in symbols[0]:
            current_state = re.search(r"\.\d+", symbols[0])
        else:
            self.aphabet.add(symbols[0])

        if "TRANSITION." in symbols[1]:
            equivalent_state = re.findall(r"\.\d+", symbols[-1])

        else:
            self.add(symbols[-1])

        finals = [str(current_state+1), 
                  str(current_state+2)]
        
        self.transitions[str(current_state)] = { 
            str(symbols[0]) : [finals[0]],
            str(symbols[1]) : [finals[1]]
        }

        self.states.update({
            str(current_state),
            finals[0],
            finals[1]
            })
        
        return finals
    
    def createANDTransition(self, symbols):
        current_state = len(self.states)
        finals = [str(current_state+2)]

        self.transitions[str(current_state)] = { 
            str(symbols[0]) : [str(current_state+1)]
        }

        self.transitions[str(current_state+1)] = { 
            str(symbols[1]) : finals
        }

        self.states.update({
            str(current_state), 
            str(current_state+1), 
            finals[0]
            })
        
        return finals

    def createKleeneStarTransition(self, symbols):
        current_state = len(self.states)

        finals = [str(current_state)]

        self.transitions[str(current_state)] = { 
            str(symbols[0]) : finals
        }

        self.states.add(finals[0])

        return finals

    def createKleenePlusTransition(self, symbols):
        current_state = len(self.states)
        finals = [str(current_state+1)]

        self.transitions[str(current_state)] = { 
            str(symbols[0]) : finals
        }

        self.transitions[str(current_state+1)] = { 
            str(symbols[0]) : finals
        }

        self.states.update({
            str(current_state), 
            finals[0]
        })

        return finals
    
