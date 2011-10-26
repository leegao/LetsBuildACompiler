from memoize import memoize

class dfa(object):
    """
    See http://en.wikipedia.org/wiki/Powerset_construction 
    Definition for an epsilon-closure
    let edge(s, epsilon) be the set of all states reachable by s with an epsilon transition, then
    For a set of states S(nfa_table), closure(S) = S U (union(for s in closure(S), edge(s, epsilon)))
    """

    def __init__(self, nfa, start, final):
        self.nfa = nfa
        self.start = start
        self.nfa_accept = final
    
    @memoize
    def edge(self, state, symb='\x00'):
        """
        The edge function looks through the list of possible transitions
        from an NFA state and returns a set of states that can be reached
        via symbol
        """
        l = []
        for trans in self.nfa:
            if trans[0] == state and trans[1] ==symb:
                l += self.nfa[trans]
        return l 

    @memoize
    def closure(self, states):
        """
        Closure calculates the epsilon closures of a set of states.
        More specifically, we know that the set of states that can
        be reached via epsilon transition (the epsilon closure) must
        be contained within either the epsilon closure of S1, S2, ...
        Sn where states is {S1, S2, ..., Sn}, or that the closure of the set
        of states is equivalent to the union of the closures of the individual
        states. Closure(S1) U Closure(S2) U ... U Closure(Sn)
        """
        def _closure(state):
            """
            A helper function that calculates the epsilon closure of
            a single state. Note that in the FA [0]-(e)->[1]-(e)->[2],
            edge([0], epsilon) will return only {[1]} whereas closure([0])
            is actually {[1], [2]}. Hence, we must rerun the edge algorithm
            on the successively larger closure until the length of the set
            between two iterations no longer changes.
            """
            edges = self.edge(state)
            last = 0
            while last != len(edges):
                last = len(edges)
                for s in edges:
                    edges += self.edge(s)
                edges = list(set(edges))
            return edges
        
        edges = list(states)
        for state in states:
            edges += _closure(state)
        return list(set(edges))
    
    def combine(self, d, symbol):
        """
        Returns every state reachable from the grouped DFA state d
        with a transition of symbol.
        Note that since a FA such as:
        [0]-(a)->[1]-(epsilon)->[2]
        will reach both states [1] and [2] by consuming 'a', we must
        also add the epsilon closure of state 1 into the 
        """
        states = []
        for state in d:
            states += self.edge(state, symbol)
        return self.closure(list(set(states)))
    
    def is_final(self, states):
        """
        If any state within states is final, then the DFA state
        is also final.
        """
        for state in states:
            if state == self.nfa_accept:
                return True
        return False
    
    def dfa(self, input):
        """
        Taken from Appel's section on converting an NFA into a DFA.

        The algorithm combines multiple NFA states into a single DFA
        state in order to eliminate epsilon transitions. Since 
        """
        # states[0] is always non-matching
        # states[1] is the initial 
        states = [[], self.closure([self.start])]
        trans = {} # a dictionary of transitions from one state into another
        final = [] # a list of accepting states
        p = 1
        j = 0
        while j <= p:
            # For each character of the alphabet
            for c in input:
                # We combine the output state into a single DFA state
                # being the union of the states.
                # this way, each character can only go to ONE state for each DFA state,
                # hence making this automaton by definition a DFA.
                e = self.combine(states[j], c)
                if e in states:
                    # if we've already seen it before, add it into the transition dict
                    trans[(j,c)] = states.index(e)
                else:
                    # we've encountered a new DFA state. Add it in and add into the transition
                    p += 1
                    states.append(e)
                    if self.is_final(e):
                        # if any of the nfa states are accepting, then so is this DFA state
                        final.append(p) 
                    trans[(j,c)] = p
                    
            j+= 1
        return trans, final # only the transition dict and the final accept states are useful

if __name__ == "__main__":
    from nfa import nfa
    n = nfa("ab*c")
    trans, start, accept = n.nfa()
    d = dfa(trans, start, accept)