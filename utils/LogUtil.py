import logging
import colorlog


class Logger(object):

    def __init__(self, log_path, level=logging.DEBUG, when='D', backCount=3,
                 fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s'):
        ### Console Logger ###
        # 输出到控制台
        # 控制台logger
        self._logger_console = logging.getLogger('logger_console')
        # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
        self._logger_console.setLevel(level)
        # 输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors={
                'DEBUG': 'white',  # cyan white
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            })
        console_handler.setFormatter(console_formatter)
        self._logger_console.addHandler(console_handler)

        ### File Logger ###
        # 输出到文件
        # 文件logger
        self._logger_file = logging.getLogger('logger_file')
        # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
        self._logger_file.setLevel(level)
        # 输出到文件
        file_handler = logging.FileHandler(filename=log_path, mode='a', encoding='utf8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self._logger_file.addHandler(file_handler)

    def debug(self, msg):
        self._logger_console.debug(msg)
        self._logger_file.debug(msg)

    def info(self, msg):
        self._logger_console.info(msg)
        self._logger_file.info(msg)

    def warning(self, msg):
        self._logger_console.warning(msg)
        self._logger_file.warning(msg)

    def error(self, msg):
        self._logger_console.error(msg)
        self._logger_file.error(msg)

    def fatal(self, msg):
        self._logger_console.fatal(msg)
        self._logger_file.fatal(msg)
