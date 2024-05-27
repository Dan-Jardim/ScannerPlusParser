

class Pilha:
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
        print(non_terminal + " -> ", end="")
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

BASICgrammar = {
    'Lines' : [('Integer', 'Statements', 'NewLine', "Lines'")],
    "Lines'" : [('Lines',),('ε',)],
    'Statements' : [('Statement', "Statements'")],
    "Statements'" : [(':','Statements'),('ε',)],

    'Statement' : [('CLOSE', '#', 'Integer'), ('DATA', 'Constant-List'), ('DIM', 'ID', '(', 'Integer-List', ')'),
                  ('END',), ('FOR', 'ID', '=', 'Expression', 'TO', 'Expression',"Statement'"),
                  ('GOTO', 'Expression'), ('GOSUB', 'Expression'), ('IF', 'Expression', 'THEN', 'Statement'), ('INPUT', "Statement'", 'ID-List'),
                  ('LET', 'ID', '=', 'Expression'), ('NEXT', 'ID-List'),
                  ('OPEN', 'Value', 'FOR', 'Access', 'AS', '#','Integer'), ('POKE', 'Value-List'), ('PRINT', "Statement'", 'Print-List'),
                  ('READ', 'ID-List'), ('RETURN',), ('RESTORE',), ('RUN',), ('STOP',),
                  ('SYS', 'Value'), ('WAIT', 'Value-List'), ('Remark',)],
    "Statement'" : [('STEP','Integer'),('#','Integer',','),('ε',)],
    'Access' : [('INPUT',), ('OUTPUT',)],
    'ID-List' : [('ID', "ID-List'")],
    "ID-List'" : [(',', 'ID-List'), ('ε',)],
    'Value-List' : [('Value', "Value-List'")],
    "Value-List'" : [(',', 'Value-List'), ('ε',)],
    'Constant-List' : [('Constant', "Constant-List'")],
    "Constant-List'" : [(',', 'Constant-List'), ('ε',)],
    'Integer-List' : [('Integer', "Integer-List'")],
    "Integer-List'" : [(',', 'Integer-List'), ('ε',)],
    'Expression-List' : [('Expression', "Expression-List'")],
    "Expression-List'" : [(',', 'Expression-List'), ('ε',)],
    'Print-List' : [('Expression', "Print-List'"), ('ε',)],
    "Print-List'" : [(';', 'Print-List'), ('ε',)],
    'Expression' : [('And-Exp', "Expression'")],
    "Expression'" : [('OR', 'Expression'), ('ε',)],
    'And-Exp' : [('Not-Exp', "And-Exp'")],
    "And-Exp'" : [('AND', 'And-Exp'), ('ε',)],
    'Not-Exp' : [('NOT', 'Compare-Exp'), ('Compare-Exp',)],
    'Compare-Exp' : [('Add-Exp', "Compare-Exp'")],
    "Compare-Exp'" :[('=', "Add-Exp"), ('<>', "Add-Exp"), ('><', "Add-Exp"), ('>', "Add-Exp"), ('>=', "Add-Exp"), ('<', "Add-Exp"), ('<=', "Add-Exp"),('ε',)],
    'Add-Exp': [('Mult-Exp', "Add-Exp'")],
    "Add-Exp'" : [('+', 'Add-Exp'), ('-', 'Add-Exp'), ('ε',)],
    'Mult-Exp': [('Negate-Exp', "Mult-Exp'")],
    "Mult-Exp'" : [('*', 'Mult-Exp'), ('/', 'Mult-Exp'), ('ε',)],
    'Negate-Exp': [('-', 'Power-Exp'), ('Power-Exp',)],
    'Power-Exp': [('Value',"Power-Exp'")],
    "Power-Exp'" :[('^', 'Value',"Power-Exp'"),('ε',)],
    'Value': [('(', 'Expression', ')'), ('ID', "Value'"), ('Constant',)],
    "Value'" : [( '(', 'Expression-List', ')'), ('ε',)],
    'Constant': [('Integer',), ('String',), ('Real',)]
}

basic_grammar = BASICgrammar



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
    

    for nt in gramatica:
        first = calcula_first(nt,first_sets,gramatica)
        first_sets[nt] = first
    
    return first_sets


def print_firsts(first_sets):
    print("FIRST sets:")
    for non_terminal, first_set in first_sets.items():
        print(f"FIRST({non_terminal}): {first_set}")


