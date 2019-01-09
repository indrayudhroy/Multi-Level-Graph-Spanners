import networkx as nx
import heapq
import copy

def main(graph_file, MAX_WEIGHT, MAX_COST, sourceNode, destNode):

	LABEL_INDEX = 2

	file=open(graph_file, 'r')

	G=nx.Graph()

	numEdges = int(file.readline())
	# numVertices = numEdges

	for i in range(0, numEdges):
		line = file.readline()
		edgeData = line.split()
		u = (int)(edgeData[0])
		v = (int)(edgeData[1])
		weight = (int)(edgeData[2])
		cost = (int)(edgeData[3])
		#print(edgeData)
		G.add_edge(u,v,weight=weight,cost=cost)

	file.close()

	# B = 33
	# M = 33
	# source = -1
	# dest = -1

	B = MAX_WEIGHT
	M = MAX_COST
	source = sourceNode
	dest = destNode

	# dest = list(G.nodes)[0]
	# source = list(G.nodes)[5]

	# =================================================
	print ("destination = " + str(dest) + ", source = " + str(source))
	T_w = nx.Graph()
	T_w = find_spt(G, dest, 'weight')
	T_c = nx.Graph()
	T_c = find_spt(G, dest, 'cost')

	# print ("Main graph")
	# print("Nodes of graph: ")
	# print(G.nodes())
	# print("Edges of graph: ")
	# print(G.edges())

	# print("Nodes of COST graph: ")
	# print(T_c.nodes())
	# print("Edges of graph: ")
	# print(T_c.edges())
	# =================================================

	auto_id = 0

	emptyGraph = nx.Graph()
	lab1 = Label(0, emptyGraph, source, 0)

	listForHeap = []
	listForHeap.append((0, auto_id, lab1))
	auto_id += 1

	H = list(listForHeap)
	heapq.heapify(H)

	count = 1
	savedFinalLabel = Label(-1, emptyGraph, -1, -1)

	while H:

		# print("count = " + str(count))

		cheapestLabel = heapq.heappop(H)
		cost = cheapestLabel[LABEL_INDEX].c
		path = cheapestLabel[LABEL_INDEX].path
		node = cheapestLabel[LABEL_INDEX].n 
		weight = cheapestLabel[LABEL_INDEX].w 

		if node == dest:
			# Done
			# 'path' is the cheapest path satisfying max wt. constraints

			# print("END --> node = dest. SOURCE = " + str(source) + ", DEST = " + str(dest))
			# print("FINAL Path:   ")
			# print(path.edges())
			# print("Cost = " + str(cost) + ", weight = " + str(weight))
			savedFinalLabel = copy.deepcopy(cheapestLabel[LABEL_INDEX])
			# print(savedFinalLabel.path.edges())
			break
		else:

			# char = str(node)
			# print("Selected NODE: " + char)
			# print("Cheapest node from heapq is path ending at " + char + ". Path = " + str(path.edges) + " with cost = " + str(cost)) 

			adjlist = G[node]

			for item in adjlist:

				# print("----------")
				# print (item)

				v = item
				temp = nx.Graph()
				newWeight = weight+(int)(G[node][v]['weight'])
				newCost = cost+(int)(G[node][v]['cost'])

				thisEdgeWeight = (int)(G[node][v]['weight'])
				thisEdgeCost = (int)(G[node][v]['cost'])

				temp.add_edge(node,v,weight=thisEdgeWeight,cost=thisEdgeCost)

				newPath = nx.compose(path, temp)
				# print("Edges of graph: ")
				# print(newPath.edges())


				# total wt, cost = sum of edges of newPath
				sumWeight = 0
				sumCost = 0
				for (temp_u, temp_v, wt) in newPath.edges.data('weight', default=0):
					sumWeight += wt
				for (temp_u, temp_v, cst) in newPath.edges.data('cost', default=0):
					sumCost += cst

				costIndex = sumCost
				# print ("costIndex = " + str(costIndex))

				t_label1 = Label(sumCost, newPath, v, sumWeight)

				# find shortest path length in original T_w and T_c

				Tw_ni = nx.shortest_path_length(T_w,source=dest,target=v,weight='weight')
				Tc_ni = nx.shortest_path_length(T_c,source=dest,target=v,weight='cost')

				totalMaxWeight = sumWeight + Tw_ni
				totalMaxCost = sumCost + Tc_ni

				presentEdge1 = (node, v)
				presentEdge2 = (v, node)
				# print(presentEdge1)
				# print(presentEdge2)
				edgeAlreadyAdded1 = presentEdge1 in path.edges()
				edgeAlreadyAdded2 = presentEdge2 in path.edges()
				edgeAddedToggle = edgeAlreadyAdded1 or edgeAlreadyAdded2

				# edgeAddedToggle = path.has_edge(node,v)
				# print("Toggle = " + str(edgeAddedToggle))

				if totalMaxWeight > B or totalMaxCost > M or edgeAddedToggle == True:
					# discard
					# print("Edge discarded.")
					pass
				else:
					heapq.heappush(H, (costIndex, auto_id, t_label1))
					auto_id += 1
					# print("Heappush check.")

				ordered = list(H)
				# print(ordered)
				freshList = []
				fresh_id = 0

				for ii in range(0,len(ordered)):

					i = ordered[ii]
					addLabel = True

					costIndex = i[0]
					currLabel_i = i[LABEL_INDEX]
					w1 = currLabel_i.w
					c1 = currLabel_i.c
					endingNode1 = currLabel_i.n

					# j = ii + 1;
					for jj in range(0,len(ordered)):

						j = ordered[jj]

						currLabel_j = j[LABEL_INDEX]
						w2 = currLabel_j.w
						c2 = currLabel_j.c
						endingNode2 = currLabel_j.n

						if endingNode1 == endingNode2 and ii != jj:
							# check if dominated label
							# print("ending nodes are the same.")
							if w2 <= w1 and c2 <= c1:
								addLabel = False
								# print ("Label at position " + str(ii) + " is dominated. Discarding.")
								break
								#path 1 is dominated, discard it
								#freshList.append((c1,currLabel_i))

					if addLabel == True:
						freshList.append((costIndex, fresh_id, currLabel_i))
						fresh_id += 1

				# print(freshList)

				heapq.heapify(freshList)					
				H = list(freshList)
				heapq.heapify(H)
				# print("Length of heap = " + str(len(H)))					
				
		count += 1

	# print(savedFinalLabel.path.edges())

	finalPath = savedFinalLabel.path
	finalPathCost = savedFinalLabel.c
	finalPathWeight = savedFinalLabel.w
	finalNode = savedFinalLabel.n
	# return savedFinalLabel

	if finalNode != -1:
		return (finalPath, finalPathCost, finalPathWeight)
	else:
		return (emptyGraph, -1, -1)


