# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150217_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='description',
            field=models.TextField(verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providercompany',
            name='description',
            field=models.TextField(verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providerindividual',
            name='description',
            field=models.TextField(verbose_name='Description'),
            preserve_default=True,
        ),
    ]
