# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0011_auto_20150617_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenders',
            name='type_public',
            field=models.IntegerField(default=1, verbose_name='public type', choices=[(2, 'Private (a Private tender is only visible to Service Provides invited by the employer)'), (1, 'Public (a Public tender is visible to everyone. Any Service Provider can view and bid)')]),
            preserve_default=True,
        ),
    ]
