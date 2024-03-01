Inference
=========

The **mcf** offers three ways of conducting inference. 

- Weights-based Inference Procedure: This is the default method. It is particularly useful to gain information on the precision of estimators that have a representation as weighted averages of the outcomes. See `Lechner (2018) <https://doi.org/10.48550/arXiv.1812.09487>`_ for more details.

- Variance of Treatment Effect Estimates: This method estimates the variance of treatment effect estimates as the sum of the variance of weighted outcomes.

- Bootstrap Algorithm: This method uses a bootstrap algorithm to obtain inference.


Methods 
------------------------

One way to do inference for treatment effects is to estimate the variance of the treatment effect estimator based on a variance decomposition into two components: 

- Expectation of the conditional variance

- Variance of the conditional expectation, given the weights. 

This variance decomposition takes heteroscedasticity in the weights into account. The conditional means and variances are estimated non-parametrically, either by the Nadaraya-Watson kernel estimator or by the k-Nearest Neighbor (k-NN) estimator (default).

Another way to obtain inference is to compute the variance of a treatment effect estimator as the sum of the variances of the weighted outcomes in the respective treatment states. A drawback of this inference method is that it implicitly assumes homoscedasticity in the weights for each treatment state.

Alternatively, the standard bootstrap can be applied to compute standard errors. Our algorithm bootstraps the equally weighted weights and then renormalizes them.

**Note**: because of the weighting representation, inference can also readily be used to account for clustering, which is a common feature in economics data.


Parameters 
------------------------

Below you find a list of the main parameters which are related to the inference procedure of the **mcf**. Please consult the :py:class:`API <mcf_functions.ModifiedCausalForest>` for more details or additional parameters. 

.. list-table:: 
   :widths: 30 70
   :header-rows: 1

   * - Parameter
     - Description
   * - ``p_se_boot_ate``
     - (Integer or Boolean (or None), optional) – Bootstrap of standard errors for ATE. Specify either a Boolean (if True, number of bootstrap replications will be set to 199) or an integer corresponding to the number of bootstrap replications (this implies True). None: 199 replications p_cluster_std is True, and False otherwise. Default is None.
   * - ``p_se_boot_gate``
     - (Integer or Boolean (or None), optional) – Bootstrap of standard errors for GATE. Specify either a Boolean (if True, number of bootstrap replications will be set to 199) or an integer corresponding to the number of bootstrap replications (this implies True). None: 199 replications p_cluster_std is True, and False otherwise. Default is None.
   * - ``p_se_boot_iate``
     - (Integer or Boolean (or None), optional) – Bootstrap of standard errors for IATE. Specify either a Boolean (if True, number of bootstrap replications will be set to 199) or an integer corresponding to the number of bootstrap replications (this implies True). None: 199 replications p_cluster_std is True, and False otherwise. Default is None.
   * - ``p_cond_var``
     - True: Conditional mean & variances are used. False: Variance estimation uses directly. Default (or None) is True.
   * - ``p_knn``
     - (Boolean (or None), optional) – True: k-NN estimation. False: Nadaraya-Watson estimation. Nadaray-Watson estimation gives a better approximaton of the variance, but k-NN is much faster, in particular for larger datasets. Default (or None) is True.


Example
~~~~~~~~~

.. code-block:: python

    my_mcf = ModifiedCausalForest(
        var_y_name="y",
        var_d_name="d",
        var_x_name_ord=["x1", "x2"],
        # Names of ordered variables with many values to define causal heterogeneity
        var_z_name_list=["age"],
        # Variables to balance the GATEs on
        var_bgate_name=["age"], 
    )



