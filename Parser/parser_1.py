#from anytree import Node, RenderTree, PreOrderIter
#from anytree.search import findall_by_attr
from treelib import Node, Tree

grammara = {
    '<expression>': [('<term>',), ('<expression>', '+', '<term>')],
    '<term>': [('<factor>',), ('<term>', '*', '<factor>')],
    '<factor>': [ ('(', '<expression>', ')'), ('<number>',)],
    '<number>': [('0',), ('1',), ('2',), ('3',), ('4',), ('5',), ('6',), ('7',), ('8',), ('9',)]
}



class Stacka:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")

    def size(self):
        return len(self.items)

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

grammar3 ={
    'program': [('stmt-sequence',)],
    'stmt-sequence': [('statement', 'stmt-sequences'),('statement',)],
    'stmt-sequences': [(';', 'statement')],
    'statement': [('if-stmt',),('repeat-stmt',),('assign-stmt',),('read-stmt',),('write-stmt',)],
    'if-stmt': [('if', 'exp','then','stmt-sequence','end'),('if', 'exp','then','stmt-sequence','else','stmt-sequence','end')],
    'repeat-stmt': [('repeat','stmt-sequence','until','exp'),],
    'assign-stmt': [('identifier', ':=', 'exp'),],
    'read-stmt': [('read', 'identifier'),],
    'write-stmt': [('write', 'exp'),],
    'exp': [('simple-exp', 'comp-op','simple-exp'),('simple-exp',)],
    'comp-op': [('<',),('=',)],
    'simple-exp': [('term', "simple-exp'"),('term',)],
    "simple-exp'": [('addop', 'simple-exp'),],
    'addop': [('+'),('-')],
    'term': [('factor', "term'"),('factor',)],
    "term'": [('mulop', 'term'),],
    'mulop': [('*',),('/',)],
    'factor': [('(', 'exp',')'),('number',),('identifier',)]
}
grammar4 ={
    'program': [('stmt-sequence',)],
    'stmt-sequence': [('statement', 'stmt-sequences')],
    'stmt-sequences': [(';', 'statement'),('ε',)],
    'statement': [('if-stmt',),('repeat-stmt',),('assign-stmt',),('read-stmt',),('write-stmt',)],
    'if-stmt': [('if', 'exp','then','stmt-sequence','else-s','end')],
    'else-s': [('else', 'stmt-sequence','end'),('ε',)],
    'repeat-stmt': [('repeat','stmt-sequence','until','exp'),],
    'assign-stmt': [('identifier', ':=', 'exp'),],
    'read-stmt': [('read', 'identifier'),],
    'write-stmt': [('write', 'exp'),],
    'exp': [('simple-exp', "exp'")],
    "exp'":[('comp-op', 'simple-exp'),('ε',)],
    'comp-op': [('<',),('=',)],
    'simple-exp': [('term', "simple-exp'")],
    "simple-exp'": [('addop', 'simple-exp'),('ε',)],
    'addop': [('+'),('-')],
    'term': [('factor', "term'")],
    "term'": [('mulop', 'factor','term'),('ε',)],
    'mulop': [('*',),('/',)],
    'factor': [('(', 'exp',')'),('number',),('identifier',)]
}

#print(grammar)
#print(grammar3)
new_grammar = remove_left_recursion(grammar)
new_grammar2 = remove_left_recursion(grammar2)
new_grammar3 = remove_left_recursion(grammar4)

print_grammar(new_grammar3)


def calcula_first(nterminal,first_sets,gramatica):
        if nterminal in first_sets:
            return first_sets[nterminal]
        
        first = set()
        for regras in gramatica[nterminal]:
            #print(regras)
            if regras[0] == 'ε':
                first.add('ε')
            elif regras[0] not in gramatica:
                #print("Estou fazendo o first do não-terminal "+nterminal+" e a regra "+regras[0]+" está na gramática como um não-terminal")
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
    

    for nt in gramatica:
        first = calcula_first(nt,first_sets,gramatica)
        first_sets[nt] = first
    
    return first_sets
    
def calcula_follow(nterminal_out,nterminal_in,regra,first_sets,follow_sets,gramatica):
    def derives_epsilon(simbolo):
        return 'ε' in first_sets[simbolo]
    
    for i in range (len(regra)):
        simbolo = regra[i]
        
        #se simbolo for não-terminal
        if simbolo == nterminal_out:
            #print(simbolo)
            for j in range(i + 1, len(regra)):
                prox_simbolo = regra[j]
                #print(nterminal_out)
                #print(prox_simbolo)
                #print(first_sets)
                #print(follow_sets[nterminal_out])            
                #print("NT:"+nt+"->"+"SA:"+simbolo+" SP:"+prox_simbolo)
                            
                # Se o próximo símbolo for um terminal, adicione ao conjunto FOLLOW do não-terminal
                if prox_simbolo not in gramatica:
                    follow_sets[simbolo].add(prox_simbolo)
                    break 
                            
                # Se o próximo símbolo for um não-terminal
                elif prox_simbolo in gramatica:
                    # Adicione o conjunto FIRST do próximo símbolo ao conjunto FOLLOW do não-terminal, excluindo ε, se estiver presente
                    follow_sets[simbolo] |= first_sets[prox_simbolo] - {'ε'}

                    # Se o próximo símbolo puder derivar ε, adicione o conjunto FOLLOW do símbolo à esquerda da produção ao conjunto FOLLOW do não-terminal
                    if derives_epsilon(prox_simbolo) :
                        if j==len(regra):
                            follow_sets[simbolo] |= follow_sets[nterminal_in]

                    # Se o FIRST do próximo símbolo não contiver ε, não é necessário continuar com os próximos símbolos
                    else:
                        break
            else:
                # Se o loop terminar sem quebra, adicione o conjunto FOLLOW do símbolo à esquerda da produção ao conjunto FOLLOW do não-terminal
                follow_sets[simbolo] |= follow_sets[nterminal_in]
        
    return follow_sets[nterminal_out]

