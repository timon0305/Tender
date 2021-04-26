# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150327_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='name',
        ),
        migrations.RemoveField(
            model_name='providercompany',
            name='name',
        ),
        migrations.RemoveField(
            model_name='providerindividual',
            name='name',
        ),
    ]
