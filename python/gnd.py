'''
By Petter Holme, May 15, 2019.
This is a Python implementation of the GND (not the GNDR) algorithm as described in:
Xiao-Long Ren, Niels Gleinig, Dirk Helbing, and Nino Antulov-Fantulin, Generalized network dismantling, PNAS 116, 6554-6559 (2019).
Unlike the paper, this code uses a standard solver for the eigenvectors.
The program can be run as: "python gnd.py network.adj [degree/unit specifying the cost function]" where network.adj is an edgelist representation of the network.
Output is as follows (per row): [accumulated deletion cost] [deleted node id] [size of largest connected component]
The randomness in the output comes from the code breaking ties by randomness. To make the output independent of the labeling of nodes.
'''

from sys import argv, stderr, exit
import networkx as nx
from networkx.algorithms.approximation import min_weighted_vertex_cover
from scipy.sparse.linalg import eigsh
from scipy.sparse.linalg.eigen.arpack.arpack import ArpackNoConvergence
from scipy.sparse import diags
import numpy as np
from numpy.random import shuffle

#  ======================================================================================================
# calculating the size of the largest connected component

def largest_connected_component(G):
    if len(G) == 0:
        return 0

    return max([len(connected_components) for connected_components in nx.connected_components(G)])


#  ======================================================================================================
# removing a node and printing the update

def remove_and_print_update(G, v):
    if G.graph['cost type'] == 'degree':
        G.graph['cost sum'] += G.degree(v)
    else:
        G.graph['cost sum'] += 1
    G.remove_node(v)
    print(str(G.graph['cost sum']), v, str(largest_connected_component(G)))


#  ======================================================================================================
# path -> path of edgelist
# cost -> degree, unit
def gnd(path, cost, budget):
    G = nx.read_edgelist(path)
    G.graph['cost type'] = cost
    G.graph['cost sum'] = 0

    if G.graph['cost type'] not in ['degree', 'unit']:
        print('usage: python gnd.py [adj file] [weight (degree or unit)]')
        exit(1)

    inf = []
    i = 0
    while largest_connected_component(G) > 2 and i < budget:
        localInf = []
        if i > 0:
            G = nx.Graph(G.subgraph(max(nx.connected_components(G), key=len)))
        # Step 1. === Construct the spectral partition of the largest connected component (LCC). ===

        LCC = G.subgraph(max(nx.connected_components(G), key=len))  # Get the LCC.
        ii = {v: i for i, v in enumerate(list(LCC.nodes()))}  # Store the node indices in the same order as LCC.

        # Construct the matrix. Notations following the paper. (We calculate the 2nd smallest eigenpair
        # directly (by the solver) rather than "manually" shifting the eigenvalues and calculate the 2nd
        # largest as mentioned in the paper.)
        if G.graph['cost type'] == 'degree':
            W = diags([d for v, d in LCC.degree()], dtype=np.int32)  # weighted matrix
            A = nx.adjacency_matrix(LCC)    # adjacency matrix
            B = A * W + W * A - A           # B = AW + WA - A
            DB = diags(np.squeeze(np.asarray(B.sum(axis=1))), dtype=np.int32)
            L = DB - B                      # Lw = [Db - B]
        else:
            L = nx.laplacian_matrix(LCC)

        # Get the eigenvectors.
        maxiter = 1000 * L.shape[0]  # when to give up, 100 times more generous than default
        try:
            eigenvalues, eigenvectors = eigsh(L.astype(np.float32), k=2, which='SM', maxiter=maxiter)
        except ArpackNoConvergence as err:
            print >> stderr, err
            exit(1)

        Fiedler = eigenvectors[:, 1]  # not really Fiedler vector, but corresponding to it

        # Step 2. === Construct a subgraph of nodes at the border of the partition. ===
        H = nx.Graph()
        for u, v in LCC.edges():
            # Adding edges between nodes of different sign. (Note that just < (not <=) would mis-classify
            # nodes in symmetric graphs like 2 in 1-2-3.)
            if Fiedler[ii[u]] * Fiedler[ii[v]] <= 0.0:
                H.add_edge(u, v)

        # Step 3. === Construct a minimal vertex cover of H w.r.t. degree in G / degree in H. ===
        for v in H.nodes():  # calculate weight
            H.nodes[v]['weight'] = 1.0 / H.degree(v)
            if G.graph['cost type'] == 'degree':
                H.nodes[v]['weight'] *= LCC.degree(v)

        cover = list(min_weighted_vertex_cover(H, weight='weight'))  # get the vertex cover
        shuffle(cover)  # shuffle away dependence on input

        # Step 4. === Delete the nodes in cover. ===
        for v in cover:
            localInf.append(v)
            remove_and_print_update(G, v)
        i = i + 1
        inf.append(localInf)

    print('final inf')
    print(inf)


#  ========================================================================================================
gnd('../dataset/city_network', 'unit', 25)
exit(0)