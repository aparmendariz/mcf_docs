Policy Tree algorithm
=====================

To determine the policy allocation, you may choose between two methods:

- Policy Tree: This method follows `Zhou, Athey, and Wager (2022) <https://doi.org/10.1287/opre.2022.2271>`_ . To opt for this method, set ``gen_method`` or ``policy tree``.

- Blackbox Rule: This method follows the logic of allocating the treatment, which implies the best potential outcome (potentially taking estimation uncertainty into account if ``var_effect_vs_0_se`` is used). 

Optimal Policy Tree
-------------------

The :py:class:`~optpolicy_functions.OptimalPolicy` class is designed to discover the optimal policy tree in a computationally cheap and tractable manner. While the basic logic follows `Zhou, Athey, and Wager (2022) <https://doi.org/10.1287/opre.2022.2271>`_ , the details of the programmatic implementation differ. 
For instance, in contrast to policytree, the optpoltree allows you to consider constraints regarding the maximal shares of treated observations, detail treatment costs and using different policy scores.


Implementation
-----------------------------

The :py:class:`~optpolicy_functions.OptimalPolicy` class explores the space of all viable policy trees and picks the optimal one. This optimal tree maximizes the value function, computed as the sum of individual-specific policy scores, by assigning treatments to observations within terminal nodes.

Given a fixed choice of previous partitions, the problem of finding an optimal solution simplifies to solving two subproblems: 

- finding optimal left and right subtrees. 

Once we have reached a terminal node, we are no longer allowed to perform splits of the feature space and the treatment which maximises the score of all observations in the respective leaf is chosen. 

This recursive approach breaks down the problem into smaller, more manageable subproblems, facilitating the overall solution.


Notation
----------------------------

Before we delve into the solution method for finding the optimal policy tree (Tree-search Exact Algorithm), let's introduce some notation:

- :math:`i=1, \ldots, n`: are :math:`n` observations
- :math:`p_1`: number of ordered features 
- :math:`p_2`: number of unordered features
- :math:`M`: number of treatments
- :math:`\hat{\Theta}_i`: vector of estimated policy scores, the potential outcomes, for the :math:`M+1` distinct potential outcomes are stacked for each observation :math:`i`.
- :math:`\hat{\Theta}_i(d)`: potential outcome for observation :math:`i` for treatment :math:`d`.
- :math:`L`: depth of the tree, which equals the number of splitting nodes plus one.

With this notation, we can now describe the Tree-Search Exact algorithm.


Tree-search Exact Algorithm
-----------------------------

Tree-search Exact Algorithm
===========================

The Tree-search Exact algorithm can be described as follows:

1. If :math:`L = 1`:

   - Choose :math:`j^* \in \{0, 1, \ldots, M\}`, which maximizes :math:`\sum_i \hat{\Theta}_i(j)` and return the corresponding reward = :math:`\sum_{\forall i} \hat{\Theta}_i(j^*)`.

2. Else:

   - Initialize reward = :math:`-\infty`, and an empty tree = :math:`\emptyset` for all :math:`m = 1, \ldots, p_1 + p_2`.

   - Pick the m-th feature; for ordered features return the unique values observed and sorted; if unordered return the unique categories to derive all possible splits.

   - Then, for all possible splitting values of the m-th feature split the sample accordingly into a sample_left and sample_right.

   - :math:`(\text{reward\_left}, \text{tree\_left}) = \text{Tree-search}(\text{sample\_left}, L-1)`.

   - :math:`(\text{reward\_right}, \text{tree\_right}) = \text{Tree-search}(\text{sample\_right}, L-1)`.

   - If :math:`\text{reward\_left} + \text{reward\_right} > \text{reward}`:
     - :math:`\text{reward} = \text{reward\_left} + \text{reward\_right}`.
     - :math:`\text{tree} = \text{Tree-search}(m, \text{splitting value}, \text{tree\_left}, \text{tree\_right})`.


Options for Optimal Policy Tree
-----------------------------------

You can personalize various parameters defined in the :py:class:`~optpolicy_functions.OptimalPolicy` class. 

When considering treatment costs, input them via `other_costs_of_treat`.  When evaluating the reward, the aggregate costs (costs per unit times units) of the policy allocation are subtracted. If left as default (None), the program determines a cost vector that imply an optimal reward (policy score minus costs) for each individual, while guaranteeing that the restrictions as specified in ``other_max_shares`` are satisfied. This is of course only relevant when ``other_max_shares`` is specified.

Alternatively, if restrictions are present and `other_costs_of_treat` is default, you can specify `other_costs_of_treat_mult`. Admissible values for this parameter are either a scalar greater zero or a tuple with values greater zero. The tuple needs as many entries as there are treatments. The imputed cost vector is then multiplied by this factor.


