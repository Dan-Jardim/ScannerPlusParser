import re

class MinorAutomata:
    def __init__(self, states, transitions, start_state, final_states, alphabet):
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.alphabet = alphabet

    def or_symbol(self, symbol, new_state):
        self.alphabet.add(symbol)
        self.final_states.add(new_state)
        start_transition = self.transitions[self.start_state]

        if symbol in start_transition:
            start_transition[symbol].append(new_state)
        else:
            start_transition[symbol] = [new_state]

        self.transitions[self.start_state] = start_transition

        return self

    def and_symbol(self, symbol, new_state):
        self.alphabet.add(symbol)

        for final in self.final_states:
            if final in self.transitions:
                final_transition = self.transitions[final]

                if symbol in final_transition:
                    final_transition[symbol].append(new_state)
                else:
                    final_transition[symbol] = [new_state]

            else:
                self.transitions[final] = {
                    symbol : [new_state]
                }

        self.final_states.clear()
        self.final_states.add(new_state)

        return self

    def kleene_plus_transition(self):
        symbol = ""

        for final in self.final_states:
            if final in self.transitions:
                final_transition = self.transitions[final]

                if symbol in final_transition:
                    final_transition[symbol].append(self.start_state)
                else:
                    final_transition[symbol] = [self.start_state]

            else:
                self.transitions[final] = {
                    symbol : [self.start_state]
                }

        return self

    def kleene_star_transition(self):
        self.kleene_plus_transition()

        self.final_states.add(self.start_state)

        return self

    def or_transition(self, other):
        self.alphabet = self.alphabet | other.alphabet
        self.final_states = self.final_states | other.final_states
        transition = self.transitions[self.start_state]

        for symbol in other.transitions[other.start_state]:
            states = other.transitions[other.start_state][symbol]

            if symbol in transition:
                for state in states:
                    transition[symbol].append(state)
            else:
                transition[symbol] = states

        self.transitions[self.start_state] = transition

        self.transitions = self.transitions | other.transitions

        del self.transitions[other.start_state]

        return self

    def and_transition(self, other):
        self.alphabet = self.alphabet | other.alphabet

        for final in self.final_states:
            if final in self.transitions:
                final_transition = self.transitions[final]

                if "" in final_transition:
                    final_transition[""].append(other.start_state)
                else:
                    final_transition[""] = [other.start_state]

            else:
                self.transitions[final] = {
                    "" : [other.start_state]
                }

        self.transitions = self.transitions | other.transitions

        self.final_states = other.final_states

        return self
        


