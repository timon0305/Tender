# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_auto_20150617_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailprovidersettings',
            name='cancel_invite',
            field=models.BooleanField(default=True, verbose_name='Cancel invite to Tender'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mailprovidersettings',
            name='invite_to_tender',
            field=models.BooleanField(default=True, verbose_name='Invite to Tender'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificationprovidersettings',
            name='cancel_invite',
            field=models.BooleanField(default=True, verbose_name='Cancel invite to Tender'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificationprovidersettings',
            name='invite_to_tender',
            field=models.BooleanField(default=True, verbose_name='Invite to Tender'),
            preserve_default=True,
        ),
    ]
