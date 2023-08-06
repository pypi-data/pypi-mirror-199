import os
import pytest
from zapish_logger import file_logger, read_log_file, add_console_logger, console_logger


def test_file_logger(tmp_path):
    d = tmp_path / 'logs'
    d.mkdir()
    path = os.path.join(str(d), 'unit-test.log')
    logger = file_logger(path=path, name='unit-test')
    add_console_logger(logger)
    logger.warning('one')
    logger.warning('two')


def test_add_console_logger_bad():
    with pytest.raises(TypeError):
        add_console_logger('bad')


def test_read_log_file(log_data_path):
    data = read_log_file(log_data_path)
    assert len(data) == 2


def test_console_logger():
    logger = console_logger('unit-test')
    logger.warning('one')
