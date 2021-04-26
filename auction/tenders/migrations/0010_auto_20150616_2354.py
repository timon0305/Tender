# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenders', '0009_auto_20150406_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitedProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider_email', models.EmailField(max_length=75, verbose_name='email address of provider')),
                ('employer', models.ForeignKey(related_name='tender_own', to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(related_name='invited_provider', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('tender', models.ForeignKey(to='tenders.Tenders')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tenders',
            name='type_public',
            field=models.IntegerField(default=1, verbose_name='public type', choices=[(1, 'Public (a Public tender is visible to everyone. Any Service Provider can view and bid)'), (2, 'Private (a Private tender is only visible to Service Provides invited by the employer)')]),
            preserve_default=True,
        ),
    ]
