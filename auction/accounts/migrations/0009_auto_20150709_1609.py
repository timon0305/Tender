# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20150618_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='facebook',
            field=models.CharField(max_length=200, null=True, verbose_name='Facebook', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employer',
            name='google',
            field=models.CharField(max_length=200, null=True, verbose_name='Google+', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employer',
            name='linkedin',
            field=models.CharField(max_length=200, null=True, verbose_name='LinkedIn', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employer',
            name='twitter',
            field=models.CharField(max_length=200, null=True, verbose_name='Twitter', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providercompany',
            name='facebook',
            field=models.CharField(max_length=200, null=True, verbose_name='Facebook', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providercompany',
            name='google',
            field=models.CharField(max_length=200, null=True, verbose_name='Google+', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providercompany',
            name='linkedin',
            field=models.CharField(max_length=200, null=True, verbose_name='LinkedIn', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providercompany',
            name='twitter',
            field=models.CharField(max_length=200, null=True, verbose_name='Twitter', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providerindividual',
            name='facebook',
            field=models.CharField(max_length=200, null=True, verbose_name='Facebook', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providerindividual',
            name='google',
            field=models.CharField(max_length=200, null=True, verbose_name='Google+', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providerindividual',
            name='linkedin',
            field=models.CharField(max_length=200, null=True, verbose_name='LinkedIn', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='providerindividual',
            name='twitter',
            field=models.CharField(max_length=200, null=True, verbose_name='Twitter', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='company_name',
            field=models.CharField(default=accounts.models.company_name, unique=True, max_length=70, verbose_name='name'),
            preserve_default=True,
        ),
    ]
