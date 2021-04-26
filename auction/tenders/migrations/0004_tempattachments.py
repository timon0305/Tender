# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0003_auto_20150304_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempAttachments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tender_ident', models.IntegerField(verbose_name='tender_ident')),
                ('file', models.FileField(upload_to='tenders/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