def follow(gramatica,first_sets,start_symbol):
    follow_sets = {nterminal: set() for nterminal in gramatica}
    follow_sets[start_symbol].add('$')
    for nt_out in gramatica:
        for nt_in, regras in gramatica.items():
            for regra in regras:
                if nt_out in regra:
                    follow = calcula_follow(nt_out,nt_in,regra,first_sets , follow_sets,gramatica)
                    follow_sets[nt_out] = follow
    
    return follow_sets


def extract_terminals(grammar):
    terminals = set()

    # Iterate through each production rule
    for production_rules in grammar.values():
        for rule in production_rules:
            # Iterate through each symbol in the rule
            for symbol in rule:
                # Check if the symbol is a terminal
                
                if symbol not in grammar and symbol != 'ε':
                    terminals.add(symbol)

    return terminals

print(extract_terminals(new_grammar))
def constroi_tabela(gramatica,first_sets,follow_sets):
    tabela = {}

    # Extract terminals from the grammar
    terminais = extract_terminals(gramatica)
    terminais.add('$')
    print("terminais:")
    print(terminais)
    # Create an empty matrix
    for non_terminal in gramatica:
        tabela[non_terminal] = {terminal: [] for terminal in terminais}

    # Fill the matrix with productions
    for non_terminal, production_rules in gramatica.items():
        
        for rule in production_rules:
            result = ' '.join(str(value) for value in rule)
            print("Non-T = ", non_terminal)
            print("Regra = ",rule)
            print(rule[0])
            if rule[0] != 'ε':
                if rule[0] in gramatica:
                    #print("STMT tá dentro")
                    #print("dentro tbm")
                    for t in first_sets[rule[0]]:
                        #print(t)
                        #print(rule)
                        if t != 'ε':
                            #print("nt:"+non_terminal+" terminal:"+t+" result:" +result)
                            tabela[non_terminal][t].append(result)
                        else:
                            for ta in follow_sets[non_terminal]:
                                tabela[non_terminal][ta].append(t)
                        
                else:
                    for t in first_sets[non_terminal]:
                        if t == rule[0]:
                            tabela[non_terminal][t].append(result)
            else:

                #print("dentro do else:"+non_terminal)
                for t in follow_sets[non_terminal]:
                    tabela[non_terminal][t].append(result)
        #print(non_terminal)
        #print(tabela[non_terminal])
        #print(tabela[non_terminal])
    return tabela
    

def printa_tabela(matrix):
    # Get all non-terminals and terminals
    non_terminals = sorted(matrix.keys())
    terminals = sorted(set(term for prod in matrix.values() for term in prod.keys()))

    # Print column headers
    header = " " * 10
    for terminal in terminals:
        header += f"{terminal:^10}"
    print(header)

    # Print rows
    for non_terminal in non_terminals:
        row = f"{non_terminal:<10}"
        for terminal in terminals:
            productions = matrix[non_terminal][terminal]
            if productions:
                row += f"{str(productions):^10}"
            else:
                row += f"{'':^10}"  # Empty cell if no production
        print(row)

def printa(tabela):
    for nts in tabela:
        #print("TESTE: "+str(tabela[nts]))
        #print(tabela[nts])
        print(""+nts+":")
        for terminals in tabela[nts]:
            #print(terminals+":")
            if tabela[nts][terminals]!=[]:

                print("\t",end="")
                print(terminals+' : ',end="")
                #for t in terminals:
                #if tabela[nts][terminals]!=[]:
                print("\t",end="")
                        #print(tabela[nts])
                print("\t",end="")
                print(tabela[nts][terminals])
                #print (str(tabela[nts]))
        print()


#def pilhar(entrada,tabela,gramatica,start_symbol):
class Noda:
    def __init__(self, value, parent=None,num=0):
        self.value = value
        self.children = []
        self.parent = parent
        self.numchilds = num
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        self.numchilds+=1
def print_tree(node, depth=0):
    print("  " * depth + f"{node.value} (Children: {node.numchilds})")  # Print the node
    for child in node.children:
        print_tree(child, depth + 1)  # Recursively print children

