"""
The JSON logger
"""
from typing import List, Dict
import json
import logging
import sys


SCHEMA = '{"level": "%(levelname)s", "ts": "%(asctime)s", "caller": "%(name)s", "msg": "%(message)s"}'


def file_logger(path: str, name: str) -> logging.Logger:
    """Function to get a file logger

    :type path: String
    :param path: The full path to the log file Example: /tmp/some_log.log
    :type name: String
    :param name: The name of the logger

    :rtype: logging.Logger
    :returns: The logger
    """
    this_logger = logging.getLogger(name)
    logging.basicConfig(format=SCHEMA, filename=path)
    logging.getLogger().setLevel(logging.INFO)
    return this_logger


def console_logger(name: str) -> logging.Logger:
    """Function to get a console logger

    :type name: String
    :param name: The name of the logger

    :rtype: logging.Logger
    :returns: The logger
    """
    this_logger = logging.getLogger(name)
    logging.basicConfig(format=SCHEMA, stream=sys.stdout)
    logging.getLogger().setLevel(logging.INFO)
    return this_logger


def add_console_logger(root_logger: logging.Logger) -> None:
    """Function to add a console logger

    :type root_logger: logging.Logger
    :param root_logger: The logger to add console logger to

    :rtype: None
    :returns: Nothing it adds a console logger

    :raises TypeError: If root_logger is not of type logging.Logger
    """
    if not isinstance(root_logger, logging.Logger):
        raise TypeError(f'root_logger must be of type logging.Logger but received a {type(root_logger)}')

    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt=SCHEMA)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def process_log_file(data: str) -> List[Dict[str, str]]:
    """Function that converts log entries to dicts and appends to list

    :type data: String
    :param data: The log data

    :rtype: List[Dict[str, str]]
    :returns: Te log data as python objects
    """
    final_data = []
    data_split = data.splitlines()
    for line in data_split:
        final_data.append(json.loads(line))

    return final_data


def read_log_file(path: str) -> List[Dict[str, str]]:
    """Function that reads log data and converts log entries to dicts and appends to list

    :type path: String
    :param path: The full path to the log file Example: /tmp/some_log.log

    :rtype: List[Dict[str, str]]
    :returns: Te log data as python objects
    """

    with open(path, 'r', encoding='utf-8') as file:
        log_file = file.read()

    return process_log_file(log_file)
