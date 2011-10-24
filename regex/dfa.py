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
    def edge(cls, state):
        return [trans[1] for trans in state.transitions if trans[0] == '\x00']
    
    @classmethod
    def closure(cls, state):
        edges = dfa.edge(state)
        last = 0
        while last != len(edges):
            last = len(edges)
            for s in edges:
                edges += dfa.edge(s)
            edges = list(set(edges))
        return edges
            
                
from regex import regex

re = regex("ab*c")
nfa = re.nfa()
print nfa
for s in nfa:
    print s, dfa.closure(s)