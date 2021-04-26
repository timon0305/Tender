# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel

from accounts.models import User
from common.fields import CurrencyField
from common.mixin import GenericModelChoise


def limit_role_choices():
    return {
        'role__in': [User.Roles.PROVIDER_COMPANY,
                     User.Roles.PROVIDER_INDIVIDUAL]
    }


class Industry(GenericModelChoise):
    pass


@python_2_unicode_compatible
class Tenders(TimeStampedModel):
    class Types(object):
        OPEN = 0
        EMPLOYER = 1
        CLOSED = 2

        CHOICES = (
            (OPEN, _('Open view')),
            (EMPLOYER, _('Employer view')),
            (CLOSED, _('Closed view'))
        )

    class TypesPublic(object):
        PUBLIC = 1
        PRIVATE = 2

        CHOICES = (
            (PRIVATE, _('Private (a Private tender is only visible to Service Provides invited by the employer)')),
            (PUBLIC, _('Public (a Public tender is visible to everyone. Any Service Provider can view and bid)')),
        )

    user = models.ForeignKey(User, verbose_name=_('employer'),
                             related_name='user_tenders',
                             limit_choices_to={'role': User.Roles.EMPLOYER})
    title = models.CharField(_('title'), max_length=255)
    deadline = models.DateTimeField(_('deadline'))
    type = models.IntegerField(_('type of tender'), choices=Types.CHOICES,
                               default=Types.OPEN)
    type_public = models.IntegerField(('public type'),
                                      choices=TypesPublic.CHOICES,
                                      default=TypesPublic.PUBLIC)
    industry = models.ForeignKey(Industry, verbose_name=_('industry'),
                                 related_name='industry_tenders',
                                 limit_choices_to={'is_active': True})
    description = models.TextField(_('project description'))
    count_bids = models.PositiveIntegerField(_('count bids'), default=0)
    is_active = models.BooleanField(_('active'), default=True)
    is_withdraw = models.BooleanField(default=False)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse_lazy('employer-tender-detail', kwargs={'pk': self.pk})

    @property
    def is_expired(self):
        return now() > self.deadline

    class Meta:
        verbose_name = _('Tender')
        verbose_name_plural = _('Tenders')

    def __str__(self):
        return self.title


class BidsManager(models.Manager):
    def is_able_bid(self, user, tender_id):
        return self.filter(user=user, tender_id=tender_id).exists()


class Bids(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name=_('provider'),
                             related_name='user_bids',
                             limit_choices_to=limit_role_choices())
    tender = models.ForeignKey(Tenders, verbose_name=_('tender'),
                               related_name='tender_bids')
    price = CurrencyField(_('best price'))

    objects = BidsManager()

    class Meta:
        verbose_name = _('Bid')
        verbose_name_plural = _('Bids')
        unique_together = ('user', 'tender')


@python_2_unicode_compatible
class TendersAttachments(models.Model):
    user = models.ForeignKey(User,
                             limit_choices_to={'role': User.Roles.EMPLOYER},
                             blank=True, null=True)
    tender = models.ForeignKey(Tenders, related_name='tendersattachments',
                               blank=True, null=True)
    tender_ident = models.CharField(_('tender_ident'), blank=True, null=True,
                                    max_length=255)
    file = models.FileField(upload_to='tenders/%Y/%m/%d')

    def __str__(self):
        return self.file.name.split('/')[-1]


@python_2_unicode_compatible
class BidsAttachments(models.Model):
    user = models.ForeignKey(User)
    tender = models.ForeignKey(Bids, related_name='bidsattachments',
                               blank=True, null=True)
    file = models.FileField(upload_to='bids/%Y/%m/%d')
    tender_ident = models.CharField(_('bids_ident'), blank=True, null=True,
                                    max_length=255)

    def __str__(self):
        return self.file.name.split('/')[-1]


@python_2_unicode_compatible
class InvitedProvider(models.Model):
    provider = models.ForeignKey(User, blank=True, null=True,
                                 related_name='invited_provider')
    user = models.ForeignKey(User, related_name='tender_own')
    tender = models.ForeignKey(Tenders)
    provider_email = models.EmailField(_('email address of provider'))

    def __str__(self):
        return self.provider_email


@receiver(post_save, sender=Bids, dispatch_uid='post_bids')
def post_bids(sender, instance=None, created=False, **kwargs):
    tender = instance.tender
    tender.count_bids = Bids.objects.filter(tender=tender).count()
    tender.save(update_fields=['count_bids'])