"""tests log.py"""
import os
import warnings
import unittest

from cpylog import (
    SimpleLogger, FileLogger, get_logger, get_logger2,
    WarningRedirector, USE_HTML)

from cpylog.screen_utils import write_screen
try:
    from cpylog.colorama_utils import write_colorama, write_error
except ImportError as exception:
    warnings.warn(exception)

from cpylog.html_utils import str_to_html
try:
    from cpylog.jupyter_utils import write_html
    HTML_PASSED = True
except ImportError as exception:
    warnings.warn(exception)
    HTML_PASSED = False

class TestLog(unittest.TestCase):
    """tests the SimpleLogger and FileLogger classes"""
    #def test_multi_logger(self):
        #logger = MultiLogger()


    @unittest.skipIf(HTML_PASSED == False, 'HTML import failed')
    def test_html(self):
        """tests the HTML interface"""
        typ = 'CAT'
        name = 'name: '
        msg = 'msg'
        encoding = 'pig'
        write_html(typ, name, msg, encoding)

        encoding = None
        write_html(typ, name, msg, encoding)

    def test_colorama(self):
        """tests colorama"""
        typ = 'CAT'
        name = 'name: '
        msg = 'msg'
        encoding = 'pig'
        write_colorama(typ, name, msg, encoding)
        write_error(msg)

    def test_screen_write(self):
        """tests writing to the screen"""
        typ = 'CAT'
        name = 'name: '
        msg = 'msg'
        encoding = 'pig'
        write_screen(typ, name, msg, encoding)

        encoding = None
        write_screen(typ, name, msg, encoding)

    def test_file_logger(self):
        """tests also writing to a file"""
        filename = 'file_logger_1.log'
        _remove_file(filename)
        with FileLogger(level='debug', filename=filename, include_stream=True,
                        encoding='utf-8') as test_log:
            assert str(test_log) == "FileLogger(level='debug', filename=file_logger_1.log, include_stream=True, encoding='utf-8')"
            test_log.debug('debug message')
            test_log.warning('warning')
            test_log.error('errors')
            test_log.exception('exception')
        os.remove(filename)

        filename = 'file_logger_2.log'
        _remove_file(filename)
        with FileLogger(level='debug', filename=filename, include_stream=False,
                        encoding='utf-8') as test_log2:
            test_log2.debug('no streamer')
        os.remove(filename)

        filename = 'file_logger_3.log'
        _remove_file(filename)
        test_log2 = FileLogger(level='debug', filename=filename, include_stream=False,
                               encoding='utf-8')
        test_log2.debug('no streamer')
        del test_log2
        #os.remove(filename)

        #test_log2 = FileLogger(level='debug', filename=None, include_stream=False, encoding='utf-8')
        #test_log2.debug('no file/streamer')

        test_log3 = FileLogger(level='debug', filename=None, include_stream=True, encoding='utf-8')
        test_log3.debug('no file')
        del test_log3

    def test_enable_disable(self):
        """tests enabling/disabling log message"""
        log = SimpleLogger(level='info')
        log.info('info_enabled original')
        log.disable()
        log.info('info_disabled 1')
        log.enable()
        log.info('info_enabled 1')
        log.set_enabled(False)
        log.info('info_disabled 2')
        log.set_enabled(True)
        log.info('info_enabled 2')

    def test_simple_logger(self):
        """tests all the logging levels"""
        log = SimpleLogger(level='critical')
        log.info('info')
        log.warning('warning')
        log.error('error')
        log.debug('debug')
        log.exception('exception')
        out = log.critical('critical')
        assert out is None

    def test_simple_logger_log_func(self):
        """tests using a log function"""
        def log_func(typ, filename, lineno, msg):
            print('typ=%r filename=%r lineno=%r msg=%r' % (typ, filename, lineno, msg))
            str_to_html(typ, filename, lineno, msg)
            assert typ == 'INFO', '%r' % msg
            assert msg == 'info_log_func', '%r' % msg
        log = SimpleLogger(level='info', log_func=log_func)
        log.info('info_log_func')

    def test_get_logger(self):
        """tests the get_logger function"""
        log1 = get_logger(level='debug')
        assert str(log1) == "SimpleLogger(level='debug', encoding='utf-8')"
        assert log1 == log1

        log2 = get_logger(level='info')
        assert str(log2) == "SimpleLogger(level='info', encoding='utf-8')"
        assert log1 is not log2
        assert log1 != log2
        assert not (log1 == log2)
        assert not (log1 is log2)
        log3 = get_logger(log=log2, level='info')
        assert log2 is log3

    def test_log_messages(self):
        """tests using get_logger2"""
        log1 = get_logger2(debug=True)
        log1.info('info')
        log1.warning('warning')
        log1.error('error')
        log1.debug('debug')
        log1.exception('exception')
        log1.critical('critical')
        log1.info('%r' % log1)

        log2 = get_logger2(debug=False)
        log2.info('info')
        log2.warning('warning')
        log2.error('error')
        log2.debug('debug')

        log3 = get_logger2(debug=None)
        log3.info('info')
        log3.warning('warning')
        log3.error('error')
        log3.debug('debug')
        with self.assertRaises(AttributeError):
            log3.bad('bad')


class TestWarningRedirector(unittest.TestCase):
    """Test for ``WarningRedirector``."""

    def test_log_context(self):
        """Test ``WarningRedirector`` as a context manager."""
        log = get_logger(log=None, level='debug')
        log.info('test_log_context')
        with WarningRedirector(log):
            warnings.warn('test_redirected')
        warnings.warn('test')

    def test_file_context(self):
        """Test ``WarningRedirector`` as a context manager."""
        filename = 'file_log_context.log'
        _remove_file(filename)
        with FileLogger(level='debug', filename=filename, include_stream=True,
                        encoding='utf-8') as log:
            log.info('test_file_context')
            with WarningRedirector(log):
                warnings.warn('test_redirected')
            warnings.warn('test')
        _remove_file(filename)

    def test_log_returns(self):
        """
        Test ``WarningRedirector`` returns to the regular warning
        function after use.

        """
        warning_function = warnings.showwarning

        log = get_logger(log=None, level='debug')
        log.info('test_returns')
        with WarningRedirector(log):
            warnings.warn('test_redirected')
        warnings.warn('default warn')
        self.assertIs(warnings.showwarning, warning_function)

def _remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
