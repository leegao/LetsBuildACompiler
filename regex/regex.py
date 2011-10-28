from nfa import nfa
from dfa import dfa

class regex(object):
    def __init__(self, regex):
        self.regex = regex
        fs = nfa(regex)
        trans, start, final = fs.nfa()
        d = dfa(trans, start, final)
        self.dfa, self.final = d.dfa(fs.input)
    
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
    
    def partial(self, s):
        def follow(dfa, state, s, c):
            if not s:
                if state not in self.final:
                    return 0
                return c
            
            if state in self.final:
                return c
            s = list(s)
            a = s.pop(0)
            next_state = dfa[(state, a)]
            if not next_state:
                return 0
            return follow(dfa, next_state, s, c+1)
        return follow(self.dfa, 1, s, 0)
    
    def greedy(self, s):
        def follow(dfa, state, s, c):
            if state == 0:
                return 0
            
            if not s:
                if state in self.final:
                    return c
                return 0
            
            final = False
            if state in self.final:
                final = True
            
            s = list(s)
            a = s.pop(0)
            
            if (state, a) not in dfa:
                return c
            
            next_state = dfa[(state, a)]
            
            after = follow(dfa, next_state, s, c+1)
            if final and not after:
                return c
            else:
                return after
        return follow(self.dfa, 1, s, 0)
if __name__ == "__main__":
    re = regex("ab*c(d|ef)*")
    def test(s):
        i = re.greedy(s)
        return s[:i], i
    def testp(s):
        i = re.partial(s)
        return s[:i], i
    print testp("acdaefef")
    print test("abcdef")
