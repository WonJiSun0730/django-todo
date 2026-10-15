from .settings import *

# Explicit isolated test option; application settings always use MySQL.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
