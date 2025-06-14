"""defines a colorama log"""
# coding: utf-8
import sys
import os
import traceback
from typing import Optional
from cpylog.utils import (
    ipython_info, properties, properties2,
    get_frame_file_from_frame)  # get_default_session
from cpylog.warning_redirector import WarningRedirector

__version__ = '1.6.0'  # 1.5.0 is latest released
__desc__ = 'cpylog'
__long__ = __desc__
__website__ = 'https://github.com/cpylog/cpylog'
__license__ = 'BSD-3'
__author__ = 'Steven Doyle'
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
        from colorama import init as colorinit  # type: ignore
        colorinit(autoreset=True)
        IS_COLORAMA = True
    except ImportError:
        IS_COLORAMA = False
    USE_COLORAMA = IS_COLORAMA and IS_TERMINAL and not USE_HTML

if USE_COLORAMA:
    from cpylog.colorama_utils import write_colorama as _write
elif USE_HTML:
    from cpylog.jupyter_utils import write_html as _write
else:
    from cpylog.screen_utils import write_screen as _write


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
                 nlevels: int=1, log_func=None) -> None:
        """
        Creates a SimpleLogger

        Parameters
        ----------
        level : str
            level of logging: 'info', 'debug', 'warning', 'error', or 'critical'
        encoding : str; default='utf-8'
            the unicode encoding method
        nlevels : int; default=1
            the number of levels to show
        log_func : function
            funtion that will be used to print log. It should take:
            type: str; default=None -> print to stdout (@see ``stdout_logging``)
               logging level; {DEBUG, INFO, WARNING, ERROR, CRITICAL}
            filename: str
                the file where the log message was raised
            lineno: int
                the line number corresponding to the filename
            msg: str
                the message to log

        Example
        -------
        >>> log1 = SimpleLogger(level='debug', encoding='utf-8',
                                log_func=None)
        >>> log1.info('info message')
        INFO:  cpylog.py:100   info message

        def func(typ, filename, lineno, msg):
            print(msg)
        >>> log2 = SimpleLogger(level='debug', encoding='utf-8',
                                log_func=func)
        >>> log2.info('log func message')
        log func message

        """
        if log_func is None:
            log_func = self.stdout_logging
        assert level in ('info', 'debug', 'warning', 'error', 'critical'), 'logging level=%r' % level
        #assert encoding in ['utf-8', 'latin-1', 'ascii'], encoding
        self.level = level
        self.log_func = log_func
        self.encoding = encoding
        self._nlevels = nlevels
        assert nlevels >= 1, nlevels

        # log may be enabled/disabled (useful for multiprocessing)
        self._active = True

        # log format may be modified to clean up printout
        # should still be of the form:
        #  '%-s %s\n'
        self._level_filename_fmt = ' %-28s %s\n'
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
        if isinstance(lineno, list):
            filename_lineno = '/'.join([f'{filenamei}:{linenoi}'
                                        for filenamei, linenoi in zip(filename, lineno)])
        else:
            filename_lineno = f'{filename}:{lineno}'
        msg2 = self._level_filename_fmt % (filename_lineno, msg)

        #from .html_utils import str_to_html
        #try:
            #str_to_html(typ, filename, lineno, msg2)
        #except:
            #print(typ, filename, lineno, msg2, type(msg2))
            #raise

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
        lineno, filename = properties2(nframe=nframe, dframe=self._nlevels-1)
        self.log_func(typ, filename, lineno, msg)
        #self.log_func(typ, '   fname=%-25s lineNo=%-4s   %s\n' % (fn, lineno, msg))

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
        # jump to get out of the logger code
        frame = sys._getframe(2)
        lineno = frame.f_lineno
        frame_file = get_frame_file_from_frame(frame)
        filename = os.path.basename(frame_file)

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
        if self.level in {'error', 'critical'}:
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
        if self.level in {'error', 'critical'}:
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

    #def __enter__(self):
        #return self.file_obj
    #def __exit__(self, type, value, traceback):
        #if USE_COLORAMA:
            #from colorama import Style
            #print(Style.RESET_ALL)
            #print("ending...")
        #return True

    def __repr__(self):
        return 'SimpleLogger(level=%r, encoding=%r)' % (self.level, self.encoding)


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
    # jump to get out of the logger code
    frame = sys._getframe(nframe)
    frame_file = get_frame_file_from_frame(frame)
    active_file = os.path.basename(frame_file)
    if active_file.endswith('.pyc'):
        return frame.f_lineno, active_file[:-1]
    return frame.f_lineno, active_file

def get_logger(log: Optional[SimpleLogger]=None,
               level: Optional[str | bool]='debug',
               encoding: str='utf-8',
               nlevels: int=1) -> SimpleLogger:
    """
    This function is useful as it will instantiate a SimpleLogger object
    if log=None.

    Parameters
    ----------
    log : log / None
        a python logging module object;
        if log is set, debug is ignored and uses the
        settings the logging object has
    level : str / bool / None; default=True
       used to set the logger if no logger is passed in
           True:  logs debug/info/warning/error messages ('debug' level)
           False: logs info/warning/error messages ('info' level)
           None:  logs warning/error messages ('warning level')
           str:   one of: 'debug', 'info', 'warning', 'error', 'critical'
    encoding : str; default='utf-8'
        the unicode encoding method
    nlevels : int; default=1
        the number of levels to show

    Returns
    -------
    log : log / SimpleLogger
        logging

    """
    if log is not None:
        pass
    elif isinstance(level, str):
        log = SimpleLogger(level=level, encoding=encoding, nlevels=nlevels)
    elif level is None:
        log = SimpleLogger(level='warning', encoding=encoding, nlevels=nlevels)
    else:
        assert isinstance(level, bool), 'level must be True/False/None or debug/info/warning/error/critical'
        level_str = 'debug' if level else 'info'
        log = SimpleLogger(level=level_str, encoding=encoding, nlevels=nlevels)
    return log


