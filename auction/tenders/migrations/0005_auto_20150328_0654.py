# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0004_tempattachments'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TempAttachments',
        ),
        migrations.AddField(
            model_name='tendersattachments',
            name='tender_ident',
            field=models.IntegerField(null=True, verbose_name='tender_ident', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tendersattachments',
            name='tender',
            field=models.ForeignKey(related_name='tendersattachments', blank=True, to='tenders.Tenders', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tendersattachments',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
