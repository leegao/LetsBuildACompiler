class dfa(object):
    """
    See http://en.wikipedia.org/wiki/Powerset_construction 
    Definition for an epsilon-closure
    let edge(s, epsilon) be the set of all states reachable by s with an epsilon transition, then
    For a set of states S(nfa_table), closure(S) = S U (union(for s in closure(S), edge(s, epsilon)))
    """
    pass