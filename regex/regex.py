# A regular expression consists of the alpha-numeric alphabet along
# with a set of operators:
# . (concat \x08)
# | (union)
# * (kleene closure/0 or more repetition)
# union can be right associative, so we look ahead until we encounter | or ) to break

operators = {"|":"union", "*":"star", "\x08":"concat", "(":"nothing", ")":"nothing"}

class state(object):
    g_state = 0
    def __init__(self):
        self.state = state.g_state
        state.g_state += 1
        self.transitions = {}
        self.accept = False
    
    def __repr__(self):
        return str(self.transitions)
    
    def transition_to(self, symbol, next_state):
        self.transitions[symbol] = next_state

def alpha(c):
    return not (c in operators)

class regex(object):
    def __init__(self, regex):
        self.operand_stack = []
        self.operator_stack = []
        self.regex = list(regex)
        self.preprocess()
        self.nfa_table = None
        
    def preprocess(self):
        regex = []
        #second pass: add concat between
        # ab, a( , )a , *a , *( , )(
        for i,c in enumerate(self.regex):
            # get lookahead
            regex.append(c)
            if i+1 >= len(self.regex):
                continue
            n = self.regex[i+1]
            if   (alpha(c) and alpha(n)) \
              or (alpha(c) and n == "(") \
              or (c == ")" and alpha(n)) \
              or (c == "*" and alpha(n)) \
              or (c == "*" and n == "(") \
              or (c == ")" and n == "("):
                regex.append('\x08')
        
        self.regex = regex
    
    def push(self, symbol):
        """
        Pushing a symbol is equivalent to
        [s0] --(symbol)--> [s1]
        """
        s0, s1 = state(), state()
        s0.transition_to(symbol, s1)
        
        self.operand_stack.append([s0, s1])
        print symbol
    
    def pop(self):
        """
        Pops from the operand stack
        """
        return self.operand_stack.pop()
    
    def eval(self, op):
        print(operators[op])
        
    
    @classmethod
    def prec(cls, left, right):
        if left == right:
            return True
        elif left == "*":
            return False
        elif right == "*":
            return True
        elif left == "\x08":
            return False
        elif right == "\x08":
            return True
        elif left == "|":
            return False
        else:
            return True
    
    def nfa(self):
        """
        Takes in 
        """
        for c in self.regex:
            if alpha(c):
                self.push(c)
            elif len(self.operator_stack) == 0:
                # if the stack is empty and we encounter (, we will still push it in
                self.operator_stack.append(c)
            elif c == '(':
                self.operator_stack.append(c)
            elif c == ')':
                # evaluate everything until we encounter (
                prev = self.operator_stack.pop()
                while not (prev == "("):
                    self.eval(prev)
                    prev = self.operator_stack.pop()
            else:
                # any operator: evaluate the entire stack
                while self.operator_stack and regex.prec(c, self.operator_stack[-1]):
                    prev = self.operator_stack.pop()
                    self.eval(prev)
                self.operator_stack.append(c)
        # loop through the rest of the operator stack and evaluate them
        while self.operator_stack:
            self.eval(self.operator_stack.pop())
        
        self.nfa_table = self.pop()
        self.nfa_table[-1].accept = True
        
re = regex("abc*(d|ef)*")
re.nfa()