def get_logger2(log: Optional[SimpleLogger]=None,
                debug: Optional[str | bool]=True,
                encoding: str='utf-8',
                nlevels: int=1) -> SimpleLogger:
    """see get_logger"""
    log = get_logger(
        log=log, level=debug,
        encoding=encoding, nlevels=nlevels)
    return log


class FileLogger(SimpleLogger):
    def __init__(self, level: str='debug', encoding: str='utf-8',
                 nlevels: int=1,
                 filename: Optional[str]=None,
                 mode: str='w',
                 include_stream: bool=True,
                 log_func=None):
        """
                Parameters
        ----------
        level : str
            level of logging: 'info', 'debug', 'warning', 'error', or 'critical'
        nlevels : int; default=1
            the number of levels to show
        encoding : str; default='utf-8'
            the unicode encoding method
        filename : str; default=None
            str : write to a file
        include_stream : bool
            write to the screen (e.g., use the classic simpleLogger)
        nlevels : int; default=1
            the number of levels to show
        log_func : function
            funtion that will be used to print log. It should take:
            type: str; default=None -> print to stdout (@see ``stdout_logging``)
               logging level; {DEBUG, INFO, WARNING, ERROR, CRITICAL}
            filename: str
                the file where the log message was raised
            lineno: int
                the line number corresponding to the filename
            msg: str
                the message to log

        Example
        -------
        >>> log1 = FileLogger(level='debug', encoding='utf-8',
                              nlevels=1, log_func=None)
        >>> log1.info('info message')
        INFO:  cpylog.py:100   info message

        def func(typ, filename, lineno, msg):
            print(msg)
        >>> log2 = FileLogger(level='debug', encoding='utf-8',
                              log_func=func)
        >>> log2.info('log func message')
        log func message

        """
        SimpleLogger.__init__(self, level=level, encoding=encoding,
                              nlevels=nlevels, log_func=None)

        self.include_stream = include_stream
        self.loggers = []
        self._file = None
        self._filename = filename

        is_file_logger = filename is not None
        assert include_stream or is_file_logger, 'a print stream or file must be included'
        if filename is not None:
            dirname = os.path.dirname(os.path.abspath(filename))
            assert os.path.exists(dirname), dirname

        if include_stream and is_file_logger:
            self.loggers.append(self.log_func)
            self._file = open(filename, mode, encoding=encoding)
            self.loggers.append(self.file_logging)
            self.msg_typ = self.msg_typ_file
        elif is_file_logger:
            #print(f'only using a file; include_stream={include_stream} is_file_logger={is_file_logger} filename={filename}')
            self._file = open(filename, mode, encoding=encoding)
            self.log_func = self.file_logging
        #else:
            #print(f'only using a streamer; include_stream={include_stream} is_file_logger={is_file_logger} filename={filename}')
        #self.debug(str(self))


    def __repr__(self) -> str:
        msg = (f'FileLogger(level={self.level!r}, filename={self._filename}, '
               f'include_stream={self.include_stream}, encoding={self.encoding!r}, nlevels={self._nlevels})')
        return msg

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
        lineno, filename = properties()
        for log_func in self.loggers:
            log_func(typ, filename, lineno, msg)

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
        filename_lineno = f'{filename}:{lineno}'
        msg2 = self._level_filename_fmt % (filename_lineno, msg)
        self._file.write((name + msg2) if typ else msg2)
        self._file.flush()

def log_exc(log: SimpleLogger, limit=None, chain: bool=True):
    """Shorthand for 'log_exception(log, *sys.exc_info(), limit)'."""
    log_exception(log, *sys.exc_info(), limit=limit, chain=chain)

def log_exception(log: SimpleLogger, etype, value, tb, limit=None, chain: bool=True):
    """Print exception up to 'limit' stack trace entries from 'tb' to 'log'.

    This differs from print_tb() in the following ways:
      (1) if traceback is not None, it prints a header "Traceback (most
          recent call last):"
      (2) it logs the exception type and value after the stack trace
      (3) if type is SyntaxError and value has the appropriate format,
          it logs the line where the syntax error occurred with a
          caret on the next line indicating the approximate position
          of the error.

    """
    lines = []
    for line in traceback.TracebackException(
            type(value), value, tb, limit=limit).format(chain=chain):
        lines.append(line)
    log.error('\n' + ''.join(lines))


if __name__ == '__main__':  # pragma: no cover
    # how to use a simple logger
    for debug_level in {'debug', 'info'}:
        #print('--- %s logger ---' % debug_level)
        test_log = SimpleLogger(debug_level, encoding='utf-8')
        test_log.debug('debug message')
        test_log.warning('warning')
        test_log.error('errors')
        test_log.exception('exception')
