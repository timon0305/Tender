# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0008_auto_20150329_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenders',
            name='deadline',
            field=models.DateTimeField(verbose_name='deadline'),
            preserve_default=True,
        ),
    ]
