
from unittest.mock import patch
from unittest.mock import call
from collections import namedtuple

from .conftest import raises
import logging

from dbassembly.logger import *


class DBAssemblyError(Exception):
    pass

class TestColorFormatter(object):
    def setup(self):
        self.color_formatter = ColorFormatter('%(levelname)s: %(message)s')

    @patch('logging.Formatter.format')
    def test_format(self, mock_format):
        MyRecord = namedtuple(
            'MyRecord',
            'levelname'
        )
        record = MyRecord(levelname='INFO')
        mock_format.return_value = 'message'
        self.color_formatter.format(record)
        assert 'message' in self.color_formatter.format(record)


class TestInfoFilter(object):
    def setup(self):
        self.info_filter = InfoFilter()

    def test_filter(self):
        MyRecord = namedtuple(
            'MyRecord',
            'levelno'
        )
        record = MyRecord(levelno=logging.INFO)
        assert self.info_filter.filter(record) is True


class TestDebugFilter(object):
    def setup(self):
        self.debug_filter = DebugFilter()

    def test_filter(self):
        MyRecord = namedtuple(
            'MyRecord',
            'levelno'
        )
        record = MyRecord(levelno=logging.DEBUG)
        assert self.debug_filter.filter(record) is True


class TestErrorFilter(object):
    def setup(self):
        self.error_filter = ErrorFilter()

    def test_filter(self):
        MyRecord = namedtuple(
            'MyRecord',
            'levelno'
        )
        record = MyRecord(levelno=logging.ERROR)
        assert self.error_filter.filter(record) is True


class TestWarningFilter(object):
    def setup(self):
        self.error_filter = WarningFilter()

    def test_filter(self):
        MyRecord = namedtuple(
            'MyRecord',
            'levelno'
        )
        record = MyRecord(levelno=logging.WARNING)
        assert self.error_filter.filter(record) is True


class TestLogger(object):
    @patch('sys.stdout')
    def test_progress(self, mock_stdout):
        log.progress(50, 100, 'foo')
        mock_stdout.write.assert_called_once_with(
            '\rfoo: [####################                    ] 50%'
        )
        mock_stdout.flush.assert_called_once_with()

    def test_progress_raise(self):
        assert log.progress(50, 0, 'foo') is None

    def test_progress_raise_with100(self):
        assert log.progress(100, 100, 'foo') is None

    @patch('logging.FileHandler')
    def test_set_logfile(self, mock_file_handler):
        log.set_logfile('logfile')
        mock_file_handler.assert_called_once_with('logfile')

    @patch('dbassembly.logger.ColorFormatter')
    def test_set_color_format(self, mock_color_format):
        log.set_color_format()
        assert sorted(mock_color_format.call_args_list) == [
            call(
                '$COLOR[ %(levelname)-8s]: %(asctime)-8s | %(message)s',
                '%H:%M:%S'
            ),
            call(
                '$COLOR[ %(levelname)-8s]: %(asctime)-8s | %(message)s',
                '%H:%M:%S'
            ),
            call(
                '$LIGHTCOLOR[ %(levelname)-8s]: %(asctime)-8s | %(message)s',
                '%H:%M:%S'
            )
        ]

    @raises(DBAssemblyError)
    @patch('logging.FileHandler')
    def test_set_logfile_raise(self, mock_file_handler):
        mock_file_handler.side_effect = DBAssemblyError
        log.set_logfile('logfile')

    def test_getLogLevel(self):
        log.setLogLevel(42)
        assert log.getLogLevel() == 42
