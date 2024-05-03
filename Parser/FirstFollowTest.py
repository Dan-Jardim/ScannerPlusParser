grammara = {
    '<expression>': [('<term>',), ('<expression>', '+', '<term>')],
    '<term>': [('<factor>',), ('<term>', '*', '<factor>')],
    '<factor>': [ ('(', '<expression>', ')'), ('<number>',)],
    '<number>': [('0',), ('1',), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)]
}





def print_grammar(grammar):
    for non_terminal, rules in grammar.items():
        print(non_terminal + " ::= ", end="")
        for i, rule in enumerate(rules):
            print("  " + " ".join(rule), end="")
            if i < len(rules) - 1:
                print(" | ", end="")
            else:
                print()
        print()




def remove_left_recursion(grammar):
    new_grammar = {}
    for non_terminal, rules in grammar.items():
        new_rules = []
        recursive_rules = []
        # Separate recursive and non-recursive rules
        for rule in rules:
            if rule[0] == non_terminal:
                recursive_rules.append(rule[1:])
            else:
                new_rules.append(rule)
        if recursive_rules:
            new_non_terminal = non_terminal + "'"
            new_grammar[non_terminal] = [(rule + (new_non_terminal,))
                                         for rule in new_rules]
            new_grammar[new_non_terminal] = [(rule + (new_non_terminal,))
                                              for rule in recursive_rules]
            new_grammar[new_non_terminal].append(('ε',))
        else:
            new_grammar[non_terminal] = rules
    return new_grammar

# Example grammar
grammar = {
    'E': [('E', '+', 'T'), ('T',)],
    'T': [('T', '*', 'F'), ('F',)],
    'F': [('(', 'E', ')'), ('id',)]
}
grammar2 = {
    'S': [('a', 'B', 'D','h')],
    'B': [('c', 'C')],
    'C': [('b', 'C'), ('ε',)],
    'D': [('E', 'F')],
    'E': [('g'), ('ε',)],
    'F': [('f'), ('ε',)]
}





new_grammar = remove_left_recursion(grammar)
print_grammar(new_grammar)


def calcula_first(nterminal,first_sets,gramatica):
        if nterminal in first_sets:
            return first_sets[nterminal]
        
        first = set()
        for regras in gramatica[nterminal]:
            if regras[0] == 'ε':
                first.add('ε')
            elif regras[0] not in gramatica:
                first.add(regras[0])
            else:
                firstr = calcula_first(regras[0],first_sets,gramatica)
                first |= firstr
                if 'ε' in firstr:
                    i = 1
                    while i < len(regras):
                        firstp = calcula_first(regras[1],first_sets,gramatica)
                        first |= (firstp - {'ε'})
                        if 'ε' not in firstp:
                            break
                        i+=1
                    if i == len(regras):
                        first.add('ε')
        
        
        return first


def first(gramatica):
    first_sets = {}
    print(first_sets)
    

    for nt in gramatica:
        first = calcula_first(nt,first_sets,gramatica)
        first_sets[nt] = first
    return first_sets
    

def follow(gramatica, first_sets,start_symbol):
    follow_sets = {nterminal: set() for nterminal in gramatica}
    
    def derives_epsilon(simbolo):
        return 'ε' in first_sets[simbolo]

    while True:
        print(follow_sets)
        old_follow_sets = {nterminal: follow_sets[nterminal].copy() for nterminal in gramatica}
        for nt,regras in gramatica.items():
            for regra in regras:
                for i in range (len(regra)):
                    simbolo = regra[i]

                    #se simbolo for não-terminal
                    if simbolo in gramatica:

                        for j in range(i + 1, len(regra)):
                            prox_simbolo = regra[j]
                            
                            print(nt+":"+simbolo+prox_simbolo)
                            
                            # Se o próximo símbolo for um terminal, adicione ao conjunto FOLLOW do não-terminal
                            if prox_simbolo not in gramatica:
                                follow_sets[simbolo].add(prox_simbolo)
                                break 
                            
                            # Se o próximo símbolo for um não-terminal
                            elif prox_simbolo in gramatica:
                                # Adicione o conjunto FIRST do próximo símbolo ao conjunto FOLLOW do não-terminal, excluindo ε, se estiver presente
                                follow_sets[simbolo] |= first_sets[prox_simbolo] - {'ε'}

                                # Se o próximo símbolo puder derivar ε, adicione o conjunto FOLLOW do símbolo à esquerda da produção ao conjunto FOLLOW do não-terminal
                                if derives_epsilon(prox_simbolo):
                                    follow_sets[simbolo] |= follow_sets[nt]

                                # Se o FIRST do próximo símbolo não contiver ε, não é necessário continuar com os próximos símbolos
                                if 'ε' not in first_sets[prox_simbolo]:
                                    break
                        else:
                            # Se o loop terminar sem quebra, adicione o conjunto FOLLOW do símbolo à esquerda da produção ao conjunto FOLLOW do não-terminal
                            follow_sets[simbolo] |= follow_sets[nt]
            
        # Verifica se houve alguma alteração nos conjuntos FOLLOW
        if all(old_follow_sets[nterminal] == follow_sets[nterminal] for nterminal in gramatica):
            break
    follow_sets[start_symbol].add('$')
    return follow_sets

