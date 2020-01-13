from __future__ import annotations
import os
import warnings
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # pragma: no cover
    from cpylog import SimpleLogger


class WarningRedirector:
    def __init__(self, log: SimpleLogger):
        """
        Initialize ``WarningRedirector``, which takes standard python
        ``warning.warn(...)`` and adds it to the ``logger.warning(...)``.

        Parameters
        ----------
        log : SimpleLogger
            Log.

        """
        self.log = log
        #assert isinstance(self.log, SimpleLogger)

        self._showwarning_old = None

    def __enter__(self):
        """
        Set new showwarning function to log.warn and save the old one
        to return to later.

        """
        self._showwarning_old = warnings.showwarning

        def warn(message: str, category, filename: str, lineno: str, file=None, line=None):
            #return self.log.log_function_handler('WARNING', os.path.basename(filename), lineno,
                                                 #message)
            self.log.log_func('WARNING', os.path.basename(filename), lineno,
                              message)
        warnings.showwarning = warn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore previous showwarning function."""
        warnings.showwarning = self._showwarning_old
