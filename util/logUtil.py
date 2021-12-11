import logging
import logging.config as log_conf
import os

log_dir = os.path.dirname(__file__) + '/../logs/'
# 创建日志文件
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_config = {
    'version': 1.0,
    # "disable_existing_loggers": False,
    'formatters': {
        'detail': {
            'format': '%(asctime)s %(pathname)s %(processName)s  %(lineno)s  %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detail',
            # "stream": "ext://sys.stdout"
        },
        'scheudle': {
            # 'class': 'logging.handlers.MultiProcessSafeDailyRotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 1024 * 1,
            'backupCount': 7,
            'filename': log_dir + 'scheudle.log',
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'formatter': 'detail'
        },
        'download': {
            # 'class': 'logging.handlers.MultiProcessSafeDailyRotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 1024 * 1,
            'backupCount': 7,
            'filename': log_dir + 'download.log',
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'formatter': 'detail'
        },
        'parse': {
            # 'class': 'logging.handlers.MultiProcessSafeDailyRotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 1024 * 1,
            'backupCount': 7,
            'filename': log_dir + 'parse.log',
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'formatter': 'detail'
        },
        'queue': {
            # 'class': 'logging.handlers.MultiProcessSafeDailyRotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 1024 * 1,
            'backupCount': 7,
            'filename': log_dir + 'queue.log',
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'formatter': 'detail'
        },
        'except': {
            # 'class': 'logging.handlers.MultiProcessSafeDailyRotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 1024 * 1,
            'backupCount': 7,
            'filename': log_dir + 'except.log',
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'formatter': 'detail'
        },
        'plugin': {
            # 'class': 'logging.handlers.MultiProcessSafeDailyRotatingFileHandler',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            # 'maxBytes': 1024 * 1024 * 1024 * 1,
            'backupCount': 7,
            'filename': log_dir + 'plugin.log',
            'level': 'DEBUG',
            'encoding': 'utf-8',
            'when': 'D',
            'interval': 1,
            'formatter': 'detail'
        },
    },
    'loggers': {
        'scheudle': {
            'handlers': ['scheudle'],
            'level': 'DEBUG',
        },
        'download': {
            'handlers': ['download'],
            'level': 'DEBUG',
        },
        'parse': {
            'handlers': ['parse'],
            'level': 'DEBUG',
        },
        'queue': {
            'handlers': ['queue'],
            'level': 'DEBUG',
        },
        'except': {
            'handlers': ['except'],
            'level': 'DEBUG',
        },
        'plugin': {
            'handlers': ['plugin'],
            'level': 'DEBUG',
        },

    }
}

log_conf.dictConfig(log_config)
schedule_log = logging.getLogger('scheudle')
download_log = logging.getLogger('download')
parse_log = logging.getLogger('parse')
queue_log = logging.getLogger('queue')
except_log = logging.getLogger('except')
plugin_log = logging.getLogger('plugin')
