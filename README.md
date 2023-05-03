---
bibliography: mybib.bib
nocite: '@*'
...

# Influence Maximization for Partially Observable Networks with Varying Degree Assortativities

## Introduction

Understanding how information disseminate in today's world has never been more important: individuals, companies, organizations, and governments face limited resources and increasing competition for audience attention in spreading their messages and encouraging actions.
The influence maximization problem has a range of applications, spanning product marketing strategy, humanitarian crowdfunding, participatory data collection, and spreading awareness about health resources. Decision-makers must not only consider how their messages will be diffused within their direct sphere of influence—existing customers, social media followers, current patients—but also how it will spread beyond what is known—friends of customers, followers of followers, coworkers of patients.

The goal of information dissemination is to effectively spread a message as widely as possible within a given network. The influence maximization problem is to select the most influential members within a social network such that the outcome of the spreading process is optimized.
Formally, given a directed network $G = (V, E, w)$ where $V$ is a set of nodes, $E \subseteq V \times V$ is a set of directed edges, and $w: E \rightarrow [0, 1]$ represents a weight function in which $w(i, j)$ is the likelihood of $j$ being influenced by $i$. Let an initial seed set $S \subset V$ of fixed size $M$ become activated. Then, each activated node $i \in S$ activates its neighboring node $j$ with probability $w(i, j)$. The goal is to find the initial seed set $S$ such that the total number of activated nodes is maximized.

However, the assumption of having complete knowledge of the full network is unrealistic. We often observe only parts of the network. Let $G' = (V', E', w')$ be the observable part of $G$, where $V' \subseteq V$ is the set of observable nodes, $E' = E \cap V' \times V'$ is the set of observed, directed edges, and $w': E' \rightarrow [0, 1]$ represents the new weight function whose range includes the weights of the edges belonging to $E'$. Thus, given only the observable part $G'$ of the network $G$, we want to find the seed set $S \subseteq V'$ of size $M$ such that the total number of activated nodes *in the underlying network* $G$ is maximized. 

This work is inspired by Stein et al. (2017) which investigates different heuristic algorithms to select seeds for partially observable networks. The heuristic algorithms experimented include:

1. **Random Selection**: Select initial seeds from the observable set uniformly at random.
2. **Random with Neighbor Activation**: Select $M$ random nodes, and then for each node, activate one of its neighbors. This method is based on the *friendship paradox*.
3. **Degree-Based Selection**: Rank known nodes based on degree, and select those with the highest rank as seeds. In the weighted version, attach a small extra weight to the ranking of neighbors of boundary nodes before selection, using the intuition that neighbors of boundary nodes likely have higher influence on unknown part of network.
4. **State-of-the-Art IMM algorithms with Limited Visibility**: classic IM algorithms such as TIM (Tang et al., 2014) and IMM (Tang et al., 2015) developed for fully observed networks.

Stein et al. shows that the weighted degree-based
method outperforms the state-of-the-art algorithms on the NetHept dataset -- a collaboration network within the high energy physics theory community between 1991 and 2003 -- particularly when network visibility is low. 


## Examples

First, you must install and import dependencies:

```python
import networkx as nx
import numpy as np
```

After creating an `networkx.classes.digraph.DiGraph` object called `graph`, you can simulate an observable part of the network with given target visibility, select seeds, and run a weighted independent cascade model on the network as follows:

```python
from models.observableSubgraph import create_subgraph, simulate_observable_nodes
from models.seeding import Seeding
from models.independentCascade import IndependentCascade


fully_observ_O, boundary_nodes = simulate_observable_nodes(graph, target_visibility = 0.1)
observable_nodes = fully_observ_O + boundary_nodes
observable_graph = create_subgraph(graph, observable_nodes)

seeding = Seeding(observable_graph, method = 'weighted-degree-based')
seeds = seeding(boundary_nodes, weight = 3, num_seed = 5)
print(seeds)

ic_model = IndependentCascade(graph, seeds)
activated = ic_model.simulate()
print(ic_model.get_spread())

avg_spread = ic_model.run_simulations(iters = 10)
print(f"Average spread across 10 runs: {avg_spread}")
```

Check out an example in `example.ipynb`!

## References

Stein, S., Eshghi, S., Maghsudi, S., Tassiulas, L., Bellamy, R. K. E., & Jennings, N. R. (2017). Heuristic algorithms for influence maximization in partially observable social networks. In *SocInf@IJCAI*.

Tang, Y., Shi, Y., & Xiao, X. (2015). Influence maximization in near-linear time: A martingale approach. *CM SIGMOD International Conference on Management of Data*.

Tang, Y., Xiao, X., & Shi, Y. (2014). *Influence maximization: Near-optimal time complexity meets practical efficiency*.


## Citation

@misc{kirati-influence-max,
  author = {Lyla Kiratiwudhikul, Caleb Saul, Derek Chang, Ben Elliott},
  title = {Influence Maximization for Partially Observable Networks with Varying Degree Assortativities},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/lylakirati/influence_maximization}}
}