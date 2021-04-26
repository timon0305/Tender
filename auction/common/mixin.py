# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pytz import timezone


class GenericModelChoise(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title.encode('utf-8')


class GenericModelCommon(models.Model):
    logo = models.ImageField(_('Image/Logo'), upload_to='account/logo',
                             blank=True, null=True)
    description = models.TextField(_('Description'))
    facebook = models.CharField(_('Facebook'), blank=True, null=True,
                                max_length=200)
    twitter = models.CharField(_('Twitter'), blank=True, null=True,
                               max_length=200)
    google = models.CharField(_('Google+'), blank=True, null=True,
                              max_length=200)
    linkedin = models.CharField(_('LinkedIn'), blank=True, null=True,
                                max_length=200)

    class Meta:
        abstract = True


class GenericModelCompany(models.Model):
    business_type = models.ForeignKey('accounts.BusinessType',
                                      verbose_name=_('Business Type'),
                                      limit_choices_to={'is_active': True})
    turnover = models.ForeignKey('accounts.Turnover',
                                 verbose_name=_('Turnover'),
                                 limit_choices_to={'is_active': True})
    number_of_emloyees = models.ForeignKey(
        'accounts.NumberOfEmloyees',
        verbose_name=_('Number of Emloyees'),
        limit_choices_to={'is_active': True}
    )

    class Meta:
        abstract = True


class GenericModelExpertise(models.Model):
    year = models.ForeignKey('accounts.Experience',
                             verbose_name=_('Years of Experience'),
                             limit_choices_to={'is_active': True})
    expertise = models.ManyToManyField('accounts.Expertise',
                                       limit_choices_to={'is_active': True})

    class Meta:
        abstract = True


class AccountMixinAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_filter = ('is_active',)


def datetime_convert(date, timezone_to, timezone_from=None):
    try:
        date = date.replace(tzinfo=None) if timezone_from else timezone('UTC').localize(date)
    finally:
        try:
            date = timezone(timezone_from).localize(date)
        finally:
            return date.astimezone(timezone(timezone_to))
