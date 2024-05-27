import re
import Scanner.nfa as nfa

class DeterministicFiniteAutomata(nfa.NondeterministicFiniteAutomata):
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

        new_states = { }

        destination_state = ""

        for state, transition in transitions.items():
            new_transitions = {}

            for symbol, destinies in transition.items():
                str_destinies = " ".join(destinies)
                if len(destinies) == 0:
                    destination_state = ''

                elif len(destinies) > 1:
                    if str_destinies in new_states:
                        destination_state = new_states[str_destinies]
                    else:
                        destination_state = str(len(self.states)+1)
                        self.states.add(destination_state)
                        new_states[str_destinies] = destination_state
                
                else:
                    destination_state = destinies[0]
                
                new_transitions[symbol] = destination_state
                       
            self.transitions[state] = new_transitions

        while len(new_states) > 0:
            str_originals = next(iter(new_states))
            new_state = new_states[str_originals]

            new_transition = {}

            destinies = set()

            originals = str_originals.split()
            
            for symbol in self.alphabet:
                for original_state in originals:
                    if original_state in self.transitions:
                        destinies.add(self.transitions[original_state][symbol])

                    if original_state in self.final_states:
                        self.final_states.add(new_state)

                str_destinies = " ".join(destinies)

                if str_destinies != "":

                    if str_destinies not in new_states:
                        new_states[str_destinies] = str(len(self.states+1))
                        self.states.add(new_states[str_destinies])

                    new_transition[symbol] = new_states[str_destinies]
            

            new_state = new_states[str_originals]
            self.transitions[new_state] = new_transition

            new_states.pop(str_originals)

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
            if unreacheble_state in self.final_states:
                self.final_states.remove(unreacheble_state)

    def read_word(self, word):
        current_state = self.start_state

        word_match = False

        for letter in word:
            current_symbol = ""
            for symbol in self.alphabet:
                if re.match(symbol, word):
                    current_symbol = symbol
                    word_match = True
                    break
                elif re.match(symbol, letter):
                    current_symbol = symbol
                    break
    
            current_transition = self.transitions[current_state]

            if current_symbol not in current_transition:
                return False
            
            current_state = current_transition[current_symbol]

            if len(current_state) == 0:
                return False
            
            if word_match:
                return True
            
        return (current_state in self.final_states)
    

def createAutomata(regular_expression):
    NonDeterministic = nfa.NondeterministicFiniteAutomata(regular_expression)

    nfa.fill_symbols_transition(NonDeterministic)
    nfa.remove_empty_transitions(NonDeterministic)

    automata = DeterministicFiniteAutomata(NonDeterministic)

    return automata
