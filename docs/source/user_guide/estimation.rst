Estimation of treatment effects
===============================

Different types of treatment effects
------------------------------------

The Modified Causal Forest estimates three types of treatment effects, which differ in their aggregation level and are discussed in depth by `Lechner (2019) <https://doi.org/10.48550/arXiv.1812.09487>`_. These effects are the average treatment effect (:math:`\textrm{ATE}`), the group average treatment effect (:math:`\textrm{GATE}`), and the individualized average treatment effect (:math:`\textrm{IATE}`).

Let us consider a discrete, multi-valued treatment :math:`D`. The potential outcome of treatment state :math:`d` is denoted by :math:`Y^d`. The covariates are denoted by :math:`X` and :math:`Z \subset X` is a vector of features with "few values" that typically define population groups (e.g. age groups, gender, etc.). The effects of interest are then defined as:

.. math::

    \textrm{ATE}(m,l;\Delta) &:= \mathbb{E} \big[ Y^m-Y^l \big\vert D\in \Delta \big]

    \textrm{GATE}(m,l;z,\Delta) &:= \mathbb{E} \big[ Y^m-Y^l \big\vert Z=z, D\in \Delta \big]

    \textrm{IATE}(m,l;x) &:= \mathbb{E} \big[ Y^m-Y^l \big\vert X=x \big]

If :math:`\Delta = \{m\}` then :math:`\textrm{ATE}(m,l;\Delta)` is better known as the average treatment effect on the treated (:math:`\textrm{ATET}`) for the individuals that received treatment :math:`m`.

:math:`\textrm{ATE's}` measure the average impact of treatment :math:`m` compared to treatment :math:`l` either for the entire population, or in case of an :math:`\textrm{ATET}`, for the units that actually received a specific treatment. 

Whereas :math:`\textrm{ATE's}` are population averages, :math:`\textrm{IATE's}` are average effects at the finest possible aggregation level. They measure the average impact of treatment :math:`m` compared to treatment :math:`l` for units with features :math:`X = x`. :math:`\textrm{GATE's}` lie somewhere in-between these two extremes. They measure the average impact of treatment :math:`m` compared to treatment :math:`l` for units in group :math:`Z = z`. :math:`\textrm{GATE's}` and :math:`\textrm{IATES's}` are special cases of the so-called conditional average treatment effects (:math:`\textrm{CATE's}`).

A recent paper by `Bearth & Lechner (2024) <https://browse.arxiv.org/abs/2401.08290>`_ introduced the Balanced Group Average Treatment Effect (:math:`\textrm{BGATE}`). Click :doc:`here </algorithm_reference/bgates_cbgates>` to learn more about estimating :math:`\textrm{BGATE's}` with the Modified Causal Forest.

Estimating ATE's / IATE's 
----------------------------------

The :math:`\textrm{ATE's}` as well as the :math:`\textrm{IATE's}` are estimated by default through the :py:meth:`~mcf_functions.ModifiedCausalForest.predict` method of the class :py:class:`~mcf_functions.ModifiedCausalForest`. See :doc:`../getting_started` for a quick example on how to access these estimates.

Another way to access the estimated :math:`\textrm{ATE's}` is through the output folder that the **mcf** package generates once a Modified Causal Forest is initialized. You can find the location of this folder by accessing the `outpath` entry of the `gen_dict` attribute of your Modified Causal Forest:

.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"]
    )
    my_mcf.gen_dict["outpath"]

You can also specify this path through the ``gen_outpath`` parameter of the class :py:meth:`~mcf_functions.ModifiedCausalForest`. The output folder will contain csv-files with the estimated :math:`\textrm{ATE's}` in the subfolder `ate_iate`.

You can control whether :math:`\textrm{IATE's}` and their standard errors are estimated by setting the parameters ``p_iate`` and ``p_iate_se`` of the class :py:class:`~mcf_functions.ModifiedCausalForest` to True or False:

+---------------+-----------------------------------------------------------------------+
| Parameter     | Description                                                           |
+---------------+-----------------------------------------------------------------------+
| ``p_iate``    | If True, IATE's will be estimated. Default: True.                     |
+---------------+-----------------------------------------------------------------------+
| ``p_iate_se`` | If True, standard errors of IATE's will be estimated. Default: False. |
+---------------+-----------------------------------------------------------------------+