class NondeterministicFiniteAutomata:
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

        sub_automata = ""
        
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

        ultimate_automata = self.sub_automatas[sub_automata]

        self.transitions = ultimate_automata.transitions
        self.alphabet = ultimate_automata.alphabet
        self.start_state = ultimate_automata.start_state
        self.final_states = ultimate_automata.final_states
        
                
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

    def print_transitions(self):
        for state, transition in self.transitions.items():
            print(state, " -> ", transition)

    def print_automata(self):
        print("Start: ",self.start_state)
        print("Alphabet: ", self.alphabet)
        print("States: ", self.states)
        self.print_transitions()
        print("End States: ", self.final_states)

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
            sub_nfa = sub_nfas[0]
            sub_nfa.or_transition(sub_nfas[1])
        
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

            sub_nfa = MinorAutomata(
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

            sub_nfas[0].or_symbol(single_symbol, current_state)

            sub_nfa = sub_nfas[0]

            self.states.add(str(current_state))

        sub_nfa_str = f"SUBAUTOMATA.{len(self.sub_automatas) + 1}"

        self.sub_automatas[sub_nfa_str] = sub_nfa
    
    def createANDTransition(self, symbols):
        sub_nfas = []

        single_symbol = ""

        if "SUBAUTOMATA." in symbols[0]:
            sub_nfas.append(self.sub_automatas[symbols[0]])

            single_symbol = symbols[1]

        if "SUBAUTOMATA." in symbols[1]:
            sub_nfas.append(self.sub_automatas[symbols[1]])

            single_symbol = symbols[0]

        if len(sub_nfas) == 2:
            sub_nfa = sub_nfas[0]
            sub_nfa.and_transition(sub_nfas[1])
        
        elif len(sub_nfas) == 0:
            current_state = len(self.states)
            
            final = str(current_state+2)

            states = str(current_state)

            transitions = {
                str(current_state) : { 
                    str(symbols[0]) : [str(current_state+1)]
                },
                str(current_state+1) : {
                    str(symbols[1]) : [final]
                }
            }

            sub_nfa = MinorAutomata(
                states,
                transitions,
                str(current_state), 
                {final},
                {symbols[0], symbols[1]}
            )

            self.states.add(str(current_state))
            self.states.add(str(current_state+1))
            self.states.add(str(current_state+2))

        else:
            if single_symbol == symbols[1]:
                current_state = len(self.states)

                sub_nfa = sub_nfas[0]

                sub_nfa.and_symbol(single_symbol, current_state)

            else:
                transition = {
                    str(current_state) : { 
                        single_symbol : [str(current_state+1)]
                    }
                }

                sub_nfa = MinorAutomata(
                    {str(current_state), str(current_state+1)},
                    transition,
                    str(current_state),
                    {str(current_state+1)},
                    {single_symbol}
                )

                sub_nfa.and_transition(sub_nfas[0])
                

            self.states.add(str(current_state))

        sub_nfa_str = f"SUBAUTOMATA.{len(self.sub_automatas) + 1}"

        self.sub_automatas[sub_nfa_str] = sub_nfa

    def createKleeneStarTransition(self, symbols):

        if "SUBAUTOMATA." in symbols[0]:
            sub_nfa = self.sub_automatas[symbols[0]]

            sub_nfa.kleene_star_transition()
            
        else:
            current_state = len(self.states)

            transition = {
                str(current_state) : {
                    symbols[0] : str(current_state)
                }
            }

            sub_nfa = MinorAutomata(
                    {str(current_state)},
                    transition,
                    str(current_state),
                    {str(current_state)},
                    {symbols[0]}
            )

            self.states.add(str(current_state))


        sub_nfa_str = f"SUBAUTOMATA.{len(self.sub_automatas) + 1}"

        self.sub_automatas[sub_nfa_str] = sub_nfa

    def createKleenePlusTransition(self, symbols):

        if "SUBAUTOMATA." in symbols[0]:
            sub_nfa = self.sub_automatas[symbols[0]]

            sub_nfa.kleene_plus_transition()
              
        else:
            current_state = len(self.states)

            transition = {
                str(current_state) : {
                    symbols[0] : str(current_state+1)
                },
                str(current_state+1) : {
                    symbols[0] : str(current_state+1)
                }
            }

            sub_nfa = MinorAutomata(
                    {str(current_state), str(current_state+1)},
                    transition,
                    str(current_state),
                    {str(current_state+1)},
                    {symbols[0]}
            )

            self.states.update({
                str(current_state), 
                str(current_state+1)
            })
            

        sub_nfa_str = f"SUBAUTOMATA.{len(self.sub_automatas) + 1}"

        self.sub_automatas[sub_nfa_str] = sub_nfa

    def get_parents_state(self, state):
        parents = {}
        for current_state, transition in self.transitions.items():
            for symbol, destinies in transition.items():
                if state in destinies:
                    parents.add((current_state, symbol))

        return parents



def fill_symbols_transition(nfa):
    for transition in nfa.transitions.values():
        for symbol in nfa.alphabet:
            if symbol not in transition:
                transition[symbol] = []

def remove_empty_transitions(nfa):
    remove_empty_child(nfa)
    remove_empty_parent(nfa)

def remove_empty_child(nfa):
    for state, transition in nfa.transitions.items():
        if '' in transition:
            parents = []
            
            while len(transition['']) > 0:
                child_state = transition[''][0]
                
                if child_state not in nfa.transitions:
                    parents.append(child_state)
                    continue

                for child_transition in nfa.transitions[child_state].items():
                    transition[child_transition[0]].extend(child_transition[1])
                
                transition[''].remove(child_state)
            
            if len(parents) > 0:
                transition[''].extend(parents)
            else:
                transition.pop('')

def remove_empty_parent(nfa):
    
    for state, transition in nfa.transitions.items():
        if state == nfa.start_state:
            continue

        if '' in transition:
            symbols = {}

            parents = nfa.get_parents_state(state)
            
            while len(transition['']) > 0:
                child_state = transition[''][0]

                for parent in parents:
                    nfa.transitions[parent[0]][parent[1]].append(child_state)

                transition[''].remove(child_state)

            transition.pop('')
class DeterministicFiniteAutomata(NondeterministicFiniteAutomata):
    def __init__(self, nfa):
        self.start_state = nfa.start_state
        self.states = nfa.states
        self.alphabet = nfa.alphabet
        self.final_states = nfa.final_states
        
        self.create_new_states(nfa.transitions)

        self.remove_unreachables()

    def convert_nfa(self, nfa):
        pass

    def create_new_states(self, transitions):
        self.transitions = {}

        new_states = {}

        for state, transition in transitions.items():
            new_transitions = {}

            for symbol, destinies in transition.items():
                
                if len(destinies) == 0:
                    destination_state = ''

                elif len(destinies) > 1:
                    if destinies in new_states:
                        destination_state = new_states[destinies]
                    else:
                        destination_state = str(len(self.states+1))
                        self.states.add(destination_state)
                        new_states[destinies] = destination_state
                
                else:
                    destination_state = destinies[0]
                
                new_transitions[symbol] = destination_state
                       
            self.transitions[state] = new_transitions

        while len(new_states) > 0:
            originals = new_states.keys()[0]
            new_state = new_states[originals]

            new_transition = {}

            destinies = {}
            
            for symbol in self.alphabet:
                for original_state in originals:
                    destinies.add(self.transitions[original_state][symbol])

                    if original_state in self.final_states:
                        self.final_states.add(new_state)

                if destinies not in new_states:
                    new_states[destinies] = str(len(self.states+1))
                    self.states.add(new_states[destinies])

                new_transition[symbol] = new_states[destinies]
            

            new_state = new_states[originals]
            self.transitions[new_state] = new_transition

            new_states.pop(new_state)

    def remove_unreachables(self):
        reachebles = {self.start_state}

        for transition in self.transitions.values():
            for reacheble_state in transition.values():
                reachebles.add(reacheble_state)
        
        unreachebles = self.states - reachebles

        for unreacheble_state in unreachebles:
            self.states.remove(unreacheble_state)
            if unreacheble_state in self.transitions:
                self.transitions.pop(unreacheble_state)