def calculate_follow(grammar, first_sets,start_symbol):
    # Inicialização dos conjuntos FOLLOW
    follow = {non_terminal: set() for non_terminal in grammar}

    # Função para verificar se um símbolo pode derivar ε
    def derives_epsilon(symbol):
        return 'ε' in first_sets[symbol]

    # Loop principal para iterar até que não haja mais alterações nos conjuntos FOLLOW
    while True:
        # Armazena os conjuntos FOLLOW antes de cada iteração
        old_follow = {non_terminal: follow[non_terminal].copy() for non_terminal in grammar}

        # Para cada produção na gramática
        for non_terminal, productions in grammar.items():
            for production in productions:
                rhs = production

                # Iteração sobre os símbolos na produção
                for i in range(len(rhs)):
                    symbol = rhs[i]

                    # Se o símbolo for um não-terminal
                    if symbol in grammar:
                        # Para cada símbolo após o não-terminal
                        for j in range(i + 1, len(rhs)):
                            next_symbol = rhs[j]

                            # Se o próximo símbolo for um terminal, adicione ao conjunto FOLLOW do não-terminal
                            if next_symbol not in grammar:
                                follow[symbol].add(next_symbol)
                                break

                            # Se o próximo símbolo for um não-terminal
                            elif next_symbol in grammar:
                                # Adicione o conjunto FIRST do próximo símbolo ao conjunto FOLLOW do não-terminal, excluindo ε, se estiver presente
                                follow[symbol] |= first_sets[next_symbol] - {'ε'}

                                # Se o próximo símbolo puder derivar ε, adicione o conjunto FOLLOW do símbolo à esquerda da produção ao conjunto FOLLOW do não-terminal
                                if derives_epsilon(next_symbol):
                                    follow[symbol] |= follow[non_terminal]

                                # Se o FIRST do próximo símbolo não contiver ε, não é necessário continuar com os próximos símbolos
                                if 'ε' not in first_sets[next_symbol]:
                                    break
                        else:
                            # Se o loop terminar sem quebra, adicione o conjunto FOLLOW do símbolo à esquerda da produção ao conjunto FOLLOW do não-terminal
                            follow[symbol] |= follow[non_terminal]
        follow[start_symbol].add('$')
        # Verifica se houve alguma alteração nos conjuntos FOLLOW
        if all(old_follow[non_terminal] == follow[non_terminal] for non_terminal in grammar):
            break

    return follow
def construct_LL1_parsing_table(grammar, first_sets, follow_sets):
    parsing_table = {}

    for non_terminal, productions in grammar.items():
        for production in productions:
            first_alpha = firsta(production, first_sets)

            for terminal in first_alpha:
                if terminal != 'ε':
                    if non_terminal not in parsing_table:
                        parsing_table[non_terminal] = {}
                    parsing_table[non_terminal][terminal] = production

            if 'ε' in first_alpha:
                follow_a = follow_sets[non_terminal]
                for terminal in follow_a:
                    if terminal == '$':
                        if non_terminal not in parsing_table:
                            parsing_table[non_terminal] = {}
                        parsing_table[non_terminal]['$'] = 'ε'
                    else:
                        if non_terminal not in parsing_table:
                            parsing_table[non_terminal] = {}
                        parsing_table[non_terminal][terminal] = 'ε'

    return parsing_table

def firsta(alpha, first_sets):
    first_alpha = set()
    for symbol in alpha:
        if symbol in first_sets:
            first_alpha |= first_sets[symbol]
            if 'ε' not in first_sets[symbol]:
                break
        else:
            first_alpha.add(symbol)
            break
    return first_alpha

def print_ll1_parsing_table(parsing_table):
    # Get sorted list of non-terminals and terminals
    non_terminals = sorted(parsing_table.keys())
    terminals = sorted(set(term for productions in parsing_table.values() for term in productions.keys() if term != 'ε'))

    # Print table header
    print('{:<5}'.format(''), end='')  # Empty space for formatting
    for terminal in terminals:
        print('{:<10}'.format(terminal), end='')
    print()

    # Print separator line
    print('-' * (5 + 10 * len(terminals)))

    # Print table body
    for non_terminal in non_terminals:
        print('{:<5}'.format(non_terminal), end='')
        for terminal in terminals:
            if terminal in parsing_table[non_terminal]:
                print('{:<10}'.format(''.join(parsing_table[non_terminal][terminal])), end='')  # Fix here
            else:
                print('{:<10}'.format(''), end='')
        print()



first_sets = first(new_grammar)
print("FIRST sets:")

for non_terminal, first_set in first_sets.items():
    print(f"FIRST({non_terminal}): {first_set}")


follow_sets = follow(new_grammar,first_sets,'E')

#pars=construct_LL1_parsing_table(new_grammar,first_sets,follow_sets)

#print("FIRST sets:")
#for non_terminal, first_set in first_sets.items():
    #print(f"FIRST({non_terminal}): {first_set}")
print("Conjuntos FOLLOW:")
for non_terminal, follow_set in follow_sets.items():
    print(f"FOLLOW({non_terminal}): {follow_set}")
#print_ll1_parsing_table(pars)

