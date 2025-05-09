Experimental features
=====================

All features in this section are experimental and thus not yet fully documented and tested. Please open an issue `here <https://github.com/MCFpy/mcf/issues>`__ if you encounter any problems or have any questions.

Balancing Tests
---------------

Treatment effects may be subject to selection bias if the distribution of the confounding features differs across treatment arms. The class :py:class:`~mcf_functions.ModifiedCausalForest` provides the option to conduct balancing tests to assess whether the feature distributions are equal across treatment arms after adjustment by the Modified Causal Forest. The balancing tests are based on the estimation of average treatment effects (:math:`\text{ATE's}`) with user-specified features as outcomes. If the features are balanced across treatment arms, the estimated :math:`\text{ATE's}` should be close to zero.

The Modified Causal Forest runs balancing tests for the features specified in the parameters ``var_x_balance_name_ord`` and ``var_x_balance_name_unord`` if the parameter ``p_bt_yes`` is set to True. See also the table below. 

+------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| Parameter                    | Description                                                                                                                                           |
+==============================+=======================================================================================================================================================+
| ``p_bt_yes``                 | If True, balancing tests for the features specified in ``var_x_balance_name_ord`` and ``var_x_balance_name_unord`` are conducted. The default is True.|
+------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``var_x_balance_name_ord``   | Only relevant if ``p_bt_yes`` is True. Ordered features for which balancing tests are conducted.                                                      |
+------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``var_x_balance_name_unord`` | Only relevant if ``p_bt_yes`` is True. Unordered features for which balancing tests are conducted.                                                    |
+------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+

Please consult the :py:class:`API <mcf_functions.ModifiedCausalForest>` for more details.

The results of the balancing tests are part of the txt-file in the output folder that the **mcf** package generates. You can find the location of this folder by accessing the `"outpath"` entry of the `gen_dict` attribute of your Modified Causal Forest:

.. code-block:: python

    from mcf import ModifiedCausalForest

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord="x"
        )

    my_mcf.gen_dict["outpath"]

Example
~~~~~~~

.. code-block:: python

    from mcf import ModifiedCausalForest

    ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"],
        var_x_name_unord=["female"],
        # Parameters for balancing tests:
        p_bt_yes=True,
        var_x_balance_name_ord=["x1", "x2"],
        var_x_balance_name_unord=["female"]
    )


Sensitivity checks
------------------

The method :py:meth:`~mcf_functions.ModifiedCausalForest.sensitivity` of the :class:`~mcf_functions.ModifiedCausalForest` class contains some simulation-based tools to check how well the Modified Causal Forest works in removing selection bias and how sensitive the results are with respect to potentially missing confounding covariates (i.e., those related to treatment and potential outcomes).

A paper by Armendariz-Pacheco, Lechner, and Mareckova (2024) will discuss and investigate the different methods in detail. So far, please note that all methods are simulation based.

The sensitivity checks consist of the following steps:

1. Estimate all treatment probabilities.
2. Remove all observations from treatment states other than one (largest treatment or user-determined).
3. Use estimated probabilities to simulate treated observations, respecting the original treatment shares (pseudo-treatments).
4. Estimate the effects of pseudo-treatments. The true effects are known to be zero, so the deviation from 0 is used as a measure of result sensitivity.

Steps 3 and 4 may be repeated, and results averaged to reduce simulation noise.

Please consult the API for details on how to use the :py:meth:`~mcf_functions.ModifiedCausalForest.sensitivity` method.