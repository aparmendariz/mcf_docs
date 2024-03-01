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
