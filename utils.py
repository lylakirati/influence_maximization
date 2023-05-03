from random import choices

import networkx as nx
import numpy as np

def alter_connections(graph, num_edges):    
    '''Returns a new graph with `num_edges` connections altered
    
    Alter a connection (u, v_1) in the given graph 
    by removing (u, v_1) and adding a new connection (u, v_2)
    where v_2 is a random node different from v_1
    
    Parameter
    ------
    graph : networkx.classes.digraph.DiGraph object
        original graph to alter connections
    num_edges : int
        number of connections to alter
        
    Returns
    ------
    new_graph : networkx.classes.digraph.DiGraph object
        new graph with connections altered
    '''
    if not isinstance(graph, nx.classes.digraph.DiGraph):
        raise TypeError("graph must be of type networkx.classes.digraph.DiGraph")    
    
    edges = list(graph.edges())
    if num_edges > len(edges):
        raise ValueError("num_edges cannot be greater than the number of edges in the original graph")
    
    to_delete_edges = choices(edges, k = num_edges)
    new_graph = nx.DiGraph(graph)
    new_graph.remove_edges_from(to_delete_edges)
    
    nodes = set(new_graph.nodes())
    # find new connections
    for u, v_1 in to_delete_edges:
        candidates = nodes - {v_1} # remove old neighbor v_1 from candidate set
        new_neighbor = np.random.choice(list(candidates), size = 1)[0]
        new_graph.add_edge(u, new_neighbor)
        
    return new_graph