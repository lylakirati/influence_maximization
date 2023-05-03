import networkx as nx
import numpy as np

def simulate_observable_nodes(graph, target_visibility, initial_seeds = 4):
    """Simulate sets of fully observable nodes and their boundary nodes
    
    Iteratively select fully observable nodes (whose set is denoted O) 
    until reaching the target network visibility. 
    The set O starts with randomly selected initial seeds.
    Then, at each iteration, select a node from O and add one of its neighbors
    that is currently not in O. If no such neighbors exist, add a random
    node from the original graph to O. Once the target number of fully observable
    nodes is reached, boundary nodes, the neighbors of nodes in O that are not
    in O, are found and returned along side O.

    Parameter
    ------
        graph : networkx.classes.digraph.DiGraph object
            graph to sample observable nodes from
        target_visibility : float
            target network visibility, between 0 (exclusive) and 1 (inclusive)
        initial_seeds : int, optional (defaults to 4)
            number of initial seeds in the fully observable set

    Returns
    ------
        fully_observ_O : list of int
            list of fully observable nodes
        boundary_nodes : list of int
            list of boundary nodes
    """
    if not isinstance(graph, nx.classes.digraph.DiGraph):
        raise TypeError("graph must be of type networkx.classes.digraph.DiGraph")
        
    if target_visibility <= 0 or target_visibility > 1:
        raise ValueError("Target network visibility must be between 0 (exclusive) and 1 (inclusive)")
    
    nodes = list(graph.nodes)
    num_nodes = len(nodes) # number of nodes in the original full graph
    
    if initial_seeds > num_nodes:
        raise ValueError("Number of initial seeds cannot exeed number of nodes in the graph")
    
    if target_visibility == 1: # trivial case
        return nodes, []
    
    ### construct a set of fully observable nodes, denoted O
    target_num_O = int(target_visibility * num_nodes)
    
    # uniform random sample initial seeds to put in O
    fully_observ_O = list(np.random.choice(nodes, 
                                           size = initial_seeds, 
                                           replace = False)) 
    
    all_neighbors = set() # neighbors of nodes in O 
    while len(fully_observ_O) < target_num_O: 
        if all_neighbors.issubset(fully_observ_O):
            # when no such neighbors exist, add a random node to O
            non_neighbors = list(set(nodes) - all_neighbors)
            random_node = np.random.choice(non_neighbors, size = 1)[0]
            fully_observ_O.append(random_node)
            all_neighbors.update(set(graph.neighbors(random_node)))
        else: 
            # pick a node from O and add one of its neighbors that is currently not in O to O
            proposed_node_in_O = np.random.choice(fully_observ_O, size = 1)[0]
            neighbors = list(graph.neighbors(proposed_node_in_O))
            while len(neighbors) == 0:
                proposed_node_in_O = np.random.choice(fully_observ_O, size = 1)[0]
                neighbors = list(graph.neighbors(proposed_node_in_O))
            proposed_neighbor = np.random.choice(list(graph.neighbors(proposed_node_in_O)), 
                                                 size = 1)[0]
            if proposed_neighbor not in fully_observ_O:
                fully_observ_O.append(proposed_neighbor)
                all_neighbors.update(list(graph.neighbors(proposed_neighbor)))
    
    # find boundary nodes (neighbors of nodes in O that are not in O)
    boundary_nodes = list(all_neighbors - set(fully_observ_O))
    
    return fully_observ_O, boundary_nodes


def create_subgraph(graph, selected_nodes):
    """Create an induced subgraph given the selected nodes.

    Parameter
    ------
        graph : networkx.classes.digraph.DiGraph object
            graph to sample from
        selected_nodes : list of int
            list of selected nodes

    Returns
    ------
        observable_graph : networkx.classes.digraph.DiGraph object
            induced subgraph
    """
    observable_graph = nx.induced_subgraph(graph, selected_nodes)
    return observable_graph