def calcula_follow(nterminal_out,nterminal_in,regra,first_sets,follow_sets,gramatica):
    def derives_epsilon(simbolo):
        return 'ε' in first_sets[simbolo]
    
    for i in range (len(regra)):
        simbolo = regra[i]
        
        if simbolo == nterminal_out:
            for j in range(i + 1, len(regra)):
                prox_simbolo = regra[j]
                            
                if prox_simbolo not in gramatica:
                    follow_sets[simbolo].add(prox_simbolo)
                    break 
                            
                elif prox_simbolo in gramatica:
                    follow_sets[simbolo] |= first_sets[prox_simbolo] - {'ε'}

                    if derives_epsilon(prox_simbolo) :
                        if j==len(regra):
                            follow_sets[simbolo] |= follow_sets[nterminal_in]

                    else:
                        break
            else:
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


def print_follows(follow_sets):
    print("Conjuntos FOLLOW:")
    for non_terminal, follow_set in follow_sets.items():
        print(f"FOLLOW({non_terminal}): {follow_set}")
def extract_terminals(grammar):
    terminals = set()

    for production_rules in grammar.values():
        for rule in production_rules:
            for symbol in rule:
                
                if symbol not in grammar and symbol != 'ε':
                    terminals.add(symbol)

    return terminals

def constroi_tabela(gramatica,first_sets,follow_sets):
    tabela = {}

    terminais = extract_terminals(gramatica)
    terminais.add('$')
    for non_terminal in gramatica:
        tabela[non_terminal] = {terminal: [] for terminal in terminais}

    for non_terminal, production_rules in gramatica.items():
        
        for rule in production_rules:
            result = ' '.join(str(value) for value in rule)
            if rule[0] != 'ε':
                if rule[0] in gramatica:
                    for t in first_sets[rule[0]]:
                        if t != 'ε':
                            tabela[non_terminal][t].append(result)
                        else:
                            for ta in follow_sets[non_terminal]:
                                tabela[non_terminal][ta].append(t)
                        
                else:
                    for t in first_sets[non_terminal]:
                        if t == rule[0]:
                            tabela[non_terminal][t].append(result)
            else:

                for t in follow_sets[non_terminal]:
                    tabela[non_terminal][t].append(result)
    return tabela
    


def printa(tabela):
    for nts in tabela:
        print(""+nts+":")
        for terminals in tabela[nts]:
            if tabela[nts][terminals]!=[]:

                print("\t",end="")
                print(terminals+' : ',end="")
                print("\t",end="")
                print("\t",end="")
                print(tabela[nts][terminals])
        print()


class ArvoreSint:
    def __init__(self, value, parent=None,num=0):
        self.value = value
        self.children = []
        self.parent = parent
        self.numchilds = num
        self.closed = False
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        self.numchilds+=1

def print_tree(root, markerStr="+- ", levelMarkers=[]):
    emptyStr = " "*len(markerStr)
    connectionStr = "|" + emptyStr[:-1]
    level = len(levelMarkers)
    mapper = lambda draw: connectionStr if draw else emptyStr
    markers = "".join(map(mapper, levelMarkers[:-1]))
    markers += markerStr if level > 0 else ""
    if root.value !="ε" and root.children==[]:
        print(f"{markers}\033[31m{root.value}\033[0m")
    else:
        print(f"{markers}{root.value}")
    for i, child in enumerate(root.children):
        isLast = i == len(root.children) - 1
        print_tree(child, markerStr, [*levelMarkers, not isLast])
