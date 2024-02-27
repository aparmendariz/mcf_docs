Local centering
===============

Method
--------

Local centering is a form of residualization, which can improve the performance of forest estimators. 
This performance improvement is achieved by regressing out the impact of the features on the outcome.

Formally, the conditionally centered outcome :math:`\tilde{Y}_i` can be defined as:

.. math::

   \tilde{Y}_i = Y_i - \hat{y}_{-i}(X_i)


where:

- :math:`\tilde{Y}_i` is the conditionally centered outcome.
- :math:`Y_i` indicates the outcome for observation :math:`\textrm{i}`.
- :math:`\hat{y}_{-i}(X_i)` is an estimate of the conditional outcome expectation :math:`E[Y_i | X_i = x_i]`, given the observed values :math:`x_i` of the feature vector :math:`X_i`, computed without using the observation i.


Implementation
---------------

The local centering procedure applies the RandomForestRegressor method of the sklearn.ensemble module to compute the predicted outcomes :math:`\hat{y}_{-i}(X_i)` for each observation i non-parametrically. 
To turn the procedure off, overrule the default ``lc_yes`` and set it to ``False``. The predicted outcomes are computed in distinct subsets by cross-validation, where the number of folds can be specified in ``lc_cs_cv_k``. Finally, the centered outcomes are obtained by subtracting the predicted from the observed outcomes.


Alternatively, two separate data sets can be generated for running the local centering procedure with ``lc_cs_cv``. In this case, the size of the first data set can be defined in ``lc_cs_share`` and it is used for training a Random Forest, again by applying the RandomForestRegressor method. The predicted and centered outcomes :math:`\hat{y}_{-i}(X_i)` and :math:`\tilde{Y}_i`, respectively, are computed in the second data set. Finally, this second data set is divided into mutually exclusive data sets for feature selection (optionally), tree building, and effect estimation.


+-------------------+-----------------------------------------------------------------------------+
| Argument          | Description                                                                 |
+-------------------+-----------------------------------------------------------------------------+
| ``lc_yes``        | Activates local centering. Default is True                                  |
+-------------------+-----------------------------------------------------------------------------+
| ``lc_cs_cv``      | Data to be used for local centering & common support adjustment. True: Crossvalidation. False: Random sample not to be used for forest building. Default (or None) is True.  |
+-------------------+-----------------------------------------------------------------------------+
| ``lc_cs_share``   | Data to be used for local centering & common support adjustment: Share of trainig data (if lc_cs_cv is False). Default (or None) is 0.25.          |
+-------------------+-----------------------------------------------------------------------------+
| ``lc_cs_cv_k``    | Number of folds in cross-validation (if lc_cs_cv is True). Default (or None) is 5.  |
+-------------------+-----------------------------------------------------------------------------+




