FAQ
==========================

.. contents::
   :local:
   :depth: 2

Installation
------------

- **How do I install the package?**

  You can install the package following the :ref:`Installation Guide <installation-guide>`.

  As a quick reference, you can install the package using pip:

  .. code-block:: bash

     pip install mcf

Usage
-----

- **Where can I find the results of the ModifiedCausalForest class?**

  The results are stored in a dictionary returned by the :py:meth:`~mcf_functions.ModifiedCausalForest.predict` method of the :py:class:`~mcf_functions.ModifiedCausalForest` class. This dictionary contains various estimated treatment 
  effects, their standard errors and other objects that you can view on your variable explorer. 

  The following example briefly showcases how to access such results: 

  .. code-block:: python

     # Train the Modified Causal Forest:
     my_mcf.train(df)
     # Assign the output of the predict method to a variable:
     results = my_mcf.predict(df)
     # The 'results' dictionary contains the estimated treatment effects, standard errors and others:
     print(results.keys())

  For more examples you can check out the Getting Started or the User Guide.

Troubleshooting
---------------

- **I'm getting an error when I try to install the package. What should I do?**

  Make sure you have the latest version of pip installed. If the problem persists, please open an issue on the GitHub repository.

- **How do I know which sample/data points were eliminated after common support checks? How do I access this dataframe? How do I access the one that had common support, the final sample?**

  [Your answer here]
