import os
from conf.base.base import BASE_DIR


LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO').upper()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{asctime}] {levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{BASE_DIR}/log/djam.log',
            'maxBytes': 1024*1024*5,    # max 5 MB per file
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'apps': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'file'],
            'propagate': True,
        }
    },
}
