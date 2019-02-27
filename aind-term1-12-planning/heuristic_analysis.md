<!-- references -->
[^1]: https://github.com/udacity/AIND-Planning#part-1---planning-problems
[^2]: Artificial Intelligence: Modern Approach, Third Edition - 3.4.2 Uniform-cost search
[^3]: Artificial Intelligence: Modern Approach, Third Edition - Figure 3.21
[^4]: https://github.com/udacity/AIND-Planning/commit/fd65ae7361517616b4263050dc647d7ac6c284fb
[^5]: https://discussions.udacity.com/t/time-elapsed-bfs-vs-ucs/311680/6
[^6]: Artificial Intelligence: Modern Approach, Third Edition - 10.2.3 Heuristics for planning
[^7]: https://en.wikipedia.org/wiki/Completeness

# AIND "_Implement a Planning Search_"

Initial state, action schema and goal for each problem are defined in [AIND-Planning
 project repository](https://github.com/udacity/AIND-Planning#part-1---planning-problems)[^1].

## Results and Analysis

In result tables, for readability purposes, the search algorithm is mapped by the following list:

1. BFS _breadth_first_search_
2. BFTS _breadth_first_tree_search_
3. DFGS _depth_first_graph_search_
4. DLS _depth_limited_search_
5. UCS _uniform_cost_search_
6. RBFS _recursive_best_first_search h_1_
7. GBFGS _greedy_best_first_graph_search h_1_
8. A* _astar_search h_1_
9. A* IP _astar_search h_ignore_preconditions_
10. A* LS _astar_search h_pg_levelsum_

Unspecified results are marked with a dash '_-_' for those searches with an execution times larger than 10 minutes.

### Non Heuristic Planning Searches results

#### Problem 1

| Search   | Expansions | Goal Tests | New Nodes | Plan Length | Execution (s) |
| -------- | ---------- | ---------- | --------- | ----------- | ------------- |
| 1. BFS   | 43         | 56         | 180       | 6           | 0.035097      |
| 2. BFTS  | 1458       | 1459       | 5960      | 6           | 0.971806      |
| 3. DFGS  | 21         | 22         | 84        | 20          | 0.014397      |
| 4. DLS   | 101        | 271        | 414       | 50          | 0.092386      |
| 5. UCS   | 55         | 57         | 224       | 6           | 0.039306      |
| 6. RBFS  | 55         | 57         | 224       | 6           | 2.836245      |
| 7. GBFGS | 7          | 9          | 28        | 6           | 0.005034      |

Based on all the columns, _(7) greedy_best_first_graph_search_ seems to be the most optimal in terms of execution time and space complexity, but this could be misleading, the problem might be not complex enough to put in evidence the optimality of the searches, e.g.: depending on the complexity, _(1) breadth_first_search_ might be a good candidate as well, in the case of _(2)_ the plan length is 6 but the node expansions and new nodes are too large compared with the other strategies.

The plan for this problem would be the one provided by _(7) greedy_best_first_graph_search_:

```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, JFK)
Fly(P2, JFK, SFO)
Unload(C1, P1, JFK)
Unload(C2, P2, SFO)
```

The plan provided by _(1) breadth_first_search_ is similar, only the two final steps differ, since the problem doesn't consider any other factors this plan could be considered as optimal as well:

```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)
```

#### Problem 2

| Search   | Expansions | Goal Tests | New Nodes | Plan Length | Execution (s) |
| -------- | ---------- | ---------- | --------- | ----------- | ------------- |
| 1. BFS   | 3346       | 4612       | 30534     | 9           | 14.572922     |
| 2. BFTS  | -          | -          | -         | -           | > 10 mins     |
| 3. DFGS  | 107        | 108        | 959       | 105         | 0.342523      |
| 4. DLS   | -          | -          | -         | -           | > 10 mins     |
| 5. UCS   | 4605       | 4607       | 41839     | 9           | 12.320716     |
| 6. RBFS  | -          | -          | -         | -           | > 10 mins     |
| 7. GBFGS | 465        | 467        | 4182      | 20          | 1.221490      |

Considering the plan length, time and space complexity in and for this problem only, _(1) breadth_first_search_ is the most optimal search, _(5) uniform_cost_search_ could be a candidate, but _(1) breadth_first_search_ is slight better in time execution and node expansion. Even though there are better execution times and less expansions in other searches, the plan lenght is too large.

The plan provided by _(1) breadth_first_search_:
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Load(C3, P3, ATL)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
```

The plan provided by _(5) uniform_cost_search_, since the problem doesn't consider any other factors this plan could be considered as optimal as well:
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Load(C3, P3, ATL)
Fly(P1, SFO, JFK)
Fly(P2, JFK, SFO)
Fly(P3, ATL, SFO)
Unload(C1, P1, JFK)
Unload(C2, P2, SFO)
Unload(C3, P3, SFO)
```

#### Problem 3

| Search   | Expansions | Goal Tests | New Nodes | Plan Length | Execution (s) |
| -------- | ---------- | ---------- | --------- | ----------- | ------------- |
| 1. BFS   | 14120      | 17673      | 124926    | 12          | 104.073143    |
| 2. BFTS  | -          | -          | -         | -           | > 10 mins     |
| 3. DFGS  | 292        | 293        | 2388      | 288         | 1.257922      |
| 4. DLS   | -          | -          | -         | -           | > 10 mins     |
| 5. UCS   | 16961      | 16963      | 149117    | 12          | 52.024249     |
| 6. RBFS  | -          | -          | -         | -           | > 10 mins     |
| 7. GBFGS | 3998       | 4000       | 35002     | 30          | 12.237363     |

Same as problem 2, _(1) breadth_first_search_ is slightly better than _(5) uniform_cost_search_ in terms of node expansion, and _(5) uniform_cost_search_ is less time expensive by a factor of 2 than _(1) breadth_first_search_, considering the plan length, both searches are optimal.

The plan provided by _(1) breadth_first_search_:
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P1, ATL, JFK)
Unload(C1, P1, JFK)
Unload(C3, P1, JFK)
Fly(P2, ORD, SFO)
Unload(C2, P2, SFO)
Unload(C4, P2, SFO)
```

The plan provided by _(5) uniform_cost_search_
```
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)x
Fly(P1, ATL, JFK)
Unload(C1, P1, JFK)
Fly(P2, ORD, SFO)
Unload(C2, P2, SFO)
Unload(C3, P1, JFK)
Unload(C4, P2, SFO)

