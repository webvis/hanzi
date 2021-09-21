import networkx as nx
import ndjson

dag = nx.DiGraph()

with open('data/dictionary.txt', 'r') as f:
    reader = ndjson.reader(f)

    for row in reader:
        dag.add_node(row['character'], data=row)
        
        for parent in row['decomposition']:
            if parent not in '？⿰⿱⿻⿳⿺⿸⿲⿹⿴⿵⿶⿷':
                dag.add_edge(parent, row['character'])

print(dag.number_of_nodes())
generations = [sorted(generation) for generation in nx.topological_generations(dag)]
print(len(generations))