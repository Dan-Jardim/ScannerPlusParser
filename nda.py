import 

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
        self.createStates()

    def processRegularExpression(self):
        # stack e transition não devem ser atributos do nda 
        stack = []
        transition_stack = []
        quantity = 0
        operator_expected = False

        for symbol in self.regular_expression:
            stack.append(symbol)

            if operator_expected == True:
                operator_expected = False
                
                string = ""
                transition_stack.append(stack.pop())
                
                while(stack[-1] != '('):
                    if (stack[-1] == ","):
                        string += stack.pop()
                    else:
                        transition_stack.append(string)
                        transition_stack.append(stack.pop())

                        string = ""

                transition_stack.append(stack.pop())
                transition_stack.reverse()

                self.processTransiton(transition_stack)
                
                transition_stack = []

                stack.append(f'transition[{quantity}]')

                quantity += 1

            if symbol == ')':
                operator_expected = True
                
    def createStates(self):
        current_state = 0
        while len(self.transitions) > 0:
            self.states.add(str(current_state))
            break

    def processTransiton(self, transition_stack):
        current_state = len(self.states)

        symbol = ""

        for i in transition_stack:
            if i in "(,)":
                continue
            
            
            self.aphabet.add(i)

            self.transitions[str(current_state)] = {
                i : [str(current_state+1)]
            }

        pass

    def print_transitions(self):
        for transition in self.transitions:
            print(transition)
            if symbol == ')':
                operator_expected = True
                
    def createStates(self):
        pass

    def processTransiton(self):
        pass

    def print_transitions(self):
        for transition in self.transitions:
            print(transition)


