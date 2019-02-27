<!-- references -->
[^1]: https://en.wikipedia.org/wiki/Go_(game)
[^2]: https://en.wikipedia.org/wiki/Go_and_mathematics
[^3]: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
[^4]: https://www.nature.com/nature/journal/v529/n7587/full/nature16961.html

AIND "*Build a Game-Playing Agent*"
===================================

Research Review
===============

"*Mastering the game of Go with deep neural networks and tree search*"
----------------------------------------------------------------------

Based on the article published in [*Nature* 529, 484–489 (28 January2016)](https://www.nature.com/nature/journal/v529/n7587/full/nature16961.html)[^4].

------------------------------------------------------------------------

What is interesting about Go[^1], is the mathematics[^2] behind the game that increases the complexity and challenges to find the most optimal next move in a reasonable amount of time, towards to win and beat the most expert human players. This is not an easy task, the number of maximum moves is at the level of astronomical numbers, impossible to process by any existing computer if no specialized technique is used.

To tackle the problem, the approach or the technique used is a combination of *Monte Carlo Tree Search*[^3], *'value'* and *'policy'* networks.

*'Value'* and *'policy'* networks are deep mind neural networks, *'value networks'* to evaluate positions and *'policy networks'* to select the move, trained under a fixed pipeline consisting of:

- supervised training from expert human moves, giving efficient learning with immediate feedback and high-quality gradients 
- reinforcement of the learning policy network by playing against itself

Monte Carlo tree searches use Monte Carlo rollouts, these rollouts allow to search to a maximum deep without branching at all, which combined with the neural networks reduce the effective depth and breadth of the search tree, evaluating positions using a value network and sampling actions using a policy network.

Basically a combination of policy and value networks with *Monte Carlo Search Tree*, still computationally intensive. AlphaGo used asynchronous multi-thread search that executes simulation on CPUs and computes policy and value networks in parallel on GPUs (40 threads and 48 CPUs and 8 GPUs), distributed version use 40 search threads, 1202 CPUs and 176 GPUs.

There are two results that are importantly related to this research:

- the performance against other agents (commercial and free): 99.8% of winning rate, other agents were using Monte Carlo techniques but without any combinations with other techniques or algorithms
- human expert players: 5 to 0 win games against human European Go Champion

Even though this research is huge in terms of tackle problems where the branching factor and tree depth are impossible to tackle, still is computationally expensive as it requires a considerable amount of resources.