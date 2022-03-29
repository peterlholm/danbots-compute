"Debug settings"
# debug settings
#
DEBUG = True

NN_ENABLE=False

#MYDEVICE = "b827eb05abc2"
#print('NN_ENABLE', NN_ENABLE)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/danbots/info.log',
            'formatter': 'verbose',
            },
    },

    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