def analiseSint(pilha,terminais,entrada, tabela,gramatica,start_symbol):
    
    
    entrada.append('$')
    sim=0
    w=entrada[sim]
    pilha.push('$')
    pilha.push(start_symbol)
    tree = ArvoreSint(start_symbol)  
    current_node = tree 
    atual=pilha.peek()
    erros = []
    while atual !="$":
        if w not in terminais and w!="$":
            erro = "Erro pois token não faz parte da linguagem"
            erros.append(erro)
            pilha.pop()
            sim+=1
            if sim <len(entrada):
                w=entrada[sim]
        elif atual == w:
            print("\033[34mMatched "+w+"\033[0m")
            current_node.closed=True
            
            while current_node.numchilds <=1 or all(child.closed   for child in current_node.children):
                if current_node.parent is None:
                            break
                if all(child.closed   for child in current_node.children):
                    current_node.closed = True
                current_node= current_node.parent
            
            pilha.pop()
            
            sim+=1
            if sim <len(entrada):
                w=entrada[sim]
            
        elif atual in terminais:
            erro = f"Erro pois {atual} é um terminal"
            erros.append(erro)
            pilha.pop()
            sim+=1
            if sim <len(entrada):
                w=entrada[sim]
        elif tabela[atual][w]==[]:

            erro = f"Erro pois derivação M[ {atual} ][ {w} ] não é possível"
            erros.append(erro)
            pilha.pop()
            sim+=1
            if sim <len(entrada):
                w=entrada[sim]
        elif tabela[atual][w]!=[]:
            print(atual,"->",tabela[atual][w])
            pilha.pop()
            sep=tabela[atual][w][0].split()
            for thing in reversed(sep):
                if thing != "ε":
                    pilha.push(thing)
                    child_node = ArvoreSint(thing)
                    current_node.add_child(child_node)
                else:
                    child_node = ArvoreSint(thing)
                    current_node.add_child(child_node)
                    while all(child.numchilds != 0 or (child.value in terminais or child.value == 'ε') for child in current_node.parent.children) and pilha.peek()!='$':
                        if all(child.closed   for child in current_node.children):
                            current_node.closed = True
                        current_node= current_node.parent
                        if current_node.parent is None:
                            break
                    if all(child.closed   for child in current_node.children):
                        current_node.closed = True
                    current_node= current_node.parent
        atual=pilha.peek()
        if (current_node.children):
            for child in current_node.children:

                if child.value==atual :
                    current_node = child
        if atual =="$":
            if erros ==[]:
                print("Parsing Completed")
                
                print("Árvore Sintática: ")
                print_tree(tree)
            else:
                for error in erros:
                    print(error)

def parser(entrada):

    first_setsBasic = first(basic_grammar)


    #print_firsts(first_setsBasic)


    follow_setsBasic = follow(basic_grammar, first_setsBasic, "Lines")

    #print_follows(follow_setsBasic)



    tabelaoBasic = constroi_tabela(basic_grammar, first_setsBasic, follow_setsBasic)

    #printa(tabelaoBasic)

    pil = Pilha()

    termsBasic=extract_terminals(basic_grammar)

    analiseSint(pil,termsBasic,entrada,tabelaoBasic,basic_grammar,'Lines')
    
fonte = ["Integer","PRINT","String","NewLine",
                            "Integer","PRINT","String","NewLine",
                            "Integer","INPUT","ID","NewLine",
                            "Integer","PRINT","String",";","ID",";","String","NewLine"]


exemplo1= ["Integer", "PRINT", "String", "NewLine", 
           "Integer", "END", "NewLine"]


exemplo2= ["Integer", "INPUT", "ID", "NewLine", 
           "Integer", "PRINT", "ID", "NewLine", 
           "Integer", "END", "NewLine"]


exemplo3= ["Integer", "IF", "ID", ">","Integer", "THEN", "PRINT", "String", "NewLine", 
           "Integer", "END", "NewLine"]

exemplo4= ["Integer", "POKE", "Integer", ",", "Integer", "NewLine", 
           "Integer", "WAIT", "Integer", ",","Integer", "NewLine", 
           "Integer", "END", "NewLine"]

exemplo5 = ["Integer","OPEN","String", "FOR", "OUTPUT","AS", "#", "Integer", "NewLine",
            "Integer","PRINT", "#", "Integer", ",", "String","NewLine",
            "Integer","CLOSE", "#", "Integer","NewLine",
            "Integer","END", "NewLine"]


exemplo6 = ["Integer","PRINT","String","NewLine",
            "Integer","GOTO","Integer","NewLine",
            "Integer","PRINT","String","NewLine",
            "Integer","GOTO","Integer","NewLine",
             "Integer","PRINT","String","NewLine",
            "Integer","PRINT","String","NewLine"]


exemplo7 = ["Integer","GOSUB","Integer","NewLine",
            "Integer","PRINT","String","NewLine",
            "Integer","END","NewLine",
            "Integer","PRINT","String","NewLine",
            "Integer","RETURN","NewLine"]


exemplo9 = ["Integer","LET","ID", "=", "Integer","NewLine",
            "Integer","LET","ID", "=", "Integer","NewLine",
            "Integer","LET","ID", "=", "Integer", "+", "Integer", "*", "(","Integer", "-", "Integer", ")", "/","Integer", "^", "Integer","NewLine",
            "Integer","PRINT","String","NewLine",
            "Integer", "END", "NewLine"]


exemplo10 = ["Integer","Remark","NewLine",
            "Integer","PRINT","String","NewLine",
            "Integer","END","NewLine"]

#parser(exemplo7)
#parser(exemplo4)
