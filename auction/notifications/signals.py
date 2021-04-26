# encoding: utf-8
from __future__ import unicode_literals

from django.dispatch import Signal

notify = Signal(providing_args=[
    'recipients', 'actor', 'verb', 'action_object', 'target', 'description',
    'timestamp', 'email_list'
])
