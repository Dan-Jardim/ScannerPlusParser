import re

class minor_automata:
    def __init__(self, states, transitions, start_state, final_states, alphabet):
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.alphabet = alphabet

    def add_transition(self, symbol, new_state):
        self.alphabet.add(symbol)
        self.final_states.add(new_state)
        start_transition = self.transitions[self.start_state]

        if symbol in start_transition:
            start_transition[symbol].append(new_state)

        self.transitions[self.start_state] = start_transition

    def __add__(self, other):
        self.alphabet = self.alphabet | other.alphabet
        self.final_states = self.final_states | other.final_states
        transition = self.transitions[self.start_state]

        for symbol, states in other.transitions[other.start_state]:
            if symbol in transition:
                for state in states:
                    transition[symbol].append(state)
            else:
                transition[symbol] = states

        self.transitions[self.start_state] = transition
        


class non_deterministic_automata:
    def __init__(self, regular_expression):
        # deve haver um preprocessamento para os espaços da expressão regular
        self.regular_expression = regular_expression
        self.states = {"0"}
        self.alphabet = set()
        self.start_state = "0"
        self.final_states = {}
        self.transitions = { 
            "0": { 
                "" : []
            }
        }

        self.sub_automatas = dict()

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

            self.processTransiton(transition.group())

            sub_automata = f"SUBAUTOMATA.{len(self.sub_automatas)}"

            temporary_re = re.sub(re_pattern, 
                                  sub_automata, 
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

        if "SUBAUTOMATA." not in symbols[0]:
            self.alphabet.add(symbols[0])

        if "SUBAUTOMATA." not in symbols[-1]:
            self.alphabet.add(symbols[-1])

        if transition_string[-1] == "|":
            self.createORTransition(symbols)

        elif transition_string[-1] == "&":
            self.createANDTransition(symbols)

        elif transition_string[-1] == "*":
            self.createKleeneStarTransition(symbols)
        
        if transition_string[-1] == "+":
            self.createKleenePlusTransition(symbols)
                
    def createStates(self):
        pass 

    def print_transitions(self):
        for transition in self.transitions:
            print(transition)

    def createORTransition(self, symbols):
        #esse caso só ocorre quando não há transição
        sub_nfas = []

        single_symbol = ""

        if "SUBAUTOMATA." in symbols[0]:
            sub_nfas.append(self.sub_automatas[symbols[0]])

            single_symbol = symbols[1]

        if "SUBAUTOMATA." in symbols[1]:
            sub_nfas.append(self.sub_automatas[symbols[1]])

            single_symbol = symbols[0]

        if len(sub_nfas) == 2:
            sub_nfa = sub_nfas[0] + sub_nfas[1]
        
        elif len(sub_nfas) == 0:
            current_state = len(self.states)
            
            finals = [str(current_state+1), 
                      str(current_state+2)]

            states = str(current_state)

            transitions = {
                str(current_state) : { 
                    str(symbols[0]) : [finals[0]],
                    str(symbols[1]) : [finals[1]]
                }
            }

            sub_nfa = minor_automata(
                states,
                transitions,
                str(current_state), 
                {finals[0], finals[1]},
                {symbols[0], symbols[1]}
            )

            self.states.add(str(current_state))
            self.states.add(str(current_state+1))
            self.states.add(str(current_state+2))

        else:
            current_state = len(self.states)

            sub_nfas[0].add_transition(single_symbol, current_state)

            sub_nfa = sub_nfas[0]

            self.states.add(str(current_state))

        sub_nfa_str = f"SUBAUTOMATA.{len(self.sub_automatas) + 1}"

        self.sub_automatas[sub_nfa_str] = sub_nfa
    
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
    

#def main():
#    my_regex = ["(((alpha,beta)|,(alpha,Empty)|)&)*",
#                "((alpha,beta)|,alpha)|"]
#    
#    test_nda = non_deterministic_automata(my_regex[1])
#
#    test_nda.print_transitions()
