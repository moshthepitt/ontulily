"""
The test runner
"""

import os

from django_micro import configure, run
from ontulily.tests.test_flood import *  # noqa

# Configuration
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TEST_DIR, 'db.sqlite3'),
    },
}

configure(locals(), django_admin=False)

# Expose application
application = run()
