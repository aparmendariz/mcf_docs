Estimation of treatment effects
===============================

The Modified Causal Forest estimates three types of average treatment effects, which differ in their aggregation level and are discussed in depth by `Lechner (2019) <https://doi.org/10.48550/arXiv.1812.09487>`_. These effects are the average treatment effect (:math:`\textrm{ATE}`), the group average treatment effect (:math:`\textrm{GATE}`), and the individualized average treatment effect (:math:`\textrm{IATE}`). They are defined as follows:

We consider a discrete, multi-valued treatment :math:`D`. The potential outcome of treatment state :math:`d` is denoted by :math:`Y^d`. The covariates are denoted by :math:`X` and :math:`Z \subset X` is a low-dimensional vector of features that defines population groups (e.g. age groups, gender, etc.). The effects of interest are then defined as:

.. math::

    \textrm{ATE}(m,l;\Delta) &:= \ \mathbb{E} \big[ Y^m-Y^l \big\vert D\in \Delta \big]

    \textrm{GATE}(m,l;z,\Delta) &:= \mathbb{E} \big[ Y^m-Y^l \big\vert Z=z, D\in \Delta \big]

    \textrm{IATE}(m,l;x) &:= \mathbb{E} \big[ Y^m-Y^l \big\vert X=x \big]

If :math:`\Delta = \{m\}` :math:`\textrm{ATE}(m,l;\Delta)` is simply the average treatment effect on the treated (:math:`\textrm{ATET}`) for treatment :math:`m`. 


ATEs / ATETs
----------------------------------

ATEs are computed without the need of specifying any input arguments.

Computing effects for the treated
----------------------------------

The effects for the treated are computed if the input arguments `p_atet <./mcf_api.md#p_atet>`_ or `p_gatet <./mcf_api.md#p_gatet>`_ are set to *True*.

we can make a reference to BGATE's and CBGATE's here

Also a quick discussion of the inference here and how to get standard errors
(not technical!)

technical details on the inference are in the algorithm reference (different
types of inference methods available). make a reference to that here.
