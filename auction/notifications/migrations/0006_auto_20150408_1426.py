# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20150408_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailnotification',
            name='action_object_content_type',
            field=models.ForeignKey(related_name='mailnotification_action_object', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailnotification',
            name='actor_content_type',
            field=models.ForeignKey(related_name='mailnotification_actor', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailnotification',
            name='recipient',
            field=models.ForeignKey(related_name='mailnotification', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailnotification',
            name='target_content_type',
            field=models.ForeignKey(related_name='mailnotification_target', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='action_object_content_type',
            field=models.ForeignKey(related_name='notification_action_object', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='actor_content_type',
            field=models.ForeignKey(related_name='notification_actor', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(related_name='notification', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(related_name='notification_target', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
