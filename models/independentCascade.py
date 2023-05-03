import networkx as nx
import numpy as np

class IndependentCascade():
    """(Weighted) Independent Cascade Model of Social Contagion
    
    Attributes
    ------
    graph : networkx.classes.digraph.DiGraph object
        full network graph that information will spread on
    seeds : list of int
        list of initial seeds
    activated : set of int
        set of activated nodes
    inactivated : set of int
        set of inactivated nodes
        
    Examples
    ------
    >>> ic_model = IndependentCascade(graph, seeds)
    >>> activated = ic_model.simulate(weighted = False, prob = 0.2)
    >>> print(ic_model.get_spread())
    135
    >>> avg_spread = ic_model.run_simulations(weighted = True, iters = 10)
    >>> print(f"Average spread across 10 runs: {avg_spread}")
    Average spread across 10 runs: 97.6
    """
    
    def __init__(self, graph, seeds):
        self.graph = graph
        self.seeds = seeds
        self.activated = set()
        self.inactivated = set(self.graph.nodes)
        
    def simulate(self, weighted = True, prob = None):
        if (prob is None) and (not weighted):
            raise ValueError("Must specify activation probability for non-weighted IC simulation")
        
        if weighted:
            return self.simulate_weighted_IC()
        else:
            return self.simulate_IC(prob)
    
    
    def run_simulations(self, weighted = True, prob = None, iters = 5):
        spreads = [len(self.simulate(weighted, prob)) for i in range(iters)]
        return np.mean(spreads)
    
        
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
        
        while len(self.inactivated) <= 0 or len(spreading) > 0:
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
        self.inactivated = set(self.graph.nodes) - self.activated
        spreading = self.seeds
        
        while len(self.inactivated) <= 0 or len(spreading) > 0:
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
    
        return self.activated
        