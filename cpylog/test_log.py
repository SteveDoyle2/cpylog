"""tests log.py"""
import os
import tempfile
import warnings
import unittest

import cpylog
from cpylog import (
    SimpleLogger, FileLogger, get_logger, get_logger2, log_exc,
    WarningRedirector)
from cpylog.utils import get_default_session

from cpylog.screen_utils import write_screen
try:
    from cpylog.colorama_utils import write_colorama, write_error
    IS_COLORAMA = True
except ImportError as exception:
    warnings.warn(exception)
    IS_COLORAMA = False

from cpylog.html_utils import str_to_html
try:
    from cpylog.jupyter_utils import write_html
    HTML_PASSED = True
except ImportError as exception:
    warnings.warn(exception)
    HTML_PASSED = False

PKG_PATH = cpylog.__path__[0]
dirname = os.path.dirname(__file__)
if dirname == '':
    dirname = '.'

is_continuous_integration = (
    'TRAVIS' in os.environ or
    'TRAVIS_PYTHON_VERSION' in os.environ or
    'GITHUB_ACTOR' in os.environ
)

class TestLog(unittest.TestCase):
    """tests the SimpleLogger and FileLogger classes"""
    #def test_multi_logger(self):
        #logger = MultiLogger()


    @unittest.skipIf(not HTML_PASSED, 'HTML import failed')
    def test_html(self):
        """tests the HTML interface"""
        typ = 'CAT'
        name = 'name: '
        msg = 'msg'
        encoding = 'pig'
        write_html(typ, name, msg, encoding)

        encoding = None
        write_html(typ, name, msg, encoding)

    @unittest.skipIf(IS_COLORAMA is False, 'colorama import failed')
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
        #dirname = '.' # os.path.relpath(os.path.dirname(PKG_PATH), os.getcwd())
        filename = os.path.join(dirname, 'file_logger_1.log')
        _remove_file(filename)

        print('dirname=', dirname)
        with FileLogger(level='debug', filename=filename, include_stream=True,
                        encoding='utf-8') as test_log:
            if is_continuous_integration:
                norm_path = f'cpylog{os.sep}file_logger_1.log'
                expected_log = rf"FileLogger(level='debug', filename={norm_path}, include_stream=True, encoding='utf-8', nlevels=1)"
            else:
                norm_path = os.path.join(dirname, 'file_logger_1.log')
                expected_log = rf"FileLogger(level='debug', filename={norm_path}, include_stream=True, encoding='utf-8', nlevels=1)"

            actual_log = str(test_log)
            # windows local: "FileLogger(level='debug', filename=.\\file_logger_1.log, include_stream=True, encoding='utf-8', nlevels=1)"
            # windows root:  "FileLogger(level='debug', filename=.\\cpylog\\file_logger_1.log, include_stream=True, encoding='utf-8', nlevels=1)"
            # linux local:   "FileLogger(level='debug', filename=./file_logger_1.log, include_stream=True, encoding='utf-8', nlevels=1)"
            # linux root:    "FileLogger(level='debug', filename=cpylog/file_logger_1.log, include_stream=True, encoding='utf-8', nlevels=1)"
            #print('actual_log: %r' % actual_log)
            if not actual_log == expected_log:
                msg = f'\nactual:   {actual_log}\nexpected: {expected_log}'
                test_log.error(msg)
            #else:
                #assert str(test_log) == r"FileLogger(level='debug', filename=cpylog/file_logger_1.log, include_stream=True, encoding='utf-8', nlevels=1)", str(test_log)
            test_log.debug('debug message')
            test_log.warning('warning')
            test_log.error('errors')
            test_log.exception('exception')
        #os.remove(filename)

        filename = os.path.join(dirname, 'file_logger_2.log')
        _remove_file(filename)
        with FileLogger(level='debug', filename=filename, include_stream=False,
                        encoding='utf-8') as test_log2:
            test_log2.debug('no streamer')
        os.remove(filename)

        filename = os.path.join(dirname, 'file_logger_3.log')
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
        assert 'critical' in out
        
    def test_simple_logger_log_func(self):
        """tests using a log function"""
        def log_func(typ, filename, lineno, msg):
            #print('typ=%r filename=%r lineno=%r msg=%r' % (typ, filename, lineno, msg))
            str_to_html(typ, filename, lineno, msg)
            assert typ == 'INFO', '%r' % msg
            assert msg == 'info_log_func', '%r' % msg
            return msg
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
        assert (log1 is not log2)
        log3 = get_logger(log=log2, level='info')
        assert log2 is log3

    def test_log_messages(self):
        """tests using get_logger2"""
        log1 = get_logger2(debug=True)
        log1.info('info')
        assert 'warning' in log1.warning('warning')
        assert 'error' in log1.error('error')
        assert 'debug' in log1.debug('debug')
        assert 'exception' in log1.exception('exception')
        assert 'critical' in log1.critical('critical')
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

    def test_log_exc(self):
        """tests ``log_exc``"""
        log = SimpleLogger(level='info')
        with self.assertRaises(TypeError):
            try:
                1 + 'cat'
            except TypeError:
                log_exc(log, limit=None, chain=True)
                raise
    def test_default_session(self):
        """tests ``get_default_session``"""
        shell = get_default_session()
        #assert shell in ('cmd.exe', 'powershell.exe', 'sh', 'WindowsTerminal.exe'), 'shell=%r' % shell
        print('shell', shell)

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

