# coding: utf-8
import sys
import os
from typing import Optional, Tuple

def ipython_info() -> Optional[str]:
    """determines if iPython/Jupyter notebook is running"""
    #print('type', type(get_ipython()))
    #print('config', get_ipython().config['IPKernelApp'])
    try:
        ipython = get_ipython()

        # Spyder 4.0 doesn't support HTML objects.
        # we're crossing our fingers that Spyder 4.1 does...
        if 'spyder' in sys.modules and 'spyder_kernels' in sys.modules:
            import spyder
            spyder_version = spyder.__version__
            if spyder_version < '4.1':
                return None
        return ipython
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
    its name, or None if not found.  Some examples include:
     - cmd.exe
     - powershell.exe
     - WindowsTerminal.exe
     - sh

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
        # powershell.exe -> conhost.exe -> WindowsTerminal.exe -> sihost.exe
        #                -> svchost.exe -> services.exe -> wininit.exe
        return None

    return_name = None
    while proc and proc.pid:
        name = proc.name()
        #print(name)
        if predicate(name):
            return_name = name
        elif name == 'WindowsTerminal.exe':
            return_name = 'cmd.exe'
            #return proc.pid
        proc = proc.parent()
    return return_name

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
    # helpful for seeing what's happening
    #for iframe in [0, 1, 2, 3, 4, 5]:
        #frame = sys._getframe(iframe)
        #active_file = os.path.basename(frame.f_globals['__file__'])
        #star = '*' if iframe == nframe else ''
        #print(f'{star}{iframe}: {frame} active_file={active_file}')

    # jump to get out of the logger code
    frame = sys._getframe(nframe)
    active_file = os.path.basename(frame.f_globals['__file__'])
    if active_file.endswith('.pyc'):
        return frame.f_lineno, active_file[:-1]
    return frame.f_lineno, active_file
