# cpylog
A simple pure python colorama/HTML capable logger

This is a library for creating a limited pure Python (3.6+) version of the standard logging object.  There are two main classes:
 - ``SimpleLogger``
 - ``FileLogger`` (new in v1.1)

``SimpleLogger`` is **limited** in that:
 - no handlers

The **additional** features that the ``SimpleLogger`` has:
 - support for colorama highlighting
   - automatically disabled when piping to a file
 - HTML support for the Jupyter notebook
   - automatically enabled
 - overwritable log functions in order to integrate the log with a GUI

The **additional** features that the ``FileLogger`` has beyond ``SimpleLogger``:
 - file writing and/or stream writing  (new in v1.1)
   - context manager to close file
     ```python
     with FileLoger(level='debug', filename=None, include_stream=True) as log:
         log.debug('SimpleLogger')
     with FileLoger(level='debug', filename='file.log', include_stream=True) as log:
         log.debug('FileLogger/SimpleLogger')
     with FileLoger(level='debug', filename='file.log', include_stream=False) as log:
         log.debug('FileLogger')
     ```

As a **bonus** (limitation?), it crashes when you have invalid logging statement.  This ensures that logging is correct, so if you switch to standard Python logging, that will also be correct.  One of the goals of this logging class is that because it implements a subset of standard Python logging, you can replace it with a standard Python log.

```python
from cpylog import get_logger, get_logger2

# if a log already exists, it's passed through
log0 = None

# level: debug, info, warning, critical, exception
log1 = get_logger(log=log0, level='debug', encoding='utf-8')
log1.debug('debug')
log1.info('info')
log1.warning('warning')
log1.exception('exception')
log1.critical('critical')
DEBUG:     file.py:4  debug
INFO:      file.py:5  info
WARNING:   file.py:6  warning
EXCEPTION: file.py:7  exception
CRITICAL:  file.py:8  critical

# debug: True=debug, False=info, None=warning
log2 = get_logger2(log=log1, debug=True, encoding='utf-8')

``SimpleLogger`` is the base class and if we call it directly, we can overwrite the logging message style.

```python
from cpylog import SimpleLogger
log_base = SimpleLogger(self, level: str='debug', encoding: str='utf-8', log_func=None)

# we can call it with an external function, so you can make a custom formatter
# such as an HTML logger
def log_func(typ, filename, n, msg):
    print('typ=%r filename=%r n=%r msg=%r' % (typ, filename, n, msg))
log_func = SimpleLogger(level='info', log_func=log_func)
```

|  Version  | Docs  | Status |
| :--- 	  | :--- 	  | :--- 	  |
|   Master | [![Documentation Status](https://readthedocs.org/projects/cpylog-git/badge/?version=latest)](http://cpylog-git.readthedocs.io/en/latest/?badge=latest) | [![Linux Status](https://img.shields.io/travis/cpylog/cpylog/master.svg)](https://travis-ci.org/cpylog/cpylog) ![Coverage Status](https://coveralls.io/repos/github/cpylog/cpylog/badge.svg?branch=master) | 
|  [![PyPi Version](https://img.shields.io/pypi/v/cpylog.svg)](https://pypi.python.org/pypi/cpylog) | docs | [![Build Status](https://img.shields.io/travis/cpylog/cpylog/v1.0.svg)](https://travis-ci.org/cpylog/cpylog) [![Coverage Status](https://img.shields.io/coveralls/cpylog/cpylog/v1.0.svg)](https://coveralls.io/github/cpylog/cpylog?branch=v1.0) |


<!---
[![Windows Status](https://ci.appveyor.com/api/projects/status/1qau107h43mbgghi/branch/master?svg=true)](https://ci.appveyor.com/project/cpylog/cpylog)

[![codecov](https://codecov.io/gh/cpylog/cpylog/branch/master/graph/badge.svg)](https://codecov.io/gh/cpylog/cpylog) 

[![Coverage Status](https://img.shields.io/coveralls/cpylog/cpylog/master.svg)](https://coveralls.io/github/cpylog/cpylog?branch=master)
