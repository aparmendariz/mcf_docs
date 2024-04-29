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
  effects, their corresponding standard errors and other related objects, all of which can be inspected in your variable explorer.

  Here is a brief demonstration on how to retrieve these results:

  .. code-block:: python

     # Train the Modified Causal Forest:
     my_mcf.train(df)
     # Assign the output of the predict method to a variable:
     results = my_mcf.predict(df)
     # The 'results' dictionary contains the estimated treatment effects, standard errors and others:
     print(results.keys())

  For more examples you can check out the :ref:`Getting Started <getting-started>` or the :doc:`user_guide`.


- **Where can I find the results of the OptimalPolicy class?**

  The results are stored in a dictionary returned by the :py:meth:`~mcf_functions.ModifiedCausalForest.predict` method of the    :py:class:`~mcf_functions.ModifiedCausalForest` class. This dictionary contains various estimated treatment 
  effects, their standard errors and other objects that you can view on your variable explorer. 

  The following example briefly showcases how to access such results: 

  .. code-block:: python

     # Train the Modified Causal Forest:
     my_mcf.train(df)
     # Assign the output of the predict method to a variable:
     results = my_mcf.predict(df)
     # The 'results' dictionary contains the estimated treatment effects, standard errors and others:
     print(results.keys())

  For more examples you can check out the :ref:`Getting Started <getting-started>` or the :doc:`user_guide`.

- **Do I include the heterogeneity variable in the covariates?**

  Yes, you must include the heterogeneity variable that you are interested in with the rest of your covariates.

- **How can I determine which data points were excluded during common support checks and access the corresponding dataframe?**

- **How do I access the dataframe representing the final sample that passed common support criteria?**

Troubleshooting
---------------

- **I'm getting an error when I try to install the package. What should I do?**

  Make sure you have the latest version of pip installed. If the problem persists, please open an issue on the GitHub repository.

- **The package installed successfully, but I'm getting an error when I try to import it. What should I do?**

  This could be due to a conflict with other packages or an issue with your Python environment. Try creating a new virtual environment and installing the package there. If the problem persists, please open an issue on the GitHub repository.

- **I'm getting unexpected results when I use the package. What should I do?**

  Make sure you're using the package as intended. Check the documentation and examples to see if you're using the functions and classes correctly. If you believe the results are incorrect, please open an issue on the GitHub repository.

- **The package is running slower than I expected. What can I do to improve performance?**

  Performance can depend on many factors, including the size of your data and your hardware. Check the documentation for tips on improving performance. 

- **I'm having trouble understanding how to use a certain feature of the package. Where can I find help?**

  The documentation is the best place to start. It provides a detailed explanation of all features and how to use them. If you're still having trouble, consider asking a question on a relevant forum or opening an issue on the GitHub repository.

