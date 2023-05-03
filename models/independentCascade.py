import networkx as nx
import numpy as np

class IndependentCascade():
    
    def __init__(self, graph, seeds, weighted = True):
        self.graph = graph
        self.seeds = seeds
        self.weighted = weighted
        self.activated = set()
        self.inactivated = set(self.graph.nodes)
        
    def __call__(self, *args, **kwargs):
        if self.weighted:
            return self.simulate_weighted_IC(*args, **kwargs)
        else:
            return self.simulate_IC(*args, **kwargs)
        
    def get_activated(self):
        return self.activated
    
    def get_inactivated(self):
        return self.inactivated
    
    def get_spread(self):
        return len(self.activated)
        
    def simulate_IC(self, prob = 0.2):
        if prob <= 0 or prob > 1:
            raise ValueError("Activation probability must be between 0 and 1")
        
        self.activated = set(self.seeds)
        self.inactivated -= self.activated
        spreading = self.seeds
        
        while len(self.inactivated) != 0:
            spreading_next = []
            for node in spreading:
                neighbors = list(set(self.graph.neighbors(node)) - set(self.activated))
                infected =  [node for node in neighbors if np.random.binomial(1, prob)]
                self.activated.update(infected)
                self.inactivated -= set(infected)
                spreading_next = spreading_next + infected
            spreading = spreading_next
            if len(spreading) == 0:
                break
        
        return self.activated
        
    
    def simulate_weighted_IC(self):
        self.activated = set(self.seeds)
        self.inactivated -= self.activated
        spreading = self.seeds
        
        while len(self.inactivated) != 0:
            spreading_next = []
            for node in spreading:
                neighbors = list(set(self.graph.neighbors(node)) - set(self.activated))
                probs = [1.0 / deg for deg in dict(self.graph.in_degree(neighbors)).values()]
                is_infected = np.random.binomial(([1] * len(neighbors)), probs)
                infected = [node for node, infected in zip(neighbors, is_infected) if infected == 1]
                self.activated.update(infected)
                self.inactivated -= set(infected)
                spreading_next = spreading_next + infected
            spreading = spreading_next
            if len(spreading) == 0:
                break
        
        return self.activated
        