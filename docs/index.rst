.. pyatmos documentation master file, created by
   sphinx-quickstart2 on Tue Aug 14 13:26:34 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cpylog's documentation for Master!
==============================================
The cpylog software is a replacement for the standard Python logging module.
It contains a limited, but simple pure Python colorama/HTML capable logger.

It's **limited** in that:
 - no handlers
 - no file writing

As a **bonus** (limitation?), it crashes when you have invalid logging statement.

The **additional** features that the logger has:
 - support for colorama highlighting
 - HTML support for the Jupyter notebook
 - overwritable log functions in order to integrate the log with a GUI

One of the goals of this logging class is that because it implements a subset of standard Python logging,
you can replace it with a standard Python log.


.. toctree::

   reference/cpylog
   reference/modules

..   reference/pyatmos.utils
..   reference/pyatmos.utils.atmosphere
..   reference/pyatmos.utils.atmosphere_vectorized
..   reference/pyatmos.utils.sweep
..   manual/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

