Policy Tree algorithm
=====================

You may choose between two methods in determining policy allocation:

- Policy Tree: This method follows `Zhou, Athey, and Wager (2022) <https://doi.org/10.1287/opre.2022.2271>`_ . To opt for this method, set ``gen_method`` or ``policy tree``.

- Blackbox Rule: This method follows the logic of allocating the treatment, which implies the best potential outcome (potentially taking estimation uncertainty into account if passed over to the program via ``var_effect_vs_0_se``). 

Optimal Policy Tree
-------------------

In what follows, we briefly explain the solution method for finding the optimal policy tree.

A Primer
-----------

The optpoltree function is designed to discover the optimal policy tree in a computationally cheap and tractable manner. While the basic logic follows `Zhou, Athey, and Wager (2022) <https://doi.org/10.1287/opre.2022.2271>`_ , the details of the programmatic implementation differ. 
For instance, in contrast to policytree, the optpoltree allows you to consider constraints in terms of the maximal shares of treated and to detail treatment costs as well as using different policy scores.


Algorithmic Implementation
-----------------------------

The optpoltree function explores the space of all viable policy trees and picks the optimal one, i.e. the one which maximizes the value function, i.e. the sum of all individual-specific policy scores, by assigning one treatment to all observations in a specific terminal node. 

The algorithmic idea is immediate. Given a fixed choice of previous partitions, the problem of finding an optimal solution simplifies to solving two subproblems: 

- find an optimal left and right subtree. Once, we have reached a terminal node, i.e. we are no longer permitted to perform splits of the feature space, the treatment is chosen, which maximises the score of all observations in the respective leaf. This train-of-thought motivates a recursive algorithm as the overall problem naturally disaggregates into smaller and easier subproblems, which feed into the overall solution. 

The tree-search procedure is outlined in the subsequent pseudocode Algorithm: Tree-search Exact.

Notation
----------------------------

Before we delve into the solution method for finding the optimal policy tree, let's introduce some notation:

- :math:`i=1, \ldots, n`: There are :math:`n` observations.
- :math:`p_1`: The number of ordered features observed.
- :math:`p_2`: The number of unordered features observed.
- :math:`M`: The number of distinct treatments.
- :math:`\hat{\Theta}_i`: The vector where estimated policy scores, the potential outcomes, for the :math:`M+1` distinct potential outcomes are stacked for each observation :math:`i`.
- :math:`\hat{\Theta}_i(d)`: The potential outcome for observation :math:`i` for treatment :math:`d`.
- :math:`L`: The depth of the tree, which equals the number of splitting nodes plus one.

With this notation in place, we can now describe the Tree-Search Exact algorithm.


Tree-search Exact Algorithm
-----------------------------

The Tree-search Exact algorithm can be described as follows:

1. If :math:`L = 1`:
   - Choose :math:`j^* \in \{0, 1, \ldots, M\}`, which maximizes :math:`\sum \hat{\Theta}_i(j)` and return the corresponding reward = :math:`\sum_{\forall i} \hat{\Theta}_i(j^*)`.

2. Else:
   - Initialize reward = :math:`-\infty`, and an empty tree = :math:`\emptyset` for all :math:`m = 1, \ldots, p_1 + p_2`.
   - Pick the m-th feature; for ordered features return the unique values observed and sorted; if unordered return the unique categories to derive all         
     possible splits.
     - Then, for all possible splitting values of the m-th feature split the sample accordingly into a sample_left and sample_right.
     - (reward_left, tree_left) = Tree-search(sample_left, L-1).
     - (reward_right, tree_right) = Tree-search(sample_right, L-1).
   - If reward_left + reward_right > reward:
     - reward = reward_left + reward_right.
     - tree = Tree-search(m, splitting value, tree_left, tree_right).


Options for Optimal Policy Tree
-----------------------------------

The optimal policy tree comes with several options:

- Minimum Observations in a Partition: To control how many observations are required at minimum in a partition, inject a number into ``pt_min_leaf_size``.

- Admissible Treatment Shares: If the number of individuals who receive a specific treatment is constrained, you may specify admissible treatment shares via the keyword argument ``other_max_shares``. Note that the information must come as a tuple with as many entries as there are treatments.

- Treatment Costs: If costs of the respective treatment(s) are relevant, you may input ``other_costs_of_treat``. When evaluating the reward, the aggregate costs (costs per unit times units) of the policy allocation are subtracted. If you leave the costs to their default, ``None``, the program determines a cost vector that imply an optimal reward (policy score minus costs) for each individual, while guaranteeing that the restrictions as specified in ``other_max_shares`` are satisfied. This is of course only relevant when ``other_max_shares`` is specified.

