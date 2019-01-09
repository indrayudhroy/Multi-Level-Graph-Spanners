import networkx as nx
import random
import sys
import math
if len(sys.argv) < 10:
	print("usage: python3 cssp.py number_of_grpahs"
		+ "\n" +"levels initial_size path_to_graph_folder={meta/}"
		+ "\n" + "class_of_graph={0/watts_strogatz,1/erdos_renyi,2/preferential,3/geometric} param1 param2"
		+ "\n" + "node_distribution_in_levels={0/linear,1/exponential} will_graph_size_change(0/1)"
		+ "\n" + "watts_strogatz:param1->neighbors,param2->probability"
		+ "\n" + "erdos_renyi:param1->probability"
		+ "\n" + "preferential:param1->neighbors"
		+ "\n" + "geometric:param1->Distance threshold value")
	print()
	quit()

#graph = nx.fast_gnp_random_graph(10,.2)
size = int(sys.argv[1])
levels = int(sys.argv[2])
initial_size = int(sys.argv[3])
param1 = float(sys.argv[6])
param2 = float(sys.argv[7])
node_distribution_in_levels = int(sys.argv[8])
will_graph_size_change = int(sys.argv[9])
for i in range(size):
	if will_graph_size_change == 1:
		nodes = i+initial_size
	else:
		nodes = initial_size
	avg_deg = 0
	if initial_size<10:
		avg_deg = 3
	else:
		#avg_deg = 6
		avg_deg = param1
	class_of_graph = int(sys.argv[5])
	while True:
		if class_of_graph==0:
			#graph = nx.connected_watts_strogatz_graph(nodes,avg_deg,.2)
			graph = nx.connected_watts_strogatz_graph(nodes,int(avg_deg),param2)
		elif class_of_graph==1:
			graph = nx.generators.random_graphs.erdos_renyi_graph(nodes,param1)
		elif class_of_graph==2:
			graph = nx.generators.random_graphs.barabasi_albert_graph(nodes,int(param1))
		elif class_of_graph==3:
			graph = nx.generators.geometric.random_geometric_graph(nodes,param1)
		if nx.is_connected(graph):
			break
	print("For steiner app:")
	print(graph.number_of_edges())
	# used below also, copy and replace print with write
	if class_of_graph==3:
		pos=nx.get_node_attributes(graph,'pos')
	edges = graph.edges()
	edge_weights = []
	edge_costs = []
	ei = 0
	for e in edges:
		edge_weights.append(random.randint(1,10))
		edge_costs.append(random.randint(1,10))
		if class_of_graph!=3:
			print(str(e[0]+1)+" "+str(e[1]+1)+" "+str(edge_weights[ei])+" "+str(edge_costs[ei]))
			ei = ei + 1
		else:
			x1, y1 = pos[e[0]]
			x2, y2 = pos[e[1]]
			print(str(e[0]+1)+" "+str(e[1]+1)+" "+str(math.pow((x1-x2)**2+(y1-y2)**2,.5))+" "+str(edge_costs[ei]))
	print(str(levels))
	for l in range(levels):
		if node_distribution_in_levels==0:
			if initial_size<10:
				steiner_nodes = initial_size-2
			else:
				steiner_nodes = int(nodes*(l+1)/(levels+1))
			steiner_nodes_str = ""
			for j in range(steiner_nodes-1):
				steiner_nodes_str = steiner_nodes_str + str(j+1) + " "
			steiner_nodes_str = steiner_nodes_str + str(steiner_nodes);
		elif node_distribution_in_levels==1:
			if initial_size<10:
				steiner_nodes = initial_size-2
			else:
				steiner_nodes = int(math.ceil(nodes*1.0/math.pow(2,levels-l)))
			steiner_nodes_str = ""
			for j in range(steiner_nodes-1):
				steiner_nodes_str = steiner_nodes_str + str(j+1) + " "
			steiner_nodes_str = steiner_nodes_str + str(steiner_nodes);
		print(steiner_nodes_str)
	file = open("A"+sys.argv[4]+"_"+str(i+1)+".txt","w")
	file.write(str(graph.number_of_edges())+"\n");
	if class_of_graph==3:
		pos=nx.get_node_attributes(graph,'pos')
	edges = graph.edges()
	ei = 0
	for e in edges:
		if class_of_graph!=3:
			file.write(str(e[0]+1)+" "+str(e[1]+1)+" "+str(edge_weights[ei])+" "+str(edge_costs[ei])+"\n")
			ei = ei + 1
		else:
			x1, y1 = pos[e[0]]
			x2, y2 = pos[e[1]]
			file.write(str(e[0]+1)+" "+str(e[1]+1)+" "+str(math.pow((x1-x2)**2+(y1-y2)**2,.5))+" "+str(edge_costs[ei])+"\n")
	file.write(str(levels)+"\n")
	for l in range(levels):
		if node_distribution_in_levels==0:
			if initial_size<10:
				steiner_nodes = initial_size-2
			else:
				steiner_nodes = int(nodes*(l+1)/(levels+1))
			steiner_nodes_str = ""
			for j in range(steiner_nodes-1):
				steiner_nodes_str = steiner_nodes_str + str(j+1) + " "
			steiner_nodes_str = steiner_nodes_str + str(steiner_nodes);
		elif node_distribution_in_levels==1:
			if initial_size<10:
				steiner_nodes = initial_size-2
			else:
				steiner_nodes = int(math.ceil(nodes*1.0/math.pow(2,levels-l)))
			steiner_nodes_str = ""
			for j in range(steiner_nodes-1):
				steiner_nodes_str = steiner_nodes_str + str(j+1) + " "
			steiner_nodes_str = steiner_nodes_str + str(steiner_nodes);
		file.write(steiner_nodes_str+"\n")
	file.close()
	print("For viewer app:")
	# used below also, copy and replace print with write
	print(graph.number_of_nodes())
	if class_of_graph==3:
		pos=nx.get_node_attributes(graph,'pos')
	edges = graph.edges()
	ei = 0
	for e in edges:
		if class_of_graph!=3:
			print(str(e[0])+" "+str(e[1])+" "+str(edge_weights[ei])+" "+str(edge_costs[ei]))
			ei = ei + 1
		else:
			x1, y1 = pos[e[0]]
			x2, y2 = pos[e[1]]
			print(str(e[0])+" "+str(e[1])+" "+str(math.pow((x1-x2)**2+(y1-y2)**2,.5))+" "+str(edge_costs[ei]))
	file = open("A"+sys.argv[4]+"_viewer_app"+str(i+1)+".txt","w")
	file.write(str(graph.number_of_nodes())+"\n");
	if class_of_graph==3:
		pos=nx.get_node_attributes(graph,'pos')
	edges = graph.edges()
	ei = 0
	for e in edges:
		if class_of_graph!=3:
			file.write(str(e[0])+" "+str(e[1])+" "+str(edge_weights[ei])+" "+str(edge_costs[ei])+"\n")
			ei = ei + 1
		else:
			x1, y1 = pos[e[0]]
			x2, y2 = pos[e[1]]
			file.write(str(e[0])+" "+str(e[1])+" "+str(math.pow((x1-x2)**2+(y1-y2)**2,.5))+" "+str(edge_costs[ei])+"\n")
	file.close()