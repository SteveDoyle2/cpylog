"""defines a colorama log"""
# coding: utf-8
import sys
import os
from typing import Optional
from cpylog.utils import ipython_info, properties # , get_default_session

__version__ = '1.2.0'
__desc__ = 'cpylog'
__long__ = __desc__
__website__ = 'https://github.com/cpylog/cpylog'
__license__ = 'BSD-3'
__author__ = ''
__email__ = ''

# True if writing to screen
# False if writing to a file
# terminal is False if we're piping to a file
IS_TERMINAL = False
if hasattr(sys.stdout, 'isatty'):  # pyInstaller <= 3.1 doesn't have this
    IS_TERMINAL = sys.stdout.isatty()

USE_HTML = ipython_info() is not None
USE_COLORAMA = IS_TERMINAL and not USE_HTML

if USE_COLORAMA:
    # You're running in a real terminal
    try:
        from colorama import init as colorinit, Fore, Style  # type: ignore
        colorinit(autoreset=True)
        IS_COLORAMA = True
    except ImportError:
        IS_COLORAMA = False
    USE_COLORAMA = IS_COLORAMA and IS_TERMINAL and not USE_HTML
#print(sys.modules)

if USE_COLORAMA:
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

    def _write(typ: str, name: str, msg: str, encoding: str) -> None:
        """if we're writing to the screen"""
        try:
            _write_colorama_screen(typ, name + msg)
        except IOError:
            sys.stdout.write(f'error writing line...encoding={encoding!r}\n')
            sys.stdout.write(msg)

elif USE_HTML:
    from IPython.core.display import display, HTML

    def _write(typ: str, name: str, msg: str, encoding: str) -> None:
        """
        per:
         - https://stackoverflow.com/questions/16816013/is-it-possible-to-print-using-different-color-in-ipythons-notebook
         - https://stackoverflow.com/questions/25698448/how-to-embed-html-into-ipython-output
        """
        if typ == 'DEBUG':
            color = 'blue'
        elif typ == 'INFO':
            color = 'green'
        elif typ == 'WARNING':
            color = 'orange'
        else:
            color = 'red'
        display(HTML(f'<text style=color:{color}>{name + msg}</text>'))
else:
    #import time
    def _write(typ: str, name: str, msg: str, encoding: str) -> None:
        """writing to the screen"""
        #timestring = '%s  ' % time.strftime('%H:%M:%S', time.localtime())
        # max length of 'INFO', 'DEBUG', 'WARNING', etc.
        #name = '%-8s' % (typ + ':')
        #filename_n = '%s:%s' % (filename, lineno)
        #msg2 = ' %-28s %s\n' % (filename_n, msg)

        #msg_all = (timestring + name + msg) if typ else timestring + msg
        #sys.stdout.write(msg_all)
        sys.stdout.write((name + msg) if typ else msg)


