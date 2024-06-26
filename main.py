import networkx as nx
import ndjson
import json
import csv

# read jlpt kanji list
kanji = set()
with open('data/kanji_JLPT_N5.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        kanji.add(row['Kanji'])

# read ndjson data and create graph
dag = nx.DiGraph()
hanzi = set()

with open('data/dictionary.txt', 'r') as f:
    reader = ndjson.reader(f)

    for row in reader:
        hanzi.add(row['character'])

        # skip non-kanji
        if row['character'] not in kanji:
            continue

        dag.add_node(row['character'], data=row)
        
        #for parent in row['decomposition']:
        #    if parent not in '？⿰⿱⿻⿳⿺⿸⿲⿹⿴⿵⿶⿷':
        #        dag.add_edge(parent, row['character'])


print(kanji.difference(hanzi))
exit(0)

# compute topological generations
generations = nx.topological_generations(dag)

# create the data structure for a tangled tree layout
data_attribute = nx.get_node_attributes(dag, 'data')
generations = [[data_attribute[node] for node in sorted(generation)] for generation in generations]

for g in generations:
    for node in g:
        node['id'] = node['character']
        node['parents'] = [parent for parent in dag.predecessors(node['id'])]

# write the data structure to JSON
with open('data/tangled_tree.json', 'w', encoding='utf8') as f:
    json.dump(generations, f, ensure_ascii=False)