def find_spt(digraph, root, weightLabel):
    """
    Finding the shortest-path-tree
    See algorithm here:
    http://www.me.utexas.edu/~jensen/exercises/mst_spt/spt_demo/spt1.html
    :param digraph: graph
    :param root: root node
    :return: spt
    """
    spt = nx.Graph()
    s1 = set()
    s1.add(root)
    path_length = {root: 0}
    s2 = set(digraph.nodes())
    s2.remove(root)
    stop_flag = False
    while s2:
        nodes_from_s2_to_s1 = set()
        direct_reachable_nodes = []
        for source in s1:
            direct_reachable_nodes.extend(digraph.edges(source, data=weightLabel))

        #direct_reachable_nodes = filter(lambda (n1, n2, data): n2 in s2, direct_reachable_nodes)
        direct_reachable_nodes = filter(lambda n1_n2_data: n1_n2_data[1] in s2, direct_reachable_nodes)
        smallest_weight_edge = min(direct_reachable_nodes, key=lambda n1_n2_data: n1_n2_data[2])
        spt.add_weighted_edges_from([smallest_weight_edge])
        nodes_from_s2_to_s1.add(smallest_weight_edge[1])
        s1.update(nodes_from_s2_to_s1)
        s2.difference_update(nodes_from_s2_to_s1)

    return spt

class Label():
	def __init__(self, c, path, n, w):
		self.c = c
		self.path = path
		self.n = n
		self.w = w    

# main()