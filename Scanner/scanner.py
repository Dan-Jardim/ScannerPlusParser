import re
import Scanner.dfa as dfa
import csv

class token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return "{"+self.type+", "+self.value+"}"
    

def read_regex_file(filename):
    rules = dict()
    with open(filename, 'r', encoding="utf8") as regex_file:
        reader = csv.reader(regex_file, delimiter=':', quoting=csv.QUOTE_NONE)
        #reader = regex_file.read()
        for linha in reader:
            rules[linha[0]] = dfa.createAutomata(linha[1])

    return rules

# Função para gerar o scanner
class Scanner:
    def __init__(self, er_file):
        self.rules = read_regex_file(er_file)

    def readCode(self, code):
        word_list = []

        symbol = ""
        insideString = False
        for char in code:
            
            if char == '"':
                symbol += char
                insideString = not insideString
                
                if not insideString:
                    word_list.append(symbol)
                    symbol = ""
        
            elif char == "\n":
                word_list.append(symbol)
                word_list.append(char)
                symbol = ""

            elif char != " " or insideString:
                symbol+=char

            else:
                word_list.append(symbol)
                symbol = ""

        if symbol != " ":
            word_list.append(symbol)
        
        return word_list

    def run_scanner(self, text):

        token_list = []

        #words = text.split(" ")
        words = self.readCode(text)
        
        for word in words:
            for type, dfa in self.rules.items():
                if dfa.read_word(word):
                    token_list.append(token(word, type))
                    break
        
        return token_list