Example
~~~~~~~

.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"],
        # Estimate IATE's but not their standard errors
        p_iate = True,
        p_iate_se = False
    )


Estimating ATET's
----------------------------------

The average treatment effects for the treated are estimated by the :py:meth:`~mcf_functions.ModifiedCausalForest.predict` method if the parameter ``p_atet`` of the class :py:class:`~mcf_functions.ModifiedCausalForest` is set to True:

.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"],
        # Estimating ATET's
        p_atet = True
    )
    my_mcf.train(my_data)

The :math:`\textrm{ATET's}` are, similar to the :math:`\textrm{ATE's}`, stored in the `"ate"` entry of the dictionary returned by the :py:meth:`~mcf_functions.ModifiedCausalForest.predict` method. This entry will then contain both the estimated :math:`\textrm{ATET's}` as well as the :math:`\textrm{ATE's}`. The output that is printed to the console during prediction will present you a table with all estimated :math:`\textrm{ATE's}` and :math:`\textrm{ATET's}`, which should give you a good idea of the structure of the `"ate"` entry in the result dictionary.

.. code-block:: python

    results = my_mcf.predict(my_data)
    results["ate"]

The standard errors of the estimates are stored in the `"ate_se"` entry of the same dictionary. The structure of the `"ate_se"` entry is analogous to the `"ate"` entry. 

.. code-block:: python

    results["ate_se"]


Estimating GATE's
-----------------
or `p_gatet <./mcf_api.md#p_gatet>`_ are set to *True*.
-> mention effects for the treatment here as well.

The effects for the treated are computed if the input arguments `p_atet <./mcf_api.md#p_atet>`_ or `p_gatet <./mcf_api.md#p_gatet>`_ are set to *True*.

By default, the program smooths the distribution of the GATEs for continuous features. A smoothing procedure evaluates the effects at a local neighborhood around a pre-defined number of evaluation points. The flag `p_gates_smooth <./mcf_api.md#p_gates_smooth>`_ activates this procedure. The level of discretization depends on the number of evaluation points, which can be defined in `p_gates_smooth_no_evalu_points <./mcf_api.md#p_gates_smooth_no_evalu_points>`_. The local neighborhood is based on an Epanechnikov kernel estimation using Silverman's bandwidth rule. The keyword argument `p_gates_smooth_bandwidth <./mcf_api.md#p_gates_smooth_bandwidth>`_ specifies a multiplier for Silverman's bandwidth rule. In addition, it discretizes continuous features and computes the GATEs for those discrete approximations.

Stabilizing estimates of effects by truncating weights
------------------------------------------------------

To obtain stable estimates, the program provides the option to truncate estimated forest weights to an upper threshold. After truncation, the program renormalizes the weights for estimation. Because of the renormalization step, the final weights can be slightly above the threshold defined in `p_max_weight_share <./mcf_api.md#p_max_weight_share>`_.


Input arguments for estimations of treatment effects
----------------------------------------------------

+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| Arguments                                     | Description                                                                                                                      |
+===============================================+==================================================================================================================================+
| `p_gates_smooth <./mcf_api.md#p_gates_smooth>`| Flag for smoothing the distribution of the estimated GATEs for continuous features. The default is True.                        |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_gates_smooth_no_evalu_points <./mcf_api.md#p_gates_smooth_no_evalu_points>` | Number of evaluation points for GATEs. The default is 50.                                                                       |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_gates_smooth_bandwidth <./mcf_api.md#p_gates_smooth_bandwidth>` | Multiplier for Silverman's bandwidth rule for GATEs. The default is 1.                                                         |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_atet <./mcf_api.md#p_atet>` | If *True*, average treatment effects for subpopulations defined by treatment status are computed. This only works if at least one GATE feature is specified. The default is *False*. |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_gatet <./mcf_api.md#p_gatet>` | If *True*, group average treatment effects for subpopulations defined by treatment status are computed. The default is *False*. |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_max_weight_share <./mcf_api.md#p_max_weight_share>` | Maximum value of the weights. The default is 0.05.                                                                              |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| `p_gates_minus_previous <./mcf_api.md#p_gates_minus_previous>` | If set to True, GATES will be compared to GATEs computed at the previous evaluation point. GATE estimation is a bit slower as it is not optimized for multiprocessing. No plots are shown. Default is False. |
+-----------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
