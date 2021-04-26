# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0009_auto_20150618_0209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailprovidersettings',
            name='cancel_invite',
        ),
        migrations.RemoveField(
            model_name='mailprovidersettings',
            name='invite_to_tender',
        ),
    ]
