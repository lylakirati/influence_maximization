import networkx as nx
import numpy as np

class Seeding():
    
    _supported_methods = ["weighted-degree-based", "degree-based", "random"]
    
    def __init__(self, observable_graph, method = 'weighted-degree-based'):
        self.observable_graph = observable_graph
        if method not in self._supported_methods:
            raise ValueError("Unsupported seeding method")
        self.method = method
        
        
    def __call__(self, *args, **kwargs):
        if self.method == "weighted-degree-based":
            return self.seed_weighted_degree(*args, **kwargs)
        elif self.method == "degree-based":
            return self.seed_degree(*args, **kwargs)
        elif self.method == "random":
            return self.seed_random(*args, **kwargs)
        else:
            return None
        
        
    def seed_random(self, num_seed = 5, activate_neighbor = False):
        random_nodes = list(np.random.choice(self.observable_graph.nodes,
                                     size = num_seed))
        if activate_neighbor:
            neighbors_set= [list(self.observable_graph.neighbors(node)) for node in random_nodes]
            eligible_neighbors = {random_nodes[i]: neighbors 
                                  for i, neighbors in enumerate(neighbors_set)
                                  if len(neighbors) != 0}
            
            while len(eligible_neighbors) < num_seed:
                node_pool = list(set(self.observable_graph.nodes) - set(eligible_neighbors.keys()))
                random_nodes = np.random.choice(node_pool, 
                                                size = num_seed - len(eligible_neighbors))
                neighbors_set= [list(self.observable_graph.neighbors(node)) 
                                for node in random_nodes]
                eligible_neighbors.update({random_nodes[i]: neighbors 
                                            for i, neighbors in enumerate(neighbors_set)
                                            if len(neighbors) != 0})
            
            return [np.random.choice(neighbors, size = 1)[0] 
                    for neighbors in eligible_neighbors]
        else:
            return random_nodes
        
        
    def seed_degree(self, num_seed = 5):
        node_to_outdegree = dict(self.observable_graph.out_degree())
        
        # rank nodes from highest out-degree
        node_ranks = sorted(node_to_outdegree.items(),
                            key = lambda x: x[1], reverse = True)
        return [n[0] for n in node_ranks[: num_seed]]


    def seed_weighted_degree(self, boundary_nodes, weight = 3, num_seed = 5):
        node_to_outdegree = dict(self.observable_graph.out_degree())
        
        # add extra weights for boundary nodes
        for node in boundary_nodes:
            node_to_outdegree[node] += weight
        
        # rank nodes from highest out-degree
        node_ranks = sorted(node_to_outdegree.items(), 
                            key = lambda x: x[1], reverse = True)
        return [n[0] for n in node_ranks[: num_seed]]