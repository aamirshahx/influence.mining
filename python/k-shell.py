import networkx as nx
import matplotlib.pyplot as plt


# Check if there is any node left with degree d
def check(graph, iteration):
    f = 0  # there is no node of deg <= iteration
    for i in graph.nodes():
        if graph.degree(i) <= iteration:
            f = 1
            break
    return f


# Find list of nodes with particular degree
def find_nodes(graph, iteration):
    set1 = []
    for i in graph.nodes():
        if graph.degree(i) <= iteration:
            set1.append(i)
    return set1


graph = nx.read_edgelist('../dataset/city_network_min')
graph_copy = graph.copy()
it = 1

# Bucket being filled currently
tmp = []

# list of lists of buckets
buckets = []
while 1:
    flag = check(graph_copy, it)
    if flag == 0:
        it += 1
        buckets.append(tmp)
        tmp = []
    if flag == 1:
        node_set = find_nodes(graph_copy, it)
        for each in node_set:
            graph_copy.remove_node(each)
            tmp.append(each)
    if graph_copy.number_of_nodes() == 0:
        buckets.append(tmp)
        break

print(buckets)
influential_group = max([len(i) for i in buckets])


