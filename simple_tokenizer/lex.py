# a simple lexer that tokenizes based on whitespace
from regex import regex

lowercase = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"
uppercase = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"
symbols = "+|-|=|.|,|/|%|^|<|>"

alphabet = lowercase

rule = regex("(%s)(%s)*"%(alphabet, alphabet))
white_space = regex("  *")

def lex(s):
    s = s[white_space.greedy(s):]
    if not s:
        return []
    word_c = rule.greedy(s)
    return [s[:word_c]]+lex(s[word_c:])
    
print lex("abc def ghijk")