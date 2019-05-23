# coding: utf-8
from __future__ import print_function, unicode_literals
import sys
import os
from typing import Optional, Any

def ipython_info() -> Optional[str]:
    """determines if iPython/Jupyter notebook is running"""
    try:
        return get_ipython()
    except NameError:
        return None
    #if 'ipykernel' in sys.modules:
        #ip = 'notebook'
    #elif 'Ipython' in sys.modules:
        #ip = 'terminal'
    #return ip


def properties(nframe: int=3) -> Any:
    """
    Gets frame information

    Parameters
    ----------
    nframe : int; default=3
        the number of frames to jump back
        0 = current
        2 = calling from an embedded function (e.g., log_msg)
        3 = calling from an embedded class (e.g., SimpleLogger)

    Returns
    -------
    line number : int
        the line number of the nth frame
    filename : str
        the filen ame of the nth frame
    """
    # jump to get out of the logger code
    frame = sys._getframe(nframe)
    active_file = os.path.basename(frame.f_globals['__file__'])
    if active_file.endswith('.pyc'):
        return frame.f_lineno, active_file[:-1]
    return frame.f_lineno, active_file
