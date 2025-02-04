from loguru import logger
import sys
import logging
from datetime import datetime

# 定义统一的日志格式字符串
log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}"

# 配置 Loguru，移除默认的日志配置
logger.remove()

# 使用统一的日志格式配置标准输出和标准错误输出，支持彩色显示
logger.add(sys.stdout, level="DEBUG", format=log_format, colorize=True)
logger.add(sys.stderr, level="ERROR", format=log_format, colorize=True)

# 同样使用统一的格式配置日志文件输出，设置文件大小为1MB自动轮换
logger.add("logs/app.log", rotation="1 MB", level="DEBUG", format=log_format)

# 为 logger 设置别名，方便在其他模块中导入和使用
LOG = logger

# 将 LOG 变量公开，允许其他模块通过 from logger import LOG 来使用它
__all__ = ["LOG"]

class ColoredFormatter(logging.Formatter):
    """自定义的彩色日志格式器"""
    
    # ANSI转义序列颜色代码
    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"

    # 不同日志级别对应的格式
    FORMATS = {
        logging.DEBUG: blue + "%(asctime)s [%(levelname)s] %(message)s" + reset,
        logging.INFO: green + "%(asctime)s [%(levelname)s] %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s [%(levelname)s] %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s [%(levelname)s] %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s [%(levelname)s] %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def setup_logger():
    """配置日志记录器"""
    logger = logging.getLogger('github_tracker')
    logger.setLevel(logging.DEBUG)

    # 如果已经有处理器，先清除
    if logger.handlers:
        logger.handlers.clear()

    # 控制台处理器（带颜色）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    # 文件处理器（不带颜色）
    file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', 
                         datefmt='%Y-%m-%d %H:%M:%S')
    )
    logger.addHandler(file_handler)

    return logger


# 创建全局日志记录器
LOG = setup_logger()