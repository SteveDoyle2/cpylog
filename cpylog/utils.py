# coding: utf-8
import sys
import os
from typing import Optional
from pathlib import Path

def ipython_info() -> Optional[str]:
    """determines if iPython/Jupyter notebook is running"""
    #print('type', type(get_ipython()))
    #print('config', get_ipython().config['IPKernelApp'])
    try:
        ipython = get_ipython()

        # Spyder doesn't support HTML objects.
        # Check for spyder in order to fall back on Colorama
        if 'SPY_PYTHONPATH' in os.environ:
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

def properties(nframe: int=3) -> tuple[int, str]:
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
        #frame_file = get_frame_file_from_frame(frame)
        #active_file = os.path.basename(frame_file)
        #star = '*' if iframe == nframe else ''
        #print(f'{star}{iframe}: {frame} active_file={active_file}')

    # jump to get out of the logger code
    frame = sys._getframe(nframe)
    frame_file = get_frame_file_from_frame(frame)
    active_file = os.path.basename(frame_file)
    if active_file.endswith('.pyc'):
        return frame.f_lineno, active_file[:-1]
    return frame.f_lineno, active_file

def properties2(nframe: int=3, dframe: int=0) -> tuple[int, str]:
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
    fnamesi = []
    frame = sys._getframe(nframe)
    frame_file = get_frame_file_from_frame(frame)
    active_file = os.path.abspath(frame_file)
    base_file = os.path.basename(active_file)
    dirname = os.path.dirname(active_file)

    if dframe == 0:
        pass
    elif dframe == 1:
        fnamesi.append(os.path.basename(dirname))
    else:
        parts = Path(dirname).parts[-dframe:]
        fnamesi.extend(parts)
    fnamesi.append(base_file[:-1] if base_file.endswith('.pyc')
                   else base_file)
    return frame.f_lineno, '/'.join(fnamesi)


def get_frame_file_from_frame(frame) -> str:
    """
    Gets the active filename from a frame

    Stock python uses __file__
    Jupyter notebook uses __session__ because reasons
    """
    try:
        frame_file = frame.f_globals['__file__']
    except KeyError:
        if '__session__' in frame.f_globals:
            frame_file = frame.f_globals['__session__']
        else:
            raise
        # for key, value in frame.f_globals.items():
        #     print(f'{key}:  {value}\n')
        # raise
    return frame_file
