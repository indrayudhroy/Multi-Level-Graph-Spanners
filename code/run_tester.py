import cspp
import networkx as nx
import copy
import os

# emptyGraph = nx.Graph()
# constrained_shortest_path_label = cspp.Label(0, emptyGraph, 0, 0)

returnedPath = nx.Graph()

MAX_WEIGHT = 7
MAX_COST = 22
source = 1
dest = 5

for filename in os.listdir('test_graphs/'):
	graphFile = 'test_graphs/' + filename
	# constrained_shortest_path_label = copy.deepcopy(cspp.main(graphFile, 7, 22, 1, 5))
	(returnedPath, cost, weight) = cspp.main(graphFile, MAX_WEIGHT, MAX_COST, source, dest)
	if cost != -1:
		print("Success. Shortest path is:")
		print(returnedPath.edges())
		print(" Cost = " + str(cost))
		print(" Weight = " + str(weight))
		print()
	else:
		print("No path found.")

print("--end.")




