#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 19/03/2021
"""

__version__ = "1.0.0"

import io
from logging import config
import logging
import os
import sys
import traceback

from mobio.libs.Singleton import Singleton
from logstash_formatter import LogstashFormatterV1
from logging import DEBUG, INFO, WARNING, ERROR


CONFIG_LOGGING_DIR = None
try:
    CONFIG_LOGGING_DIR, _ = os.path.split(os.path.abspath(__file__))
except Exception as ex:
    print(ex)
    pass


class LoggingConfig:
    K8S = bool(int(os.environ.get("K8S", '0')))
    SENSITIVE_LEVEL = os.environ.get("LOGGING_SENSITIVE_LEVEL", "normal").lower()  # 0:normal, 1:encrypt, 2:nolog
    SENSITIVE_LEVEL_NORMAL = ['normal', 'n']
    SENSITIVE_LEVEL_ENCRYPT = ['encrypt', 'e', 'encrypted', 'enc']
    SENSITIVE_LEVEL_NOLOG = ['nolog', 'no-log', 'no_log']


class LoggingConstant:
    LOGGING_MODE = "logging_mode"
    WRITE_TRACEBACK_FOR_ALL_CUSTOMIZE_EXCEPTION = "write_traceback_for_all_customize_exception"
    WRITE_TRACEBACK_FOR_GLOBAL_EXCEPTION = "write_traceback_for_global_exception"
    LOG_FOR_REQUEST_SUCCESS = "log_for_request_success"
    LOG_FOR_ALL_CUSTOMIZE_EXCEPTION = "log_for_all_customize_exception"
    LOG_FOR_GLOBAL_EXCEPTION = "log_for_global_exception"
    FILE_MAX_BYTES = "file_max_bytes"
    FILE_BACKUP_COUNT = "file_backup_count"
    DATA_SENSITIVE = {'mbo_sensitive_data': True}
    DATA_NON_SENSITIVE = {'mbo_sensitive_data': False}


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


@Singleton
class MobioLogging:
    def __init__(self):
        self.name = 'MOBIO'

        self.logger = logging.getLogger(self.name)

        log_config_file_path = os.path.join(CONFIG_LOGGING_DIR, 'logging.conf')

        self.file_config(log_config_file_path)

    def file_config(self, config_file_path):
        if not LoggingConfig.K8S:
            logging.config.fileConfig(config_file_path, None, disable_existing_loggers=False)
            pass
        else:
            handler = logging.StreamHandler(stream=sys.stdout)
            if LoggingConfig.K8S:
                handler.setFormatter(LogstashFormatterV1())
            logging.basicConfig(handlers=[handler], level=logging.DEBUG)

    def __mark_data_sensitive(self, content, extra, sensitive=False):
        if sensitive:
            if extra:
                extra.update(LoggingConstant.DATA_SENSITIVE)
            else:
                extra = LoggingConstant.DATA_SENSITIVE

            if LoggingConfig.SENSITIVE_LEVEL in LoggingConfig.SENSITIVE_LEVEL_NOLOG:
                content = None
            elif LoggingConfig.SENSITIVE_LEVEL in LoggingConfig.SENSITIVE_LEVEL_ENCRYPT:
                pass
        else:
            if extra:
                extra.update(LoggingConstant.DATA_NON_SENSITIVE)
            else:
                extra = LoggingConstant.DATA_NON_SENSITIVE

        return extra, content

    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # # On some versions of IronPython, currentframe() returns None if
        # # IronPython isn't run with -X:Frames.
        # if f is not None:
        #     f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        _srcfile = os.path.abspath(__file__)
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def warning(self, content, *args, sensitive=False, **kwargs):
        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('exc_info', False)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        extra, content = self.__mark_data_sensitive(content, extra, sensitive)

        if content is not None:
            record = self.logger.makeRecord(self.name, WARNING, fn, lno, content, args,
                                            exc_info, func, extra, sinfo)
            self.logger.handle(record)

    def debug(self, content, *args, sensitive=False, **kwargs):
        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('exc_info', False)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        extra, content = self.__mark_data_sensitive(content, extra, sensitive)

        if content is not None:
            record = self.logger.makeRecord(self.name, DEBUG, fn, lno, content, args,
                                            exc_info, func, extra, sinfo)
            self.logger.handle(record)

    def error(self, content, *args, sensitive=False, **kwargs):
        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('exc_info', True)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        extra, content = self.__mark_data_sensitive(content, extra, sensitive)

        if content is not None:
            record = self.logger.makeRecord(self.name, ERROR, fn, lno, content, args,
                                            exc_info, func, extra, sinfo)
            self.logger.handle(record)
        # self.logger.error(content, exc_info=True)

    def info(self, content, *args, sensitive=False, **kwargs):
        try:
            fn, lno, func, sinfo = self.findCaller()
        except ValueError:  # pragma: no cover
            fn, lno, func, sinfo = "(unknown file)", 0, "(unknown function)", None

        exc_info = kwargs.get('exc_info', False)

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
                if exc_info[0] is None and exc_info[1] is None:
                    exc_info = False

        extra = kwargs.get('extra', None)
        extra, content = self.__mark_data_sensitive(content, extra, sensitive)

        if content is not None:
            record = self.logger.makeRecord(self.name, INFO, fn, lno, content, args,
                                            exc_info, func, extra, sinfo)
            self.logger.handle(record)

    def exception(self, content):
        self.logger.exception(content)


if __name__ == '__main__':
    def test():
        MobioLogging().info('app_test_lib_logging::test():info', sensitive=True, extra={"key1": "value1"})
        try:
            a = 1 / 0
            MobioLogging().info('__init__::test():a: %s' % a)
        except Exception as ex1:
            MobioLogging().error('app_test_lib_logging::test():error: %s' % ex1, sensitive=True)

        MobioLogging().debug('app_test_lib_logging::test():debug')
        MobioLogging().warning('app_test_lib_logging::test():warning', sensitive=False)

    test()
