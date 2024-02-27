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
- :math:`Y_i` indicates the outcome for observation i.
- :math:`\hat{y}_{-i}(X_i)` is an estimate of the conditional outcome expectation :math:`E[Y_i | X_i = x_i]`, given the observed values :math:`x_i` of the feature vector :math:`X_i`, computed without using the observation i.


Implementation
---------------
