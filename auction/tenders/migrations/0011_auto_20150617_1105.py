# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0010_auto_20150616_2354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitedprovider',
            old_name='employer',
            new_name='user',
        ),
    ]
