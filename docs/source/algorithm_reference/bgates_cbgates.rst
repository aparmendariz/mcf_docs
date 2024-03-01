CBGATEs and BGATEs
==================

Balanced Group Average Treatment Effects (:math:`\textrm{BGATE's}`) and Causal Balanced Group Average Treatment Effects (:math:`\textrm{CBGATE's}`) have been introduced by `Bearth & Lechner (2024) <https://browse.arxiv.org/abs/2401.08290>`_.

The :math:`\textrm{BGATE}` can be used to estimate :math:`\textrm{ATE's}` for different groups (:math:`\textrm{GATE's}`), while accounting for differences in other covariates, i.e.

.. math::
   BGATE(m,l;x) = \mathbb{E} \bigg[ \mathbb{E} \big[ Y^1 - Y^0 \big\vert Z=z, W=w \big]\bigg]

Here, :math:`Z` is a single feature of :math:`X` and :math:`W` denotes a subgroup of features of :math:`X` excluding :math:`Z`. :math:`z` is a possible value of the variable of interest :math:`Z`. 

The :math:`\textrm{BGATE}` partially overcomes the attribution problem related to a simple :math:`\textrm{GATE}`, where other relevant variables may confound effect heterogeneity.
Furthermore, the Causal Balanced Group Average Treatment Effect (:math:`\textrm{CBGATE}`) makes a causal interpretation of the :math:`\textrm{BGATE}` possible, when all variables other than the heterogeneity variable :math:`Z` are balanced and further asssumptions discussed in `Bearth & Lechner (2024) <https://browse.arxiv.org/abs/2401.08290>`_ hold. Hence, both :math:`\textrm{CBGATE}` and the plain-vanilla :math:`\textrm{GATE}` are limiting cases of the :math:`\textrm{BGATE}`.

Algorithmically, the :math:`\textrm{BGATE}` and the :math:`\textrm{CBGATE}` are implemented as follows:

1. Draw a random sample from the prediction data.
2. Keep the heterogeneity and balancing variables.
3. Replicate the data from step 2 :math:`n_z` times, where :math:`n_z` denotes the cardinality of the heterogeneity variable of interest. In each :math:`n_z` fold, set :math:`Z` to a specific value.
4. Draw the nearest neighbours of each observation in the prediction data in terms of the balancing variables and the heterogeneity variable. If there is a tie, the algorithm chooses one randomly.
5. Form a new sample with all selected neighbours.
6. Compute :math:`\textrm{GATE's}` and their standard errors.

One should note that this procedure only happens in the prediction part using the previously trained forest. This implementation differs from `Bearth & Lechner (2024) <https://browse.arxiv.org/abs/2401.08290>`_ estimation approach. They use double/debiased machine learning to estimate the parameters of interest.

To turn on the :math:`\textrm{BGATE}` , set ``p_bgate`` to True. To turn on the :math:`\textrm{CBGATE}`, set ``p_cbgate`` to True. The balancing variables :math:`W` have to be specified in ``var_bgate_name``.


Below you find a list of the main parameters which are related to the :math:`\textrm{BGATE's} and :math:`\textrm{CBGATE's}. Please consult the :py:class:`API <mcf_functions.ModifiedCausalForest>` for more details or additional parameters. 

.. list-table:: 
   :widths: 30 70
   :header-rows: 1

   * - Parameter
     - Description
   * - ``var_bgate_name``
     - This parameter is a string or a list of strings that specifies the variables to balance the GATEs on. It's only relevant if p_bgate is True. The distribution of these variables is kept constant when a BGATE is computed. If set to None, the other heterogeneity variables (var_z_ …) are used for balancing. The default value is None.
   * - ``p_bgate``
     - This parameter enables the estimation of a GATE that is balanced in selected features, as specified in var_bgate_name. The default value is False.
   * - ``p_cbgate``
     - This parameter enables the estimation of a GATE that is balanced in all other features. The default value is False.
   * - ``p_bgate_sample_share``
     - This parameter determines the method of nearest neighbour matching. If set to True, prognostic scores are used. If set to False, the inverse of the covariance matrix of features is used. The default value is True.
   * - ``p_gate_no_evalu_points``
     - This parameter is an integer that determines the number of evaluation points for discretized variables in (C)BGATE estimation. The default value is 50.
   * - ``p_bgate_sample_share``
     - This parameter is used to speed up the program as the implementation of (C)BGATE estimation is very CPU intensive. Therefore, random samples are used if the number of observations / number of evaluation points > 10. If the number of observations in prediction data (n) is less than 1000, the value is 1. If n is greater than or equal to 1000, the value is None. The default value is None.


Example
~~~~~~~

.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"],
        # De
        var_z_name_list=["age"],
        # De
        var_bgate_name=, 
        # De
        p_bgate=True,  
        # Det
        p_bgate_sample_share = True, 
        # Det
        p_gate_no_evalu_points, 
        # Det
        p_bgate_sample_share
    )


.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"],
        # De
        var_bgate_name
        var_z_name_list=["age"],
        # De
        p_cbgate=True 
        # Det
        cf_match_nn_prog_score = True
    )

