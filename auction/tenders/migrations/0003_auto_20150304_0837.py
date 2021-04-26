# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenders', '0002_tenders_is_withdraw'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidsAttachments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to='bids/%Y/%m/%d')),
                ('tender', models.ForeignKey(related_name='bidsattachments', to='tenders.Bids')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='attachments',
            name='bids',
        ),
        migrations.RemoveField(
            model_name='attachments',
            name='tender',
        ),
        migrations.DeleteModel(
            name='Attachments',
        ),
    ]