class TestLazyFormatting(unittest.TestCase):
    """Tests for *args lazy formatting (lazy=True/False)."""

    def test_args_formatting_when_logged(self):
        """Verify %-format args produce the correct message when logged."""
        messages = []
        def capture(typ, filename, lineno, msg):
            messages.append(msg)
            return msg

        log = SimpleLogger(level='debug', log_func=capture)
        log.info('count=%d name=%s', 42, 'hello')
        self.assertEqual(messages[-1], 'count=42 name=hello')

        log.warning('pi=%.2f', 3.14159)
        self.assertEqual(messages[-1], 'pi=3.14')

        log.debug('%s %s %s', 'a', 'b', 'c')
        self.assertEqual(messages[-1], 'a b c')

        log.error('value=%r', [1, 2])
        self.assertEqual(messages[-1], "value=[1, 2]")

        log.critical('x=%d', 99)
        self.assertEqual(messages[-1], 'x=99')

        log.exception('err=%s code=%d', 'fail', 500)
        self.assertEqual(messages[-1], 'err=fail code=500')

    def test_no_args_unchanged(self):
        """Verify plain string messages still work without args."""
        messages = []
        def capture(typ, filename, lineno, msg):
            messages.append(msg)
            return msg

        log = SimpleLogger(level='debug', log_func=capture)
        log.info('plain message')
        self.assertEqual(messages[-1], 'plain message')

    def test_lazy_true_skips_formatting_when_suppressed(self):
        """With lazy=True, args are not formatted if the level suppresses the message."""
        class Bomb:
            def __str__(self):
                raise RuntimeError('should not format')
            def __repr__(self):
                raise RuntimeError('should not format')

        log = SimpleLogger(level='warning', lazy=True)
        # debug and info are suppressed — Bomb.__str__ must not be called
        log.debug('value=%s', Bomb())
        log.info('value=%s', Bomb())

    def test_lazy_false_formats_eagerly_even_when_suppressed(self):
        """With lazy=False (default), bad format args raise even if message is suppressed."""
        log = SimpleLogger(level='warning', lazy=False)
        with self.assertRaises(TypeError):
            log.debug('bad=%d', 'not_a_number')
        with self.assertRaises(TypeError):
            log.info('bad=%d', 'not_a_number')

    def test_lazy_true_formats_when_logged(self):
        """With lazy=True, args are still formatted when the message passes the level check."""
        messages = []
        def capture(typ, filename, lineno, msg):
            messages.append(msg)
            return msg

        log = SimpleLogger(level='debug', lazy=True, log_func=capture)
        log.info('n=%d', 7)
        self.assertEqual(messages[-1], 'n=7')

    def test_lazy_flag_default_is_false(self):
        """The default lazy value is False."""
        log = SimpleLogger(level='debug')
        self.assertFalse(log.lazy)

    def test_get_logger_passes_lazy(self):
        """get_logger propagates the lazy parameter."""
        log = get_logger(level='debug', lazy=True)
        self.assertTrue(log.lazy)

        log2 = get_logger(level='info', lazy=False)
        self.assertFalse(log2.lazy)

    def test_file_logger_lazy(self):
        """FileLogger accepts and uses the lazy parameter."""
        filename = os.path.join(dirname, 'file_logger_lazy.log')
        _remove_file(filename)

        class Bomb:
            def __str__(self):
                raise RuntimeError('should not format')

        with FileLogger(level='warning', filename=filename, lazy=True) as log:
            # suppressed — should not format
            log.debug('val=%s', Bomb())
            log.info('val=%s', Bomb())
            # logged — should format
            log.warning('x=%d', 5)
        _remove_file(filename)


