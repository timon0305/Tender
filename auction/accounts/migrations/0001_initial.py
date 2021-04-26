# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.IntegerField(default=0, choices=[(0, 'Employer'), (1, 'Provider')])),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusinessType',
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
            name='Employer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('logo', models.ImageField(upload_to='account/logo', verbose_name='Image/Logo')),
                ('description', models.TextField(verbose_name='Description of Company')),
                ('facebook', models.URLField(null=True, verbose_name='Facebook', blank=True)),
                ('twitter', models.URLField(null=True, verbose_name='Twitter', blank=True)),
                ('google', models.URLField(null=True, verbose_name='Google+', blank=True)),
                ('linkedin', models.URLField(null=True, verbose_name='LinkedIn', blank=True)),
                ('business_type', models.ForeignKey(verbose_name='Business Type', to='accounts.BusinessType')),
            ],
            options={
                'verbose_name': 'Employer',
                'verbose_name_plural': 'Employers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('years', models.PositiveIntegerField(verbose_name='Year')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Expertise',
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
            name='NumberOfEmloyees',
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
            name='ProviderCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('logo', models.ImageField(upload_to='account/logo', verbose_name='Image/Logo')),
                ('description', models.TextField(verbose_name='Description of Company')),
                ('facebook', models.URLField(null=True, verbose_name='Facebook', blank=True)),
                ('twitter', models.URLField(null=True, verbose_name='Twitter', blank=True)),
                ('google', models.URLField(null=True, verbose_name='Google+', blank=True)),
                ('linkedin', models.URLField(null=True, verbose_name='LinkedIn', blank=True)),
                ('business_type', models.ForeignKey(verbose_name='Business Type', to='accounts.BusinessType')),
                ('expertise', models.ManyToManyField(to='accounts.Expertise')),
                ('number_of_emloyees', models.ForeignKey(verbose_name='Number of Emloyees', to='accounts.NumberOfEmloyees')),
            ],
            options={
                'verbose_name': 'Provider Company',
                'verbose_name_plural': 'Provider Companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProviderIndividual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('logo', models.ImageField(upload_to='account/logo', verbose_name='Image/Logo')),
                ('description', models.TextField(verbose_name='Description of Company')),
                ('facebook', models.URLField(null=True, verbose_name='Facebook', blank=True)),
                ('twitter', models.URLField(null=True, verbose_name='Twitter', blank=True)),
                ('google', models.URLField(null=True, verbose_name='Google+', blank=True)),
                ('linkedin', models.URLField(null=True, verbose_name='LinkedIn', blank=True)),
                ('expertise', models.ManyToManyField(to='accounts.Expertise')),
                ('user', models.OneToOneField(related_name='user_provider', verbose_name='user', to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(verbose_name='Years of Experience', to='accounts.Experience')),
            ],
            options={
                'verbose_name': 'Provider Individual',
                'verbose_name_plural': 'Provider Individuals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Turnover',
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
        migrations.AddField(
            model_name='providercompany',
            name='turnover',
            field=models.ForeignKey(verbose_name='Turnover', to='accounts.Turnover'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='providercompany',
            name='user',
            field=models.OneToOneField(related_name='user_provider_company', verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='providercompany',
            name='year',
            field=models.ForeignKey(verbose_name='Years of Experience', to='accounts.Experience'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employer',
            name='number_of_emloyees',
            field=models.ForeignKey(verbose_name='Number of Emloyees', to='accounts.NumberOfEmloyees'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employer',
            name='turnover',
            field=models.ForeignKey(verbose_name='Turnover', to='accounts.Turnover'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employer',
            name='user',
            field=models.OneToOneField(related_name='user_employer', verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
