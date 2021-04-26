# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_mailnotification_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailnotification',
            name='emailed',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='emailed',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='send_to_email',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='view_on_page',
        ),
    ]
