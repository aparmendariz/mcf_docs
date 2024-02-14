Common support
==============

Estimating heterogenous treatment effects requires common support in all treatment arms. The class :py:class:`~mcf_functions.ModifiedCausalForest` has several options to check for and enforce common support. 

Common support checks and corrections are performed before any causal effects are estimated. You can control the type of common support adjustment with the parameter ``cs_type`` of the class :py:class:`~mcf_functions.ModifiedCausalForest`. If you set ``cs_type`` to 0, there is no common support adjustment. 

If you set ``cs_type`` to 1 (the default) or 2, common support is enforced based on propensity scores that are estimated with classification forests. [1]_ The Modified Causal Forest will then remove all observations whose propensity scores lie outside certain cut-off probabilities. For a value of 1, which is the default, the cut-off probabilities are determined automatically by the **mcf** package. For a value of 2, you can specify the cut-off probabilities yourself using the parameter ``cs_min_p``. Any observation with an estimated propensity score :math:`\widehat{P(D = m| X)}` less than or equal to ``cs_min_p`` for at least one treatment arm will then be removed from the data set.

When common support adjustments are enabled, the **mcf** package will display standard common support plots to help you understand the distribution of propensity scores across treatment arms. These plots are also saved in the output folder that the **mcf** package generates. You can find the location of this folder by accessing the `"outpath"` entry of the `gen_dict` attribute of your Modified Causal Forest:

.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord="x"
    )
    my_mcf.gen_dict["outpath"]

The common support plots will be stored in the subfolder `common_suppport`.

.. [1] Out of bag predictions are used to avoid overfitting.


Advanced options
----------------

In a setting with multiple treatments the restrictiveness of a common support criterion increases with the number of treatments. The parameter ``cs_adjust_limits`` allows you to reduce this restrictiveness. The upper cut-off will be multiplied by :math:`1 + \text{cs_adjust_limits}` and the lower cut-off will be multiplied by :math:`1 - \text{cs_adjust_limits}`. 

The parameter ``cs_max_del_train`` allows you to specify a maximum share of observations in the training data set that are allowed to be dropped to enforce common support. If this threshold is exceeded, the program will terminates raise a corresponding exception. By default an error will be raised if more than 50% of the observations are dropped. In this case, you should consider using a more balanced input data set.


WIP here

The parameter ``cs_quantil`` allows you to deviate from the default cut-off probabilities when ``cs_type`` is set to 1, which are based on min-max rules. 

If ``cs_quantil`` is set to a value of less than 1, the respective quantile is used to determine the upper and lower cut-off probabilities. 

Concretely, observations are dropped if at least one of their propensity scores
is smaller than the largest ``cs_quantil``-quantile or larger than the ``1-cs_quantil``) quantile of the treatment groups.

propensity scores are smaller than the largest :math:`q` or larger than the smallest (:math:`1-q`) quantile of the treatment groups. 


Parameter overview
------------------

Below is an overview of the above mentioned parameters related to common support adjustments in the class :py:class:`~mcf_functions.ModifiedCausalForest`:  



Examples
------------------

        cs_quantil : Float (or None), optional
            Common support adjustment: How to determine upper and lower bounds.
                If CS_TYPE == 1: 1 or None: min-max rule
                                 < 1: respective quantil
            Default (or None) is 1.

interpretation:
    if cs_type is 1,
        if cs_quantil = 1: min max rules are employed 
        if cs_quantil < 1: quantile is used to determine upper and lower bounds


        cs_type : Integer (or None), optional
            Common support adjustment: Method.
                0: No common support adjustment
                1,2: Support check based on estimated classification forests.
                  1: Min-max rules for probabilities in treatment subsamples.
                  2: Enforce minimum and maximum probabilities for all obs
                     all but one probability
                  Observations off support are removed. Out-of-bag predictions
                  are used to avoid overfitting (which would lead to a too
                  large reduction in the number of observations).
            Default (or None) is 1.














For 1, the min-max rules for the estimated probabilities in the treatment subsamples are deployed. For 2, the minimum and maximum probabilities for all observations are deployed. All observations off support are removed. 


 You may specify a quantile in `cs_quantil <./mcf_api.md#cs_quantil>`_. Denoting by :math:`q` the quantile chosen, the program drops observations with propensities scores smaller than the largest :math:`q` or larger than the smallest (:math:`1-q`) quantile of the treatment groups. Alternatively, you may specify the support threshold of the propensity scores in `cs_min_p <./mcf_api.md#cs_min_p>`_. If a support check is conducted, the program removes all observations with at least one treatment state off support.

The argument `cs_max_del_train <./mcf_api.md#cs_max_del_train>`_ defines a threshold for the share of observations off support in the training data set. If this threshold is exceeded, the program terminates because of too large imbalances in the features across treatment states. In such a case, a new and more balanced input data set is required to run the program.

Parameter overview
------------------

The following table summarizes the parameters related to common support adjustments in the class :py:class:`~mcf_functions.ModifiedCausalForest`:


### Input arguments for common support

| Argument                                       | Description                                                  |
| ---------------------------------------------- | ------------------------------------------------------------ |
| [cs_type](./mcf_api.md#cs_type)     | Specifies type of common support adjustment. If set to 0, there is no common support adjustment. If set to 1 or 2, the support check is based on the estimated classification regression forests. For 1, the min-max rules for the estimated probabilities in the treatment subsamples are deployed. For 2, the minimum and maximum probabilities for all observations are deployed. All observations off support are removed. Note that out-of-bag predictions are used to avoid overfitting (which leads to a too large reduction in observations). |


            cs_adjust_limits=None, cs_max_del_train=0.5, cs_min_p=0.01,
            cs_quantil=1, cs_type=1,