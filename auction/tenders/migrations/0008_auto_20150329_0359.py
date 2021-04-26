# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0007_bidsattachments_tender_ident'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidsattachments',
            name='tender',
            field=models.ForeignKey(related_name='bidsattachments', blank=True, to='tenders.Bids', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bidsattachments',
            name='tender_ident',
            field=models.CharField(max_length=255, null=True, verbose_name='bids_ident', blank=True),
            preserve_default=True,
        ),
    ]