- Cost Multiplier: If there are restrictions, and ``other_costs_of_treat`` is left to its default, the ``other_costs_of_treat_mult`` can be specified. Admissible values are either a scalar greater zero or a tuple with values greater zero. The tuple needs as many entries as there are treatments. The imputed cost vector is then multiplied by this factor.


.. list-table:: Optimal Policy Tree Options
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Details
   * - var_effect_vs_0
     - Specifies effects relative to the default treatment zero.
   * - var_effect_vs_0_se
     - Specifies standard errors of the effects given in var_effect_vs_0.
   * - other_max_shares
     - Specifies maximum shares of treated for each policy.
   * - other_costs_of_treat_mult
     - Specifies a multiplier to costs; valid values range from 0 to 1; the default is 1. Note that parameter is only relevant if other_costs_of_treat is set to its default None.
   * - other_costs_of_treat
     - Specifies costs per unit of treatment. Costs will be subtracted from policy scores; 0 is no costs; the default is None, which implies 0 costs if there are no constraints. Accordingly, the program determines individually best treatments fulfilling the restrictions in other_max_shares and implying the smallest possible costs.
   * - pt_min_leaf_size
     - Specifies minimum leaf size; the default is the integer part of 10% of the sample size divided by the number of leaves.
   * - pt_depth
     - Regulates depth of the policy tree; the default is 3; the programme accepts any number strictly greater 0.
   * - pt_no_of_evalupoints
     - Implicitly set the approximation parameter of Zhou, Athey, and Wager (2022) - :math:`A`. Accordingly, :math:`A=N/n_{evalupoints}`, where :math:`N` is the number of observations and :math:`n_{evalupoints}` the number of evaluation points; default value is 100.

Example
---------



Speed Considerations
----------------------------------

You can control aspects of the algorithm, which impact running time:

- Number of Evaluation Points: Specify the number of evaluation points via ``pt_no_of_evalupoints``. This regulates when performing the tree search how many of the possible splits in the feature space are considered. If the ``pt_no_of_evalupoints`` is smaller than the number of distinct values of a certain feature, the algorithm visits fewer splits, thus increasing computational efficiency.

- Tree Depth: Specify the admissible depth of the tree via the keyword argument ``pt_depth``.

- Parallel Execution: Run the program in parallel. You can set the number of processes via the keyword argument ``_int_how_many_parallel``. By default, the number is set equal to the 80 percent of the number of logical cores on your machine.

- Numba Optimization: A further speed up is accomplished through Numba. Numba is a Python library, which translates Python functions to optimized machine code at runtime. By default, the program uses Numba. To disable Numba, set ``_int_with_numba`` to False.


.. list-table:: Algorithm Control Options
   :widths: 30 70
   :header-rows: 1

   * - Keyword
     - Details
   * - _int_parallel_processing
     - If True, the program is run in parallel with the number of processes equal to _int_how_many_parallel. If False, the program is run on one core; the default is True.
   * - _int_how_many_parallel
     - Specifies the number of parallel processes; the default number of processes is set equal to the logical number of cores of the machine.
   * - _int_with_numba
     - Specifies if Numba is deployed to speed up computation time; the default is True.


Example
---------



Changes concerning the class OptimalPolicy
-------------------------------------------------

Change of  names of keywords (to use the same names as in the ModifiedCausalForest class)

var_x_ord_name –> var_x_name_ord

var_x_unord_name –> var_x_name_unord

Change of default values

The default of pt_enforce_restriction is set to False.

The previous default of pt_min_leaf_size is now multiplied by the smallest allowed treatment if (and only if) treatment shares are restricted.

“policy tree eff” becomes the standard method for policy trees and is renamed as “policy tree”.

Change of default value for gen_variable_importance. New default is True.

There are several changes to speed up the computation of policy trees.

New keyword: _int_xtr_parallel Parallelize to a larger degree to make sure all CPUs are busy for most of the time. Only used for “policy tree” and only used if _int_parallel_processing > 1 (or None). Default is True.

There is the new option to build a new optimal policy trees based on the data in each leaf of the (first) optimal policy tree. Although this second tree will also be optimal, the combined tree is no longer optimal. The advantage is a huge speed increase, i.e. a 3+1 tree computes much, much faster than a 4+0 tree, etc. This increased capabilities require a change in keywords:

Deleted keyword: pt_depth_tree

New keywords

pt_depth_tree_1 Depth of 1st optimal tree. Default is 3.

pt_depth_tree_2 Depth of 2nd optimal tree. This tree is build within the strata obtained from the leaves of the first tree. If set to 0, a second tree is not build. Default is 1. Using both defaults leads to a (not optimal) total tree of level of 4.