class SimpleLogger:
    """
    Simple logger object. In future might be changed to use Python logging module.
    Four levels are supported:
      - 'debug'
      - 'info'
      - 'warning'
      - 'error'
      - 'critical'
    'debug' prints all messages.  'info' removes only 'debug' messages, etc.

    .. note:: Logging module is currently not supported because I don't
      know how to repoint the log file if the program is called a second
      time.  Poor logging can result in:\n
        1) double logging to a single file\n
        2) all logging going to one file\n
      This is really only an issue when calling logging multiple times,
      such as in an optimization loop or testing.

    """
    def __init__(self, level: str='debug', encoding: str='utf-8',
                 log_func=None) -> None:
        """
        Parameters
        ----------
        level : str
            level of logging: 'info', 'debug', 'warning', 'error', or 'critical'
        encoding : str; default='utf-8'
            the unicode encoding method
        log_func : log
          funtion that will be used to print log. It should take one argument:
          string that is produces by a logger. Default: print messages to
          stderr using @see stderr_logging function.

        """
        if log_func is None:
            log_func = self.stdout_logging
        assert level in ('info', 'debug', 'warning', 'error', 'critical'), 'logging level=%r' % level
        #assert encoding in ['utf-8', 'latin-1', 'ascii'], encoding
        self.level = level
        self.log_func = log_func
        self.encoding = encoding
        self._active = True
        assert isinstance(encoding, str), type(encoding)

    def set_enabled(self, enabled: bool) -> None:
        """temporarily enable/disable logging"""
        assert isinstance(enabled, bool), enabled
        self._active = enabled

    def enable(self) -> None:
        """activates the logger"""
        self._active = True

    def disable(self) -> None:
        """deactivates the logger"""
        self._active = False

    def stdout_logging(self, typ: str, filename: str, lineno: int,
                       msg: str) -> None:
        """
        Default logging function. Takes a text and outputs to stdout.

        Parameters
        ----------
        typ : str
            message type - ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        filename : str
            the active file
        lineno : int
            line number
        msg : str
            message to be displayed

        Message will have format 'typ: msg'

        """
        # max length of 'INFO', 'DEBUG', 'WARNING', etc.
        name = '%-8s' % (typ + ':')
        filename_n = f'{filename}:{lineno}'
        msg2 = ' %-28s %s\n' % (filename_n, msg)

        _write(typ, name, msg2, self.encoding)
        #sys.stdout.flush()

    def msg_typ(self, typ: str, msg: str, nframe: int=3) -> None:
        """
        Log message of a given type

        Parameters
        ----------
        typ : str
            type of a message (e.g. INFO)
        msg : str
            message to be logged
        nframe : int; default=3
            the number of log levels to jump
            should be 3+


        """
        if not self._active:
            return
        n, filename = properties(nframe=nframe)
        self.log_func(typ, filename, n, msg)
        #self.log_func(typ, '   fname=%-25s lineNo=%-4s   %s\n' % (fn, n, msg))

    def simple_msg(self, msg: str, typ: Optional[str]=None) -> None:
        """
        Log message directly without any altering.

        Parameters
        ----------
        msg : str
            message to be looged without any alteration.
        typ : str
            type of a message (e.g. INFO)

        """
        frame = sys._getframe(2)  # jump to get out of the logger code
        lineno = frame.f_lineno
        filename = os.path.basename(frame.f_globals['__file__'])

        assert msg is not None, msg
        self.log_func(typ, filename, lineno, msg)

    def debug(self, msg: str) -> None:
        """
        Log DEBUG message

        Parameters
        ----------
        msg : str
            message to be logged

        """
        if self.level != 'debug':
            return
        self.msg_typ('DEBUG', msg)

    def info(self, msg: str) -> None:
        """
        Log INFO message

        Parameters
        ----------
        msg : str
            message to be logged

        """
        if self.level not in ('debug', 'info'):
            return
        assert msg is not None, msg
        self.msg_typ('INFO', msg)

    def warning(self, msg: str) -> None:
        """
        Log WARNING message

        Parameters
        ----------
        msg : str
            message to be logged

        """
        if self.level in ('error', 'critical'):
            return
        assert msg is not None, msg
        self.msg_typ('WARNING', msg)

    def error(self, msg: str) -> None:
        """
        Log ERROR message

        Parameters
        ----------
        msg : str
            message to be logged

        """
        if self.level in ('error', 'critical'):
            return
        assert msg is not None, msg
        self.msg_typ('ERROR', msg)

    def exception(self, msg: str) -> None:
        """
        Log EXCEPTION message

        Parameters
        ----------
        msg : str
            message to be logged

        """
        assert msg is not None, msg
        self.msg_typ('EXCEPTION', msg)

    def critical(self, msg: str) -> None:
        """
        Log CRITICAL message

        Parameters
        ----------
        msg : str
            message to be logged

        """
        assert msg is not None, msg
        self.msg_typ('CRITICAL', msg)

    def __repr__(self):
        return 'SimpleLogger(level=%r, encoding=%r)' % (self.level, self.encoding)


