from djangoProject.settings import DATABASES, INSTALLED_APPS
from .settings import *

INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']

MIDDLEWARE = [mw for mw in MIDDLEWARE if mw != 'debug.toolbar.middleware.DebugTooldbarMiddleware']

DATABASES = {
    'default':{
        'ENGINE':"django.db.backends.sqlite3",
        'NAME':'memory'
    }
}

CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.dummy.DummyCache'
    }
}

LOGGING = {
    'version':1,
    'disable_existing_logger':False,
    'handlers':{
        'console':{
            'class':'logging.StreamHandler'
        },
    },
    'root':{
        "handler":['console'],
        'level':'CRITICAL'
    },
}