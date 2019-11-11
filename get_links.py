import json
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from pprint import pprint

with open('cran_packages.json', 'r') as f:
	data = json.load(f)

depends_graph = nx.DiGraph()
imports_graph = nx.DiGraph()
suggests_graph = nx.DiGraph()

for package in data:
	depends_graph.add_node(package)
	imports_graph.add_node(package)
	suggests_graph.add_node(package)

for package in data:
	depends = list(data[package]['depends'].keys())
	for item in depends:
		depends_graph.add_edge(package, item)
		imports_graph.add_edge(package, item)

	imports = list(data[package]['imports'].keys())
	for item in imports:
		imports_graph.add_edge(package, item)

	suggests = list(data[package]['suggests'].keys())
	for item in suggests:
		suggests_graph.add_edge(package, item)

# write_dot(imports_graph, 'imports_graph.dot')
# pprint(list(imports_graph.edges))

for node in imports_graph.nodes:
	print(node+': {}'.format(imports_graph.in_degree(node)))