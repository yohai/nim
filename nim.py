import numpy as np
from collections import defaultdict
import pdb

def sort(x):
    return tuple(sorted(x, reverse=True))

def children(x):
    return set().union(
        sort(x[:k] + (i,) + x[k+1:])  
        for k in range(len(x)) 
        for i in range(x[k])
    )

def parents(x, max_nodes):
    return set().union(
        sort(x[:k] + (i,) + x[k+1:])  
        for k in range(len(x)) 
        for i in range(x[k]+1, max_nodes+1)
    )
            
def mark_as_loser(x, winners, losers, todo, max_nodes):
    losers.add(x)
    todo.discard(x)
    for p in parents(x, max_nodes):
        winners[p].append(x)
        todo.discard(p)
        for gp in parents(p, max_nodes):
            if gp not in winners and gp not in losers:
                todo.add(gp)

def solve(max_nodes, num_columns, debug=False):
    winners = defaultdict(list)
    losers = set()
    todo = set()
    
    seed = sort((1,) + tuple(0 for _ in range(num_columns-1)))
    mark_as_loser(seed, winners, losers, todo, max_nodes)
    while todo:
        x = todo.pop()
        if all(c in winners for c in children(x)):
            if debug:
                print(f'{x} is a loser!')
            mark_as_loser(x, winners, losers, todo, max_nodes)

    return winners, losers


class GameTree:
    def __init__(self, board):
        self.winners, self.losers = solve(
            max_nodes=max(board), 
            num_columns=len(board)
            )
        