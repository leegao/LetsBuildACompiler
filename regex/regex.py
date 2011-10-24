from nfa import nfa
from dfa import dfa

class regex(object):
    def __init__(self, regex):
        self.regex = regex
        fs = nfa(regex)
        self.dfa, self.final = dfa.dfa(fs.nfa()[0], fs.input)
    
    def match(self, s):
        def follow(dfa, state, s):
            if not s:
                return state
            s = list(s)
            a = s.pop(0)
            next_state = dfa[(state, a)]
            if not next_state:
                return 0
            return follow(dfa, next_state, s)
        state = follow(self.dfa, 1, s)
        return state in self.final
        
if __name__ == "__main__":
    re = regex("ab*c(d|ef)*")
    print re.match("acefef")