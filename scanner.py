import re
import nda
import csv

class token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return "{"+self.type+", "+self.value+"}"
    

def read_regex_file(filename):
    with open(filename, 'r') as regex_file:
        reader = csv.reader(regex_file, delimiter=';', quoting=csv.QUOTE_NONE)
        for linha in reader:
            print(linha)

# Função para gerar o scanner
class Scanner:
    def __init__(self, rules):
        self.rules = rules

    def run_scanner(self, text):
        words = text.split()
        for word in words:
            for type, dfa in rules.items():
                if dfa.read_word(word):
                    yield token(word, type)

        #token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.rules)
        #for mo in re.finditer(token_regex, text):
        #    token_type = mo.lastgroup
        #    value = mo.group(token_type)
        #    if token_type != 'NEWLINE':
        #        yield token(value, token_type)
