from .base import *

DEBUG = True

SECRET_KEY = 'b3r)sn9!9-muzn0c^mt+8p^*h)5qnxtnvb2gvk*=!3vo$#*i&f'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += (
    # 'debug_toolbar',
)

try:
    from .local import *
except ImportError:
    pass
