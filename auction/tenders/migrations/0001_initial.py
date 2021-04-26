# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone
from django.conf import settings
import common.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to='tenders/files', verbose_name='file')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('price', common.fields.CurrencyField(verbose_name='best price', max_digits=15, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Bid',
                'verbose_name_plural': 'Bids',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tenders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('deadline', models.DateField(verbose_name='deadline')),
                ('type', models.IntegerField(default=0, verbose_name='type of tender', choices=[(0, 'Open view'), (1, 'Employer view'), (2, 'Closed view')])),
                ('description', models.TextField(verbose_name='project description')),
                ('count_bids', models.PositiveIntegerField(default=0, verbose_name='count bids')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('industry', models.ForeignKey(related_name='industry_tenders', verbose_name='industry', to='tenders.Industry')),
                ('user', models.ForeignKey(related_name='user_tenders', verbose_name='employer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tender',
                'verbose_name_plural': 'Tenders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TendersAttachments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to='tenders/%Y/%m/%d')),
                ('tender', models.ForeignKey(related_name='tendersattachments', to='tenders.Tenders')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bids',
            name='tender',
            field=models.ForeignKey(related_name='tender_bids', verbose_name='tender', to='tenders.Tenders'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(related_name='user_bids', verbose_name='provider', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='bids',
            unique_together=set([('user', 'tender')]),
        ),
        migrations.AddField(
            model_name='attachments',
            name='bids',
            field=models.ForeignKey(verbose_name='bid', blank=True, to='tenders.Bids', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachments',
            name='tender',
            field=models.ForeignKey(verbose_name='tender', blank=True, to='tenders.Tenders', null=True),
            preserve_default=True,
        ),
    ]
