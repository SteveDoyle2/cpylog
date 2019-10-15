# coding: utf-8
import sys
import os
from typing import Optional, Tuple

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

def get_default_session() -> Optional[str]:
    """
    Locates the first ancestor process which is a shell. Returns
    its pid, or None if not found.
    """
    try:
        import psutil
    except ImportError:
        return None

    if psutil.POSIX:
        def predicate(name):
            return name.endswith("sh")
    elif psutil.WINDOWS:
        def predicate(name):
            return name in ("cmd.exe", "powershell.exe")
    else:
        return None

    proc = psutil.Process()
    proc = proc.parent()
    if proc is None:
        # python.exe -> wing.exe -> explorer.exe
        # python.exe -> cmd.exe -> explorer.exe
        # python.exe -> powershell.exe -> explorer.exe
        return None

    while proc.pid:
        name = proc.name()
        if predicate(name):
            return name
            #return proc.pid
        proc = proc.parent()
    return None

def properties(nframe: int=3) -> Tuple[int, str]:
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
