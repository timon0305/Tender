# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver

from common.mixin import (GenericModelChoise, GenericModelCompany,
                          GenericModelCommon, GenericModelExpertise)
from notifications.models import notification_model_by_user


def company_name():
    base_name ='test'
    name = base_name
    i = 1
    while User.objects.filter(company_name=name).exists():
        name = '{}{}'.format(base_name, i)
        i += 1
    return name


class User(AbstractUser):
    class Roles(object):
        EMPLOYER = 0
        PROVIDER_INDIVIDUAL = 1
        PROVIDER_COMPANY = 2

        CHOICES = (
            (EMPLOYER, _('Employer')),
            (PROVIDER_INDIVIDUAL, _('Provider Individual')),
            (PROVIDER_COMPANY, _('Provider Company'))
        )

    role = models.IntegerField(choices=Roles.CHOICES, default=Roles.EMPLOYER)
    company_name = models.CharField(_('name'), max_length=70, unique=True, default=company_name)

    def is_employer(self):
        """
        Returns True if user's employer else False
        """
        return self.role == User.Roles.EMPLOYER

    def is_provider(self):
        """
        Returns True if user's provider else False
        """
        roles = [User.Roles.PROVIDER_INDIVIDUAL, User.Roles.PROVIDER_COMPANY]
        return self.role in roles

    @property
    def get_notification_cache_name(self):
        return 'notify_settings_cache::{0}'.format(self.id)

    @property
    def get_mail_cache_name(self):
        return 'mail_settings_cache::{0}'.format(self.id)

    def get_notification_settings(self, prefix='notification'):
        model = notification_model_by_user(self, prefix)
        obj, created = model.objects.get_or_create(user=self)
        return obj

    def __str__(self):
        return self.username


class Experience(GenericModelChoise):
    pass


class BusinessType(GenericModelChoise):
    pass


class Expertise(GenericModelChoise):
    pass


class Turnover(GenericModelChoise):
    pass


class NumberOfEmloyees(GenericModelChoise):
    pass


class Employer(GenericModelCompany, GenericModelCommon):
    user = models.OneToOneField(User, verbose_name=_('user'),
                                limit_choices_to={'role': User.Roles.EMPLOYER},
                                related_name='user_employer')

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'


class ProviderIndividual(GenericModelExpertise, GenericModelCommon):
    user = models.OneToOneField(User, verbose_name=_('user'),
                                limit_choices_to={
                                    'role': User.Roles.PROVIDER_INDIVIDUAL},
                                related_name='user_provider')

    class Meta:
        verbose_name = 'Provider Individual'
        verbose_name_plural = 'Provider Individuals'


class ProviderCompany(GenericModelCompany, GenericModelExpertise,
                      GenericModelCommon):
    user = models.OneToOneField(User, verbose_name=_('user'),
                                limit_choices_to={
                                    'role': User.Roles.PROVIDER_COMPANY},
                                related_name='user_provider_company')

    class Meta:
        verbose_name = 'Provider Company'
        verbose_name_plural = 'Provider Companies'


USER_ROLE_MAP = {
    User.Roles.EMPLOYER: {
        'model': Employer,
        'base_url': 'employer_tenders',
        'reg_tpl': 'accounts/employer_registration.html'
    },
    User.Roles.PROVIDER_COMPANY: {
        'model': ProviderCompany,
        'base_url': 'provider_bids',
        'reg_tpl': 'accounts/provider_registration.html'
    },
    User.Roles.PROVIDER_INDIVIDUAL: {
        'model': ProviderIndividual,
        'base_url': 'provider_bids',
        'reg_tpl': 'accounts/provider_registration.html'
    }
}


@receiver(post_save, sender=User, dispatch_uid='user_notification_settings')
def user_notification_settings(sender, instance=None, created=False, **kwargs):
    if created:
        for prefix in ['notification', 'mail']:
            notification_model = notification_model_by_user(instance, prefix)
            notification_settings = notification_model.objects.create(user=instance)
            cache_name = getattr(instance, 'get_' + prefix + '_cache_name')
            cache.set(cache_name, notification_settings)
