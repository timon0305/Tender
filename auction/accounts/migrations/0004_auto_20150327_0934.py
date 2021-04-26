# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150226_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='logo',
            field=models.ImageField(upload_to='account/logo', null=True, verbose_name='Image/Logo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providercompany',
            name='logo',
            field=models.ImageField(upload_to='account/logo', null=True, verbose_name='Image/Logo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providerindividual',
            name='logo',
            field=models.ImageField(upload_to='account/logo', null=True, verbose_name='Image/Logo', blank=True),
            preserve_default=True,
        ),
    ]
