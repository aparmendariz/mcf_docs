Inference
=========

The **mcf** offers three ways of conducting inference. 

- Weights-based Inference Procedure: This is the default method. It is particularly useful to gain information on the precision of estimators that have a representation as weighted averages of the outcomes. See `Lechner (2018) <https://doi.org/10.48550/arXiv.1812.09487>`_ for more details.

- Variance of Treatment Effect Estimates: This method estimates the variance of treatment effect estimates as the sum of the variance of weighted outcomes.

- Bootstrap Algorithm: This method uses a bootstrap algorithm to obtain inference.


Methods
----------------

One way to do inference for treatment effects is to estimate the variance of the treatment effect estimator based on a variance decomposition into two components: 

- Expectation of the conditional variance

- Variance of the conditional expectation, given the weights. 

This variance decomposition takes heteroscedasticity in the weights into account. 

The conditional means and variances are estimated non-parametrically, either by the Nadaraya-Watson kernel estimator or by the k-Nearest Neighbor (k-NN) estimator (default).

Another way to obtain inference is to compute the variance of a treatment effect estimator as the sum of the variances of the weighted outcomes in the respective treatment states. A drawback of this inference method is that it implicitly assumes homoscedasticity in the weights for each treatment state.

Alternatively, the standard bootstrap can be applied to compute standard errors. Our algorithm bootstraps the equally weighted weights and then renormalizes them.

**Note**: because of the weighting representation, inference can also readily be used to account for clustering, which is a common feature in economics data.

