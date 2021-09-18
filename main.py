import networkx as nx

dag = nx.DiGraph([(2,1),(3,1),(4,2)])
generations = [sorted(generation) for generation in nx.topological_generations(dag)]
print(generations)