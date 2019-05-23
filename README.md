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

|  Version  | Docs  | Status |
| :--- 	  | :--- 	  | :--- 	  |
|   Master | [![Documentation Status](https://readthedocs.org/projects/cpylog-git/badge/?version=latest)](http://cpylog-git.readthedocs.io/en/latest/?badge=latest) | [![Linux Status](https://img.shields.io/travis/cpylog/cpylog/master.svg)](https://travis-ci.org/cpylog/cpylog) ![Coverage Status](https://coveralls.io/repos/github/cpylog/cpylog/badge.svg?branch=master) | 
|  [![PyPi Version](https://img.shields.io/pypi/v/cpylog.svg)](https://pypi.python.org/pypi/cpylog) | docs | [![Build Status](https://img.shields.io/travis/cpylog/cpylog/v1.0.svg)](https://travis-ci.org/cpylog/cpylog) [![Coverage Status](https://img.shields.io/coveralls/cpylog/cpylog/v1.0.svg)](https://coveralls.io/github/cpylog/cpylog?branch=v1.0) |


<!---
[![Windows Status](https://ci.appveyor.com/api/projects/status/1qau107h43mbgghi/branch/master?svg=true)](https://ci.appveyor.com/project/cpylog/cpylog)

[![codecov](https://codecov.io/gh/cpylog/cpylog/branch/master/graph/badge.svg)](https://codecov.io/gh/cpylog/cpylog) 

[![Coverage Status](https://img.shields.io/coveralls/cpylog/cpylog/master.svg)](https://coveralls.io/github/cpylog/cpylog?branch=master)