.. list-table:: 
   :widths: 25 75
   :header-rows: 1

   * - Keyword
     - Details
   * - ``var_effect_vs_0_se``
     - Variables of effects of treatment relative to first treatment. Dimension is equal to the number of treatments minus 1. Default is None.
   * - ``pt_min_leaf_size``
     - Minimum leaf size. Leaves that are smaller will not be considered. A larger number reduces computation time and avoids some overfitting. Only relevant if ``gen_method`` is ``policy tree`` or ``policy tree old``. Default is None.
   * - ``other_max_shares``
     - Maximum share allowed for each treatment. Note that the information must come as a tuple with as many entries as there are treatments. Default is None.
   * - ``other_costs_of_treat``
     - Treatment specific costs. Subtracted from policy scores. None (when there are no constraints): 0 None (when are constraints): Costs will be automatically determined such as to enforce constraints in the training data by finding cost values that lead to an allocation (``best_policy_score``) that fulfils restrictions ``other_max_shares``. Default is None.
   * - ``other_costs_of_treat_mult``
     - Multiplier of automatically determined cost values. Use only when automatic costs violate the constraints given by ``other_max_shares``. This allows to increase (>1) or decrease (<1) the share of treated in particular treatment. Default is None.

Please consult the :py:class:`API <mcf_functions.ModifiedCausalForest>` for more details or additional parameters. 


Example
---------

.. code-block:: python

   my_policy_tree = OptimalPolicy(
       var_d_name="d",
       var_polscore_name=["Y_LC0_un_lc_pot", "Y_LC1_un_lc_pot", "Y_LC2_un_lc_pot"],
       var_x_name_ord=["x1", "x2"],
       var_x_name_unord=["female"],
       gen_method="policy tree",
       pt_depth_tree_1=2
       )


Speed Considerations
----------------------------------

You can control aspects of the algorithm, which impact running time:

- Number of evaluation points: Specify the number of evaluation points via ``pt_no_of_evalupoints``. This regulates when performing the tree search how many of the possible splits in the feature space are considered. If the ``pt_no_of_evalupoints`` is smaller than the number of distinct values of a certain feature, the algorithm visits fewer splits, thus increasing computational efficiency.

- Tree depth: Specify the admissible depth of the tree via the keyword argument ``pt_depth_tree_1`` or ``pt_depth_tree_2``.

- Parallel execution: Run the program in parallel. You can set the number of processes via the keyword argument ``_int_how_many_parallel``. By default, the number is set equal to the 80 percent of the number of logical cores on your machine.

- Numba optimization: A further speed up is accomplished through Numba. Numba is a Python library, which translates Python functions to optimized machine code at runtime. By default, the program uses Numba. To disable Numba, set ``_int_with_numba`` to False.


.. list-table:: 
   :widths: 30 70
   :header-rows: 1

   * - Keyword
     - Details
   * - ``_int_parallel_processing``
     - If True, the program is run in parallel with the number of processes equal to _int_how_many_parallel. If False, the program is run on one core; the default is True.
   * - ``_int_how_many_parallel``
     - Specifies the number of parallel processes; the default number of processes is set equal to the logical number of cores of the machine.
   * - ``_int_with_numba``
     - Specifies if Numba is deployed to speed up computation time; the default is True.
   * - ``pt_depth_tree_1``
     - ; the default is True.
   * - ``pt_no_of_evalupoints``
     - Implicitly set the approximation parameter of Zhou, Athey, and Wager (2022) - :math:`A`. Accordingly, :math:`A=N/n_{evalupoints}`, where :math:`N` is the number of observations and :math:`n_{evalupoints}` the number of evaluation points; default value is 100.


Example
---------

.. code-block:: python

   my_policy_tree = OptimalPolicy(
       var_d_name="d",
       var_polscore_name=["Y_LC0_un_lc_pot", "Y_LC1_un_lc_pot", "Y_LC2_un_lc_pot"],
       var_x_name_ord=["x1", "x2"],
       var_x_name_unord=["female"],
       gen_method="policy tree",
       pt_depth_tree_1=2
       )


Changes concerning the class OptimalPolicy
-------------------------------------------------

Change of default values

The default of pt_enforce_restriction is set to False.

The previous default of pt_min_leaf_size is now multiplied by the smallest allowed treatment if (and only if) treatment shares are restricted.

“policy tree eff” becomes the standard method for policy trees and is renamed as “policy tree”.

Change of default value for gen_variable_importance. New default is True.

New keyword: _int_xtr_parallel Parallelize to a larger degree to make sure all CPUs are busy for most of the time. Only used for “policy tree” and only used if _int_parallel_processing > 1 (or None). Default is True.

There is the new option to build a new optimal policy trees based on the data in each leaf of the (first) optimal policy tree. Although this second tree will also be optimal, the combined tree is no longer optimal. The advantage is a huge speed increase, i.e. a 3+1 tree computes much, much faster than a 4+0 tree, etc. This increased capabilities require a change in keywords:

Deleted keyword: pt_depth_tree

New keywords

pt_depth_tree_1 Depth of 1st optimal tree. Default is 3.

pt_depth_tree_2 Depth of 2nd optimal tree. This tree is build within the strata obtained from the leaves of the first tree. If set to 0, a second tree is not build. Default is 1. Using both defaults leads to a (not optimal) total tree of level of 4.
