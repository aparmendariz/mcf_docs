(Causal) balanced group average treatment effects - (C)BGATEs
=============================================================

-> former arguments now renamed to p_bgate

- ``p_gmate_no_evalu_points`` --> ``p_gate_no_evalu_points``
- ``p_gmate_sample_share`` --> ``p_bgate_sample_share``

+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_gmate_no_evalu_points <./mcf_api.md#p_gmate_no_evalu_points>` | Number of evaluation points for marginal treatment effects. The default is 50.                                |                   
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_gmate_sample_share <./mcf_api.md#p_gmate_sample_share>` | Number in the interval $(0,1]$ determining the size of $N_{SS}$ for the computation of AMTEs. Note that $N_{SS}$ also depends on the number of evaluation points. |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+


CBGATEs and BGATEs
==================

Causal balanced group average treatment effects (CBGATEs) and balanced group average treatment effects (BGATEs) have been introduced by Bearth and Lechner (2024).

The CBGATE is comparing the treatment effects for two groups of the heterogeneity variable of interest, while accounting for differences in other covariates, i.e.

.. math::

   CBGATE(m,l;x) = \mathbb{E} \bigg[ \mathbb{E} \big[ IATE(m,l;x) \big\vert X^p=u, X^{-p}=x^{-p} \big]  \\ - \mathbb{E} \big[IATE(m,l;x) \big\vert X^p=v, X^{-p}=x^{-p} \big] \bigg]

Here, :math:`p` is a single feature of :math:`X` and :math:`X^{-p}` denotes the remaining features of :math:`X` without :math:`p`. :math:`p` and :math:`u` are two possible values of the variable of interest :math:`X^p`. 

Hence, the CBGATE overcomes the causal attribution problem related to a simple GATE, where other relevant variables may confound effect heterogeneity. Bearth and Lechner (2024) discuss the assumptions required for a causal interpretation.

The balanced group average treatment effect (BGATE) relaxes the CBGATE in the sense that only a subset of the variables in the computation of the pseudo-derivative is balanced. Hence, both CBGATE and the plain-vanilla GATE are limiting cases of the BGATE.

Algorithmically, the BGATE and the CBGATE are implemented as follows:

1. Draw a random sample from the prediction data.
2. Keep the heterogeneity and balancing variables.
3. Replicate the data from step 2 :math:`n_z` times, where :math:`n_z` denotes the cardinality of the heterogeneity variable of interest. In each :math:`n_z` fold, set :math:`z` to a specific value.
4. Draw the nearest neighbours of each observation in the prediction data in terms of the balancing variables and the heterogeneity variable. If there is a tie, the algorithm chooses one randomly.
5. Form a new sample with all selected neighbours.
6. Compute GATEs and their standard errors.

This implementation differs from Bearth and Lechner's (2024) estimation approach. They use double/debiased machine learning to estimate the parameters of interest.

To turn on the CBGATE, set ``p_cbgate`` to True. To turn on the BGATE, set ``p_bgate`` to True.
