import os
import djcelery
from django_markup.filter.markdown_filter import MarkdownMarkupFilter
from diskurs.markdown.giffer import GifferMarkdownFilter

# Django settings for AuroraProject project.

DEBUG = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'database.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '8080',                      # Set to empty string for default.
    },

    'plagcheck': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database-plagcheck.db',
    }
}

DATABASE_ROUTERS = ['PlagCheck.router.PlagCheckRouter']

MARKUP_FILTER = {
    'markdown': MarkdownMarkupFilter,
    'markdown_giffer': GifferMarkdownFilter,
}

MARKUP_SETTINGS = {
    'markdown': {
        'safe_mode': True
    },
    'markdown_giffer': {
        'safe_mode': True
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

if DEBUG:
    MEDIA_ROOT = os.path.curdir
    MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/vagrant/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(os.path.join('static'),),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n@sn@dc_ayzqb2-u3cugqej7a_fj#^$b9$8h(m$r!us_oxz!d3'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\', '/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.exception_logging_middleware.ExceptionLoggingMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'middleware.AuroraAuthenticationBackend.AuroraAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'AuroraProject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'AuroraProject.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'suit',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.humanize',
    # third party apps
    'easy_thumbnails',
    'django_comments',
    'django_comments_xtd',
    # 'memoize',
    # own apps
    'AuroraUser',
    'Challenge',
    'Course',
    'Elaboration',
    'Stack',
    'Evaluation',
    'Review',
    'ReviewQuestion',
    'ReviewAnswer',
    'FileUpload',
    'Comments',
    'Slides',
    'Statistics',
    'Notification',
    'el_pagination',
    'taggit',
    'Faq',
    'djcelery',
    'PlagCheck',
    'diskurs',
    'django_markup',
    'Feedback'
)

THUMBNAIL_ALIASES = {
    '': {
        'preview': {'size': (640, 480)},
        'full-res': {'size': (1920, 1080)},
    },
}

## COMMENTS ##

COMMENTS_APP = 'django_comments_xtd'

# Either enable sending mail messages to the console:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Or set up the EMAIL_* settings so that Django can send emails:
#EMAIL_HOST = "smtp.mail.com"
#EMAIL_PORT = "587"
#EMAIL_HOST_USER = "alias@mail.com"
#EMAIL_HOST_PASSWORD = "yourpassword"
#EMAIL_USE_TLS = True
#DEFAULT_FROM_EMAIL = "Helpdesk <helpdesk@yourdomain>"

COMMENTS_XTD_CONFIRM_MAIL = False
COMMENTS_XTD_MAX_THREAD_LEVEL = 2



TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'timed': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'review': {
            'format': '%(asctime)s - %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*10,
            'backupCount': 1,
            'filename': '/tmp/aurora.log',
            'formatter': 'timed',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'timed'
        },
	'review_candidate': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*10,
            'backupCount': 1,
            'filename': os.path.dirname(PROJECT_ROOT) + '/AuroraUser/log/review_candidate.log',
            'formatter': 'review',
        },
    },
    'loggers': {} # loggers are set below
}

# production log handling
if not DEBUG:
    LOGGING['loggers'] = {
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # django logs
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Review logs
        'review': {
            'handlers': ['review_candidate'],
            'level': 'INFO',
            'propagate': False,
        },
        # python logs
        '': {
            'handlers': ['file'],
            'level': 'CRITICAL',
            'propagate': True,
        },
    }
# debug log handling
else:
    LOGGING['loggers'] = {
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # django logs
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Review logs
        'review': {
            'handlers': ['review_candidate'],
            'level': 'INFO',
            'propagate': False,
        },
        # python logs
        '': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }


LOGIN_URL = '/course/{{course}}/login'

EL_PAGINATION_PER_PAGE = (
    20
)
EL_PAGINATION_PREVIOUS_LABEL = (
    '<div class="paginator prev"><i class="fa fa-angle-double-left"></i> prev</div>'
)
EL_PAGINATION_NEXT_LABEL = (
    '<div class="paginator next">next <i class="fa fa-angle-double-right"></i></div>'
)

PLAGCHECK = {
    # a document scanned by PlagCheck needs to have the same or higher similarity percentage
    # than PLAGCHECK_SIMILARITY_THRESHOLD_PERCENT's value to be reported as a possible
    # plagiarism.
    'similarity_threshold': 50,

    # discards suspects whose matching hashes count is not greater than this
    'minimal_match_count': 10,

    # connection name for separation from default database
    'database': 'plagcheck',

    'suspicion_filters': [
        'PlagCheck.filters.SimilarityThresholdFilter',
        'PlagCheck.filters.MinimalMatchCountFilter',
        'PlagCheck.filters.RevisedElaborationFilter',
        'PlagCheck.filters.SelfPlagiarismFilter',
        'PlagCheck.filters.DummyUserFilter',
    ]
}

CELERY_ALWAYS_EAGER=False # set to True by unit tests
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'db+postgresql://user:pass@host/plagcheck-db'

if DEBUG:
    # The monitors currently doesn't work with the Django broker.
    #
    # Means we can't use celerymon/flower monitor the django message broker, instead to properly
    # monitor and debug events we need to use RabbitMQ message broker locally.
    #
    # Enable USE_DJANGO_BROKER to entirely run PlagCheck inside django, without RabbitMQ.
    #
    # http://stackoverflow.com/questions/5449163/django-celery-admin-interface-showing-zero-tasks-workers

    USE_DJANGO_BROKER = False

    if USE_DJANGO_BROKER is True:
        CELERY_BROKER_BACKEND = "django"
        CELERY_BROKER_URL = 'django://'

    # kombu is used to use djangos database as message broker while debugging
    #INSTALLED_APPS += ('kombu.transport.django',)

    djcelery.setup_loader()

    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

    ## DEBUG TOOLBAR ##

    def show_toolbar(request):
        return not request.is_ajax() and 'toolbar' in request.GET

    #INTERNAL_IPS = ('127.0.0.1', '10.0.0.11')

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': False,
        'SHOW_TOOLBAR_CALLBACK': 'AuroraProject.settings.show_toolbar',
    }

    ## PROFILING ##
    MIDDLEWARE_CLASSES += (
        'middleware.Profiling.ProfileMiddleware',
    )

try:
    from local_settings import *
except ImportError:
    pass
