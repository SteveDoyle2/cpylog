"""tests log.py"""
import os
import unittest

from cpylog import SimpleLogger, FileLogger, get_logger, get_logger2

class TestLog(unittest.TestCase):
    #def test_multi_logger(self):
        #logger = MultiLogger()

    def test_file_logger(self):
        with FileLogger(level='debug', filename='file1.log', include_stream=True, encoding='utf-8') as test_log:
            test_log.debug('debug message')
            test_log.warning('warning')
            test_log.error('errors')
            test_log.exception('exception')
        os.remove('file1.log')

        with FileLogger(level='debug', filename='file2.log', include_stream=False, encoding='utf-8') as test_log2:
            test_log2.debug('no streamer')
        os.remove('file2.log')

        test_log2 = FileLogger(level='debug', filename='file2b.log', include_stream=False, encoding='utf-8')
        test_log2.debug('no streamer')
        del test_log2
        #os.remove('file2b.log')

        #test_log2 = FileLogger(level='debug', filename=None, include_stream=False, encoding='utf-8')
        #test_log2.debug('no file/streamer')

        test_log3 = FileLogger(level='debug', filename=None, include_stream=True, encoding='utf-8')
        test_log3.debug('no file')
        del test_log3

    def test_simple_logger(self):
        log = SimpleLogger(level='critical')
        log.info('info')
        log.warning('warning')
        log.error('error')
        log.debug('debug')
        log.exception('exception')
        out = log.critical('critical')
        assert out is None

    def test_simple_logger_log_func(self):
        def log_func(typ, filename, n, msg):
            print('typ=%r filename=%r n=%r msg=%r' % (typ, filename, n, msg))
            assert typ == 'INFO', '%r' % msg
            assert msg == 'info_log_func', '%r' % msg
        log = SimpleLogger(level='info', log_func=log_func)
        log.info('info_log_func')

    def test_get_logger(self):
        log1 = get_logger(level='debug')
        log2 = get_logger(level='info')
        assert log1 is not log2
        log3 = get_logger(log=log2, level='info')
        assert log2 is log3

    def test_log_messages(self):
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


if __name__ == "__main__":
    unittest.main()