```

### Domain-independent heuristic A* results

#### Problem 1

| Search    | Expansions | Goal Tests | New Nodes | Plan Length | Execution (s) |
| --------- | ---------- | ---------- | --------- | ----------- | ------------- |
| 8. A*     | 55         | 57         | 224       | 6           | 0.039192      |
| 9. A* IP  | 41         | 43         | 170       | 6           | 0.031476      |
| 10. A* LS | 11         | 13         | 50        | 6           | 0.405618      |

All three searches are optimal in terms of plan lenght and execution time, but choosing _(10) A* LS astar_search h_pg_levelsum_ makes the difference in terms of expansion, this could be misleading as the problem isn't big enough to demonstrate the real performance of these searches.

Plan provided by _(10) A* LS astar_search h_pg_levelsum_:
```
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C1, P1, JFK)
Unload(C2, P2, SFO)
```

\newpage

#### Problem 2

| Search    | Expansions | Goal Tests | New Nodes | Plan Length | Execution (s) |
| --------- | ---------- | ---------- | --------- | ----------- | ------------- |
| 8. A*     | 4605       | 4607       | 41839     | 9           | 12.411097     |
| 9. A* IP  | 1311       | 1313       | 11989     | 9           | 3.685396      |
| 10. A* LS | 74         | 76         | 720       | 9           | 31.601187     |

For problem 2 _(9) A* IP astar_search h_ignore_preconditions_ performs better in terms of expansions and execution time, other two searches are optimal in terms of plan length and uses less node expansions but time execution is inefficient.

Plan provided by _(9) A* IP astar_search h_ignore_preconditions_:
```
Load(C1, P1, SFO)
Fly(P1, SFO, JFK)
Unload(C1, P1, JFK)
Load(C2, P2, JFK)
Fly(P2, JFK, SFO)
Unload(C2, P2, SFO)
Load(C3, P3, ATL)
Fly(P3, ATL, SFO)
Unload(C3, P3, SFO)
```

#### Problem 3

| Search    | Expansions | Goal Tests | New Nodes | Plan Length | Execution (s) |
| --------- | ---------- | ---------- | --------- | ----------- | ------------- |
| 8. A*     | 16961      | 16963      | 149117    | 12          | 53.613295     |
| 9. A* IP  | 4444       | 4446       | 39227     | 12          | 14.640858     |
| 10. A* LS | 229        | 231        | 2081      | 13          | 128.400390    |

The _(9) A* IP astar_search h_ignore_preconditions_ search is the most optimal in terms of expansions, plan lenght and execution time.

Plan provided by _(9) A* IP astar_search h_ignore_preconditions_:
```
Load(C1, P1, SFO)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P1, ATL, JFK)
Unload(C3, P1, JFK)
Unload(C1, P1, JFK)
Load(C2, P2, JFK)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P2, ORD, SFO)
Unload(C4, P2, SFO)
Unload(C2, P2, SFO)
```

### Overall Analysis

For uninformed searches, both _(1) breadth_first_search_ and _(5) uniform_cost_search_ are optimal for problem 1 and 2, the time difference is practically none but they differ in node expansions, for problem 3, _(5) uniform_cost_search_ is the most optimal as it cuts the time by a factor of two although it requires almost the same expansions. The suggestion is to use _(5) uniform_cost_search_ as a general solution for these three problems as it behaves consistently independently of the complexity of the problem, but for other problems, the searches need to be chosen case by case.

The uniform cost search behaves almost the same as the breadth first search, this is a property when all the cost are equals[^2], but the node expansion is slightly more considering that the search explores the three searching the goal with the lowest cost visiting more nodes whereas breadth first stops as soon the goal is found. What this means is in principle the uniform cost execution time, in this case, should not be less than the breadth first search[^3], in this case, there are three possible reasons why the uniform cost search is better in terms of time execution:

1. there is an implementation error in the search algorithm
2. the uniform cost search is implemented to be more efficient or breadth first search is poorly implemented in terms of efficiency
3. a problem in one of the in-house developed libraries used

After tracing the root of the cause, a change[^4] to the _PriorityQueue_ in _aimacode/utils.py_ the module might seem to trigger the difference

Before the change:
```
Solving Air Cargo Problem 3 using uniform_cost_search...

