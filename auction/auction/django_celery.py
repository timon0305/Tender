# encoding: utf-8
from __future__ import unicode_literals, absolute_import
import os

from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings.local')

app = Celery('auction')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
