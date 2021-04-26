# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_mailnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='send_to_email',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='view_on_page',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
