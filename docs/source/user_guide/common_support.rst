Common support
==============

Estimating heterogenous treatment effects requires common support in all treatment arms. The class :py:class:`~mcf_functions.ModifiedCausalForest` has several options to check for and enforce common support. 

Implementation
==============

Common support checks and corrections are performed before any causal effects are estimated. You can control the type of common support adjustment with the parameter ``cs_type``. If you set ``cs_type`` to 0, there is no common support adjustment. If you set ``cs_type`` to 1 or 2, common support is enforced based on on propensity scores that are the estimated with classification forests. 

For a value of 1, the min-max rules for the estimated probabilities in the treatment subsamples are deployed. For 2, the minimum and maximum probabilities for all observations are deployed. All observations off support are removed.

        cs_quantil : Float (or None), optional
            Common support adjustment: How to determine upper and lower bounds.
                If CS_TYPE == 1: 1 or None: min-max rule
                                 < 1: respective quantil
            Default (or None) is 1.

        cs_min_p : Float (or None), optional
            Common support adjustment: If cs_type == 2, observations are
               deleted if p(d=m|x) is less or equal than cs_min_p for at least
               one treatment. Default (or None) is 0.01.

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


This is a prameter uses to adjust the upper and lower limits to account for multiple treatments:

        cs_adjust_limits : Float (or None), optional
            Common support adjustment: Accounting for multiple treatments.
                None: (number of treatments - 2) * 0.05
                If cs_type > 0:
                    upper limit *= 1+support_adjust_limits,
                    lower limit *= 1-support_adjust_limits
            The restrictiveness of the common support criterion increases with
            the number of treatments. This parameter allows to reduce this
            restrictiveness. Default is None.

Parameter to raise an exception should a large share of observations be off support.

        cs_max_del_train : Float (or None), optional
            Common support adjustment: If share of observations in training
               data used that are off support is larger than cs_max_del_train
               (0-1), an exception is raised. In this case, user should change
               input data. Default (or None) is 0.5.







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