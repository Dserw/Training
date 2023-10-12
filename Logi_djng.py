LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style' : '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style' : '{',
        },
        'overbose': {
            'format': '{levelname} {asctime} {message} {pathname} {exc_info} ',
            'style' : '{',

        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'verbose',
            'filter': 'require_debug_false'
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'overbose',
        },
        'secret': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'overbose',
            'email_backend': 'django.core.mail.backends.filebased.EmailBackend',
            'filter': 'require_debug_false'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'general'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['mail_admins', 'errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['secret'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