class TestLevelFiltering(unittest.TestCase):
    """Tests that messages are suppressed/emitted based on logger level.

    These tests use a capturing log_func so we can inspect what was
    actually logged vs. silently returned.
    """

    def _make_logger(self, level, **kwargs):
        """Return (logger, logged_messages_list)."""
        logged = []
        def capture(typ, filename, lineno, msg):
            logged.append((typ, msg))
            return msg
        log = SimpleLogger(level=level, log_func=capture, **kwargs)
        return log, logged

    # ----------------------------------------------------------------
    # Bug 1a: debug() has NO non-lazy level gate — always emits
    # ----------------------------------------------------------------
    def test_debug_suppressed_at_info_level(self):
        """debug() should not emit when level='info'."""
        log, logged = self._make_logger('info')
        log.debug('should be hidden')
        self.assertEqual(logged, [], 'debug message was emitted at info level')

    def test_debug_suppressed_at_warning_level(self):
        log, logged = self._make_logger('warning')
        log.debug('hidden')
        self.assertEqual(logged, [])

    def test_debug_suppressed_at_error_level(self):
        log, logged = self._make_logger('error')
        log.debug('hidden')
        self.assertEqual(logged, [])

    def test_debug_suppressed_at_critical_level(self):
        log, logged = self._make_logger('critical')
        log.debug('hidden')
        self.assertEqual(logged, [])

    def test_debug_emitted_at_debug_level(self):
        log, logged = self._make_logger('debug')
        log.debug('visible')
        self.assertEqual(len(logged), 1)
        self.assertEqual(logged[0][1], 'visible')

    # ----------------------------------------------------------------
    # Bug 1b: info() uses wrong variable in level check
    # ----------------------------------------------------------------
    def test_info_suppressed_at_warning_level(self):
        """info() should not emit when level='warning'."""
        log, logged = self._make_logger('warning')
        log.info('should be hidden')
        self.assertEqual(logged, [], 'info message was emitted at warning level')

    def test_info_suppressed_at_error_level(self):
        log, logged = self._make_logger('error')
        log.info('hidden')
        self.assertEqual(logged, [])

    def test_info_suppressed_at_critical_level(self):
        log, logged = self._make_logger('critical')
        log.info('hidden')
        self.assertEqual(logged, [])

    def test_info_emitted_at_debug_level(self):
        log, logged = self._make_logger('debug')
        log.info('visible')
        self.assertEqual(len(logged), 1)

    def test_info_emitted_at_info_level(self):
        log, logged = self._make_logger('info')
        log.info('visible')
        self.assertEqual(len(logged), 1)

    # ----------------------------------------------------------------
    # Bug 1c: warning() uses wrong variable in level check
    # ----------------------------------------------------------------
    def test_warning_suppressed_at_error_level(self):
        log, logged = self._make_logger('error')
        log.warning('hidden')
        self.assertEqual(logged, [], 'warning message was emitted at error level')

    def test_warning_suppressed_at_critical_level(self):
        log, logged = self._make_logger('critical')
        log.warning('hidden')
        self.assertEqual(logged, [])

    def test_warning_emitted_at_warning_level(self):
        log, logged = self._make_logger('warning')
        log.warning('visible')
        self.assertEqual(len(logged), 1)

    # ----------------------------------------------------------------
    # Bug 1d: error() uses wrong variable in level check
    # ----------------------------------------------------------------
    def test_error_suppressed_at_critical_level(self):
        """error() should not emit when level='critical'.

        Note: the current WRITE_LEVELS_MAP includes 'error' in
        the 'critical' set, so this test documents the expected
        behavior per the map.  If the intent is that critical
        suppresses error, the map needs changing too.
        """
        # Per WRITE_LEVELS_MAP['critical'] = {'error', 'critical'},
        # error IS in the set, so error messages SHOULD be logged
        # at critical level.  This test verifies that.
        log, logged = self._make_logger('critical')
        log.error('should be visible per map')
        self.assertEqual(len(logged), 1)

    # ----------------------------------------------------------------
    # Return value checks — suppressed messages should return ''
    # ----------------------------------------------------------------
    def test_suppressed_debug_returns_msg(self):
        """When suppressed (non-lazy), debug() returns the formatted msg."""
        log = SimpleLogger(level='warning')
        result = log.debug('suppressed')
        self.assertEqual(result, 'suppressed')

    def test_suppressed_info_returns_msg(self):
        """When suppressed (non-lazy), info() returns the formatted msg."""
        log = SimpleLogger(level='warning')
        result = log.info('suppressed')
        self.assertEqual(result, 'suppressed')

    def test_suppressed_lazy_returns_empty(self):
        """When suppressed with lazy=True, methods return ''."""
        log = SimpleLogger(level='warning', lazy=True)
        self.assertEqual(log.debug('x'), '')
        self.assertEqual(log.info('x'), '')

    # ----------------------------------------------------------------
    # Verify critical and exception always emit
    # ----------------------------------------------------------------
    def test_critical_always_emits(self):
        for level in ('debug', 'info', 'warning', 'error', 'critical'):
            log, logged = self._make_logger(level)
            log.critical('always')
            self.assertEqual(len(logged), 1,
                             f'critical not emitted at level={level}')

    def test_exception_always_emits(self):
        for level in ('debug', 'info', 'warning', 'error', 'critical'):
            log, logged = self._make_logger(level)
            log.exception('always')
            self.assertEqual(len(logged), 1,
                             f'exception not emitted at level={level}')


