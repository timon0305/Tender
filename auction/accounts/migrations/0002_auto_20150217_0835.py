# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='years',
        ),
        migrations.AddField(
            model_name='experience',
            name='title',
            field=models.CharField(default=1, max_length=255, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(default=0, choices=[(0, 'Employer'), (1, 'Provider Individual'), (2, 'Provider Company')]),
            preserve_default=True,
        ),
    ]
