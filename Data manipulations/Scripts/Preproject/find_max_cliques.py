import pandas as pd
from tqdm import trange

data = pd.read_csv("../Outdata/CrossAUC.csv", index_col=0)
data.replace("*", 0, inplace=True)
data = data.apply(pd.to_numeric)
data = data > 0.6

studies = data.columns

max_cliques = []

def verify_clique_is_max(clique):
    rest = set(studies) - set(clique)
    for r in rest:
        edges = [data[s][r] * data[r][s] for s in clique]
        if len(edges) == sum(edges):
            return False
    return True

def add_node(clique, index):
    for i, r in enumerate(studies[index:]):
        edges = [data[s][r] * data[r][s] for s in clique]
        if len(edges) == sum(edges):
            clique.add(r)
            add_node(clique, index+i+1)
            clique.remove(r)
    if verify_clique_is_max(clique):
        max_cliques.append(clique.copy())

add_node(set(), 0)
print(sorted(max_cliques, key=len, reverse=True))
