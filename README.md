# cpylog
A simple pure python colorama/HTML capable logger

This is a library for creating a llimited pure Python version of the standard logging object,

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
