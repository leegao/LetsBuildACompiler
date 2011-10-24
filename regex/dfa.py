from memoize import memoize

class dfa(object):
    """
    See http://en.wikipedia.org/wiki/Powerset_construction 
    Definition for an epsilon-closure
    let edge(s, epsilon) be the set of all states reachable by s with an epsilon transition, then
    For a set of states S(nfa_table), closure(S) = S U (union(for s in closure(S), edge(s, epsilon)))
    """
    
    @classmethod
    @memoize
    def edge(cls, state, symb='\x00'):
        l = [trans[1] for trans in state.transitions if trans[0] == symb] 
        return l

    
    @classmethod
    @memoize
    def closure(cls, states):
        def _closure(state):
            edges = dfa.edge(state)
            last = 0
            while last != len(edges):
                last = len(edges)
                for s in edges:
                    edges += dfa.edge(s)
                edges = list(set(edges))
            return edges
        edges = list(states)
        for state in states:
            edges += _closure(state)
        return list(set(edges))
    
    @classmethod
    def combine(cls, d, symbol):
        states = []
        for state in d:
            states += dfa.edge(state, symbol)
        return dfa.closure(states)
    
    @classmethod
    def is_final(cls, states):
        for state in states:
            if state.accept:
                return True
        return False
    
    @classmethod
    def dfa(cls, s1, input):
        states = [[], dfa.closure([s1])]
        trans = {}
        final = []
        p = 1
        j = 0
        while j <= p:
            for c in input:
                e = dfa.combine(states[j], c)
                if e in states:
                    trans[(j,c)] = states.index(e)
                else:
                    p += 1
                    states.append(e)
                    if dfa.is_final(e):
                        final.append(p)
                    trans[(j,c)] = p
                    
            j+= 1
        return trans, final