#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import call_command


def runtests():
    if not settings.configured:
        settings.configure(
            SECRET_KEY='123',
            DIRNAME=os.path.dirname(os.path.abspath(__file__)),
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=(
                'sluggable',
                'sluggable.tests',
            )
        )
    django.setup()
    failures = call_command('test', interactive=False, failfast=False,
                            verbosity=2)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