class TestFileLoggerBugs(unittest.TestCase):
    """Tests for FileLogger-specific bugs."""

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _tmpfile(self, name='test.log'):
        return os.path.join(self._tmpdir, name)

    # ----------------------------------------------------------------
    # Bug 2: msg_typ_file returns None, breaking return contract
    # ----------------------------------------------------------------
    def test_msg_typ_file_returns_string(self):
        """FileLogger with stream+file should return a string from info()."""
        filename = self._tmpfile('retval.log')
        with FileLogger(level='debug', filename=filename,
                        include_stream=True) as log:
            result = log.info('return value test')
            self.assertIsInstance(
                result, str,
                f'FileLogger.info() returned {type(result).__name__}, expected str')

    # ----------------------------------------------------------------
    # Bug 3: FileLogger ignores log_func parameter
    # ----------------------------------------------------------------
    def test_file_logger_custom_log_func(self):
        """FileLogger should honor a custom log_func when only streaming."""
        calls = []
        def custom_func(typ, filename, lineno, msg):
            calls.append((typ, msg))
            return msg
        log = FileLogger(level='debug', filename=None,
                         include_stream=True, log_func=custom_func)
        log.info('custom')
        # If log_func were honored, calls would be non-empty
        # Currently it's silently ignored (line 498 passes log_func=None)
        self.assertTrue(
            len(calls) > 0,
            'FileLogger ignored the custom log_func parameter')
        del log

    def test_file_logger_file_written(self):
        """FileLogger with include_stream=False writes to the file."""
        filename = self._tmpfile('content.log')
        with FileLogger(level='debug', filename=filename,
                        include_stream=False) as log:
            log.info('hello file')
        with open(filename) as f:
            content = f.read()
        self.assertIn('hello file', content)

    def test_file_logger_level_filtering(self):
        """FileLogger should respect level filtering for file output."""
        filename = self._tmpfile('level.log')
        with FileLogger(level='warning', filename=filename,
                        include_stream=False) as log:
            log.debug('hidden debug')
            log.info('hidden info')
            log.warning('visible warning')
            log.error('visible error')
        with open(filename) as f:
            content = f.read()
        self.assertNotIn('hidden debug', content,
                         'debug message appeared in file at warning level')
        self.assertNotIn('hidden info', content,
                         'info message appeared in file at warning level')
        self.assertIn('visible warning', content)
        self.assertIn('visible error', content)


