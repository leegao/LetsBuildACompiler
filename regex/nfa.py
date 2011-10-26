# A regular expression consists of the alpha-numeric alphabet along
# with a set of operators:
# . (concat \x08)
# | (union)
# * (kleene closure/0 or more repetition)
# union can be right associative, so we look ahead until we encounter | or ) to break

operators = {"|":"union", "*":"star", "\x08":"concat", "(":"nothing", ")":"nothing"}

def alpha(c):
    return not (c in operators)

class nfa(object):
    def __init__(self, regex):
        self.operand_stack = []
        self.operator_stack = []
        self.regex = list(regex)
        self.preprocess()
        self.nfa_table = None
        self.input = []
        self.states = 0
        self.trans = {}
        self.accept = 0

    def state(self):
        s = self.states
        self.states += 1
        return s

    def transition(self, a, symbol, b):
        if (a,symbol) not in self.trans:
            self.trans[(a,symbol)] = []
        self.trans[(a,symbol)].append(b)
        
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
        s0, s1 = self.state(), self.state()
        self.transition(s0, symbol, s1)
        
        self.operand_stack.append([s0, s1])
        
        if symbol not in self.input:
            self.input.append(symbol)
        #print symbol
    
    def pop(self):
        """
        Pops from the operand stack
        """
        return self.operand_stack.pop()
    
    def apply(self, op):
        """
        Takes in the map and applies the intended operation on the current operand stack
        """
        #print(operators[op])
        operation = getattr(self, operators[op])
        operation()
        
    def concat(self):
        """
        b(top) = [3] - [...] -> [4]
        a = [1'] - [...] -> [2']
        
        a concat b ->
        [1'] -> [2'] -(epsilon)-> [3] -> [4]
        """
        b, a = self.pop(), self.pop()
        self.transition(a[-1], '\x00',b[0]) # epsilon transition
        for x in b:
            a.append(x)
        self.operand_stack.append(a)
    
    def star(self):
        """
        if a = [1] -...-> [2]
        then
        
        a star ->
                     +----(e)---+
                     v          ^
        [0'] -(e)-> [1] -...-> [2] -(e)-> [3']
         v                                 ^
         +---------------(e)---------------|
        """
        a = self.pop()
        start, end = self.state(), self.state()
        
        # directly to the end state
        self.transition(start, '\x00', end)
        
        # start to the first state in a
        self.transition(start, '\x00', a[0])
        
        # end of a to end
        self.transition(a[-1], '\x00', end)
        
        # end of a to start of a
        self.transition(a[-1], '\x00', a[0])
        
        a.insert(0, start)
        a.append(end)
        
        self.operand_stack.append(a)
    
    def union(self):
        """
        b(top) = [3] - [...] -> [4]
        a = [1] - [...] -> [2]
        
        then
        a|b ->
             +--(e)--> [1]->[2] --(e)-+
        [0'] +                        + --> [5']
             +--(e)--> [3]->[4] --(e)-+
        """
        b, a = self.pop(), self.pop()
        
        start, end = self.state(), self.state()
        
        self.transition(start, '\x00', a[0])
        self.transition(start, '\x00', b[0])
        self.transition(a[-1], '\x00', end)
        self.transition(b[-1], '\x00', end)
        
        # push(start a b end)
        self.operand_stack.append([start]+a+b+[end])
        
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
        Transforms a regular expression into an RPN representation and apply the
        transformations from each operation on the operand stack
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
                    self.apply(prev)
                    prev = self.operator_stack.pop()
            else:
                # any operator: evaluate the entire stack
                while self.operator_stack and nfa.prec(c, self.operator_stack[-1]):
                    prev = self.operator_stack.pop()
                    self.apply(prev)
                self.operator_stack.append(c)
        # loop through the rest of the operator stack and evaluate them
        while self.operator_stack:
            self.apply(self.operator_stack.pop())
        
        nfa_table = self.pop()
        self.accept = nfa_table[-1]
        
        return self.trans, self.accept, nfa_table[0]
        
if __name__ == "__main__":
    fa = nfa("ab*c")
