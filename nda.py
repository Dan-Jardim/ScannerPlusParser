class non_deterministic_automata:
    def __init__(self, regular_expression):
        # deve haver um preprocessamento para os espaços da expressão regular
        self.regular_expression = regular_expression
        self.transitions = []
        self.states = []
        self.processRegularExpression()

    def processRegularExpression(self):
        # stack e transition não devem ser atributos do nda 
        stack = []
        transition = []
        quantity = 0
        operator_expected = False

        for symbol in self.regular_expression:
            stack.append(symbol)

            if operator_expected == True:
                operator_expected = False

                transition.append(stack.pop())
                
                while(stack[-1] != '('):
                    transition.append(stack.pop())

                transition.append(stack.pop())
                transition.reverse()

                self.transitions.append(transition)
                
                transition = []

                stack.append(f'transition[{quantity}]')

                quantity += 1

            if symbol == ')':
                operator_expected = True
                
    def createStates(self):
        pass

    def processTransiton(self):
        pass

    def print_transitions(self):
        for transition in self.transitions:
            print(transition)