def pilhagem(pilha,terminais,entrada, tabela,gramatica,start_symbol):
    
    
    entrada.append('$')
    sim=0
    w=entrada[sim]
    pilha.push('$')
    pilha.push(start_symbol)
    #tree= Tree()
    tree = Noda(start_symbol)  # Root of the tree
    current_node = tree  # Current node in the tree
    atual=pilha.peek()
    print("Atual = ",atual)
    print("Posição na entrada = ",w)
    
    #tree.create_node(atual, atual)
    pastatual=""
    while atual !="$":
        if w not in terminais and w!="$":
            
            print("Erro pois token não faz parte da linguagem")
            break
        elif atual == w:
            print("Matched "+w)
            print(current_node.parent.value)
            while current_node.numchilds <=1:
                if current_node.parent is None:
                            break
                current_node= current_node.parent
            print(current_node.value)
            pilha.pop()
            sim+=1
            w=entrada[sim]
            print("w = ",w)
            
        elif atual in terminais:
            print("Erro pois terminal")
            break
        elif tabela[atual][w]==[]:
            print("Erro pois derivação M[",atual,"][",w,"] não é possível")
            break
        elif tabela[atual][w]!=[]:
            print(atual,"->",tabela[atual][w])
            pilha.pop()
            print("0=",tabela[atual][w][0])
            sep=tabela[atual][w][0].split()
            for thing in reversed(sep):
                #node=Node(thing,parent=tree)
                #print(thing+atual)
                #tree.create_node(thing, atual+thing, parent=pastatual+atual)
                if thing != "ε":
                    pilha.push(thing)
                    child_node = Noda(thing)
                    print("Criança=",child_node.value)
                    current_node.add_child(child_node)
                else:
                    print("adcionando ",thing," em ",current_node.value)
                    child_node = Noda(thing)
                    current_node.add_child(child_node)
                    for child in current_node.parent.children:
                        print(child.value)
                    while all(child.numchilds != 0 or (child.value in terminais or child.value == 'ε') for child in current_node.parent.children) and pilha.peek()!='$':
                        print("PILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL ",pilha.peek())
                        if current_node.value=="E'":
                            for child in current_node.children:
                                print("HEY = ",child.numchilds)
                        print(current_node.parent.value)
                        current_node= current_node.parent
                        for child in current_node.children:
                            print("CRE = ",child.value)
                        if current_node.parent is None:
                            print("breajubg E")
                            break
                    print("adcionando ",thing," em ",current_node.value)
                    current_node= current_node.parent
        pastatual= atual
        atual=pilha.peek()
        if (current_node.children):
            for child in current_node.children:
                print("Estou procurando em ", current_node.value)
                if child.value==atual :
                    print("NÒ atual = ", current_node.value)
                    current_node = child
                    print("Novo NÒ atual = ", current_node.value)
        else:
            print("NAO")
        
        print("Atual = ",atual)
        if atual =="$":
            print("Parsing Completed")
        #print("Topo da pilha ="+atual)
        print()
        #print("Root = ",tree.value," Children = ",tree.children.value)
        #print_tree(tree)
        #print(tree.show(stdout=False))
    print_tree(tree)



first_setsE = first(new_grammar)
first_setsS = first(new_grammar2)
first_setsprogram = first(new_grammar3)
print("FIRST sets:")

for non_terminal, first_set in first_setsprogram.items():
    print(f"FIRST({non_terminal}): {first_set}")


follow_setsE = follow(new_grammar,first_setsE,"E")
follow_setsS = follow(new_grammar2,first_setsS,"S")
follow_setsprogram = follow(new_grammar3,first_setsprogram,"program")



#pars=construct_LL1_parsing_table(new_grammar,first_sets,follow_sets)

#print("FIRST sets:")
#for non_terminal, first_set in first_sets.items():
    #print(f"FIRST({non_terminal}): {first_set}")
print("Conjuntos FOLLOW:")
for non_terminal, follow_set in follow_setsprogram.items():
    print(f"FOLLOW({non_terminal}): {follow_set}")
tabelao= constroi_tabela(new_grammar,first_setsE,follow_setsE)
tabelaoS=constroi_tabela(new_grammar2,first_setsS,follow_setsS)
tabelaoprogram=constroi_tabela(new_grammar3,first_setsprogram,follow_setsprogram)
#print(tabelaoprogram)
print()
printa(tabelaoprogram)
pil = Stacka()
terms=extract_terminals(new_grammar)
termsS=extract_terminals(new_grammar2)
termsprogram=extract_terminals(new_grammar3)
pilhagem(pil,terms,["id","+","id","*","id"],tabelao,new_grammar,'E')
#pilhagem(["a","c","g","h"],tabelaoS,new_grammar2,'S')
#pilhagem(pil,termsprogram,["identifier",":=","identifier","+","identifier"],tabelaoprogram,new_grammar3,'program')
#arv=Node("A")
#b=Node('a',arv)
#b=Node('c',b)
#b=Node('c',b)

#for pre,fill , node in RenderTree(arv):
    #print("%s%s" % (pre, node.name))


#print(tree.show(stdout=False))
#printa(tabelaoprogram)

# -> ['(', ['(', [['n']], '+', [['n']], ')'], '+', [['n']], ')']