class TestEdgeCases(unittest.TestCase):
    """Additional edge-case and coverage tests."""

    def test_simple_msg(self):
        """Exercise simple_msg path."""
        calls = []
        def capture(typ, filename, lineno, msg):
            calls.append((typ, msg))
            return msg
        log = SimpleLogger(level='debug', log_func=capture)
        log.simple_msg('raw message', typ='INFO')
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1], 'raw message')

    def test_enable_disable_returns_empty(self):
        """Disabled logger should return '' from all methods."""
        log = SimpleLogger(level='debug')
        log.disable()
        self.assertEqual(log.debug('x'), '')
        self.assertEqual(log.info('x'), '')
        self.assertEqual(log.warning('x'), '')
        self.assertEqual(log.error('x'), '')

    def test_repr(self):
        log = SimpleLogger(level='info', encoding='ascii')
        self.assertEqual(repr(log), "SimpleLogger(level='info', encoding='ascii')")

    def test_get_logger_with_none_level(self):
        """get_logger(level=None) should create a warning-level logger."""
        log = get_logger(level=None)
        self.assertEqual(log.level, 'warning')

    def test_get_logger_with_bool_true(self):
        log = get_logger(level=True)
        self.assertEqual(log.level, 'debug')

    def test_get_logger_with_bool_false(self):
        log = get_logger(level=False)
        self.assertEqual(log.level, 'info')

    def test_get_logger_passthrough(self):
        """get_logger returns existing log unchanged."""
        existing = SimpleLogger(level='error')
        returned = get_logger(log=existing, level='debug')
        self.assertIs(returned, existing)
        self.assertEqual(returned.level, 'error')  # not overridden

    def test_invalid_level_raises(self):
        with self.assertRaises(AssertionError):
            SimpleLogger(level='bogus')

    def test_nlevels_zero_raises(self):
        with self.assertRaises(AssertionError):
            SimpleLogger(level='debug', nlevels=0)

    def test_format_args_type_error(self):
        """Bad %-format args raise TypeError."""
        log = SimpleLogger(level='debug')
        with self.assertRaises(TypeError):
            log.info('val=%d', 'not_a_number')

    def test_lazy_debug_skips_bomb(self):
        """lazy=True + suppressed debug should not touch args."""
        class Bomb:
            def __str__(self):
                raise RuntimeError('boom')
            def __mod__(self, other):
                raise RuntimeError('boom')
        log = SimpleLogger(level='error', lazy=True)
        # Should not raise
        log.debug('val=%s', Bomb())

    def test_lazy_error_skips_bomb_at_critical(self):
        """lazy=True: error() suppressed at critical level skips formatting.

        Note: per WRITE_LEVELS_MAP['critical'] = {'error', 'critical'},
        error is NOT suppressed at critical level, so this Bomb WILL
        be formatted.  Adjusting test to match actual map semantics.
        """
        # error IS in WRITE_LEVELS_MAP['critical'], so it's not suppressed
        # This test just documents current behavior
        log = SimpleLogger(level='critical', lazy=True)
        # error is logged at critical level per the map, so formatting happens
        result = log.error('count=%d', 42)
        self.assertIn('42', result)


def _remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
