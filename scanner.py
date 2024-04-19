import re

class token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return "{"+self.type+", "+self.value+"}"

# Função para gerar o scanner
class Scanner:
    def __init__(self, rules):
        self.rules = rules

    def run_scanner(self, text):
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.rules)
        for mo in re.finditer(token_regex, text):
            token_type = mo.lastgroup
            value = mo.group(token_type)
            if token_type != 'NEWLINE':
                yield token(value, token_type)