Expansions   Goal Tests   New Nodes
  16961       16963       149117  

Plan length: 12  Time elapsed in seconds: 374.1983297660008
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P1, ATL, JFK)
Unload(C1, P1, JFK)
Fly(P2, ORD, SFO)
Unload(C2, P2, SFO)
Unload(C3, P1, JFK)
Unload(C4, P2, SFO)
```

After the change:
```
Solving Air Cargo Problem 3 using uniform_cost_search...

Expansions   Goal Tests   New Nodes
  16961       16963       149117  

Plan length: 12  Time elapsed in seconds: 52.024249959999
Load(C1, P1, SFO)
Load(C2, P2, JFK)
Fly(P1, SFO, ATL)
Load(C3, P1, ATL)
Fly(P2, JFK, ORD)
Load(C4, P2, ORD)
Fly(P1, ATL, JFK)
Unload(C1, P1, JFK)
Fly(P2, ORD, SFO)
Unload(C2, P2, SFO)
Unload(C3, P1, JFK)
Unload(C4, P2, SFO)
```

This could be an implementation problem, due time constraints, the analysis was stick to the algorithms rather than finding the root issue, this was reported in one of the course forums[^5].

The heuristic based search, _(9) A* IP astar_search h_ignore_preconditions_, problem 1 doesn't say too much, but problem 2 the time is improved significantly using fewer expansions, one could argue that _(10) A* LS astar_search h_pg_levelsum_ can be treated as optimal as well based on the expansions, but _(9) A* IP astar_search h_ignore_preconditions_ takes 3 seconds whereas _(10)_ takes 31.

We can see clearly that _(9) A* IP astar_search h_ignore_preconditions_ behaves consistently for all these tree problems in terms of expansion and time execution independently of the complexity of the problem, this is because the level sum heuristic needs to navigate the graph to compute the level cost for each goal whereas the _Ignore Preconditions_ heuristics ignore the preconditions computing only the number of not satisfied goals from the current state without exploring the graph [^6].

## Conclusion

Optimality, completeness[^7], expansion and time execution are key indicators to find the right search algorithm for a very specific plan. Even though some algorithms behave similarly for different problems - it really depends on the problem nature which algorithm to use.

Uniformed searches are good enough when the problem is not big enough in terms of complexity and if one may want to sacrifice space and time in favor of having a naive approach of the solution.

For the more complex problem, independent domain heuristics can achieve better time performance compared to the uninformed search, this is due the heuristic is basically a hint for the algorithm which path or node need to expand further whereas uninformed need to explore the graph.