# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0005_auto_20150328_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tendersattachments',
            name='tender_ident',
            field=models.CharField(max_length=255, null=True, verbose_name='tender_ident', blank=True),
            preserve_default=True,
        ),
    ]
