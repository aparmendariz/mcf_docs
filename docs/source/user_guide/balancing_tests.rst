Balancing Tests
===============

Treatment effects may be subject to selection bias if the distribution of the confounding features differs across treatment arms. The class :py:class:`~mcf_functions.ModifiedCausalForest` provides the option to conduct balancing tests to assess whether the feature distributions are equal across treatment arms after adjustment by the Modified Causal Forest. The balancing tests are based on the estimation of average treatment effects (:math:`\text{ATE's}`) with user-specified features as outcomes. If the features are balanced across treatment arms, the estimated :math:`\text{ATE's}` should be close to zero.

Note: These balancing test should be considered experimental for now. Further work is needed to investigate how the balancing statistics are related to the bias of the estimation.

The Modified Causal Forest runs balancing tests for the features specified in the parameters ``var_x_balance_name_ord`` and ``var_x_balance_name_unord`` if the parameter ``p_bt_yes`` is set to True. See also the table below:

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

Example
-------

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