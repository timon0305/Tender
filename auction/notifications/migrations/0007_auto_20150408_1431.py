# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20150408_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailnotification',
            name='recipient',
            field=models.ForeignKey(related_name='mailnotifications', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(related_name='notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