def get_logger(log=None, level: str='debug', encoding: str='utf-8') -> SimpleLogger:
    """
    This function is useful as it will instantiate a simpleLogger object
    if log=None.

    Parameters
    ----------
    log: log / None
         a logger object or None
    level : str
        level of logging: 'info' or 'debug'
    encoding : str; default='utf-8'
        the unicode encoding method

    Returns
    -------
    log : SimpleLogger
        a logger object
    """
    assert not isinstance(log, str), log
    return SimpleLogger(level, encoding=encoding) if log is None else log


def get_logger2(log=None, debug=True, encoding='utf-8') -> SimpleLogger:
    """
    This function is useful as it will instantiate a SimpleLogger object
    if log=None.

    Parameters
    ----------
    log : log / None
        a python logging module object;
        if log is set, debug is ignored and uses the
        settings the logging object has
    debug : bool / None
       used to set the logger if no logger is passed in
           True:  logs debug/info/warning/error messages
           False: logs info/warning/error messages
           None:  logs warning/error messages
    encoding : str; default='utf-8'
        the unicode encoding method

    Returns
    -------
    log : log / SimpleLogger
        logging

    """
    if log is not None:
        pass
    elif debug is None:
        log = SimpleLogger('warning', encoding=encoding)
    else:
        level = 'debug' if debug else 'info'
        log = SimpleLogger(level, encoding=encoding)
    return log

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

def write_error(msg: str) -> None:
    """writes an error message"""
    sys.stdout.write(RED + msg)


class FileLogger(SimpleLogger):
    def __init__(self, level='debug', encoding='utf-8', filename=None, include_stream=True, log_func=None):
        SimpleLogger.__init__(self, level=level, encoding=encoding, log_func=None)

        self.include_stream = include_stream
        self.loggers = []
        self._file = None
        self._filename = filename

        is_file_logger = filename is not None
        assert include_stream or is_file_logger, 'a print stream or file must be included'

        if include_stream and is_file_logger:
            self.loggers.append(self.log_func)
            self._file = open(filename, 'w', encoding=encoding)
            self.loggers.append(self.file_logging)
            self.msg_typ = self.msg_typ_file
        elif is_file_logger:
            #print(f'only using a file; include_stream={include_stream} is_file_logger={is_file_logger} filename={filename}')
            self._file = open(filename, 'w', encoding=encoding)
            self.log_func = self.file_logging
        #else:
            #print(f'only using a streamer; include_stream={include_stream} is_file_logger={is_file_logger} filename={filename}')
        #self.debug(str(self))


    def __repr__(self):
        return f'FileLogger(level={self.level!r}, filename={self._filename}, include_stream={self.include_stream}, encoding={self.encoding!r})'

    def __del__(self):
        #print('del...')
        if self._file is not None:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exct_type, exce_value, traceback):
        if self._file is not None:
            #print(f'closing {self._filename}')
            self._file.close()
        #print(f'cleanup {self._filename}')

    def msg_typ_file(self, typ: str, msg: str) -> None:
        """
        Log message of a given type

        Parameters
        ----------
        typ : str
            type of a message (e.g. INFO)
        msg : str
            message to be logged

        """
        n, filename = properties()
        for log_func in self.loggers:
            log_func(typ, filename, n, msg)

    def file_logging(self, typ: str, filename: str, lineno: int, msg: str) -> None:
        """
        Default logging function. Takes a text and outputs to stdout.

        Parameters
        ----------
        typ : str
            message type - ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        filename : str
            the active file
        lineno : int
            line number
        msg : str
            message to be displayed

        Message will have format 'typ: msg'

        """
        # max length of 'INFO', 'DEBUG', 'WARNING', etc.
        name = '%-8s' % (typ + ':')
        #filename_n = '%s:%s' % (filename, lineno)
        #msg2 = ' %-28s %s\n' % (filename_n, msg)

        #print('file name=%r msg=%r' % (name, msg))
        self._file.write((name + msg) if typ else msg)


if __name__ == '__main__':  # pragma: no cover
    # how to use a simple logger
    for debug_level in ['debug', 'info']:
        #print('--- %s logger ---' % debug_level)
        test_log = SimpleLogger(debug_level, encoding='utf-8')
        test_log.debug('debug message')
        test_log.warning('warning')
        test_log.error('errors')
        test_log.exception('exception')
