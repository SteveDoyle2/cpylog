import sys
from colorama import Fore, Style  # type: ignore

#import time
#session_name = get_default_session()
RED = Fore.RED # error
GREEN = Fore.GREEN # info
CYAN = Fore.CYAN # debug
YELLOW = Fore.YELLOW # warning
#if session_name and 'powershell.exe' in session_name or 'cmd.exe' in session_name:
RED += Style.BRIGHT
CYAN += Style.BRIGHT
GREEN += Style.BRIGHT
YELLOW += Style.BRIGHT


def write_error(msg: str) -> None:
    """writes an error message"""
    sys.stdout.write(RED + msg)


def write_colorama(typ: str, name: str, msg: str, encoding: str) -> None:
    """if we're writing to the screen"""
    try:
        _write_colorama_screen(typ, name + msg)
    except IOError:
        sys.stdout.write(f'error writing line...encoding={encoding!r}\n')
        sys.stdout.write(msg)


def _write_colorama_screen(typ: str, msg: str) -> None:
    """
    Writes to the screen

    Parameters
    ----------
    typ : str
        messeage type - ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    msg : str
        message to be displayed

    """
    # write to the screen
    #
    # Python 3 requires str, not bytes
    #timestring = '%s  ' % time.strftime('%H:%M:%S', time.localtime())
    # max length of 'INFO', 'DEBUG', 'WARNING', etc.
    #name = '%-8s' % (typ + ':')
    #filename_n = '%s:%s' % (filename, lineno)
    #msg2 = ' %-28s %s\n' % (filename_n, msg)

    #msg_all = (timestring + name + msg) if typ else timestring + msg

    #msg = timestring + msg
    if typ == 'INFO':
        sys.stdout.write(GREEN + msg)
    elif typ == 'DEBUG':
        sys.stdout.write(CYAN + msg)
    elif typ == 'WARNING':
        # no ORANGE?
        sys.stdout.write(YELLOW + msg)
    else: # error / other
        sys.stdout.write(RED + msg)
