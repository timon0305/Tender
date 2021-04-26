# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
from django.core.cache import cache

from .signals import notify

notify_cache_name = lambda user_id: 'user_notif_settings::%s'.format(user_id)

NOTIFICATION_MAP_FIELDS = {
    'change_tender': 'changed in tender',
    'withdraw_tender': 'withdrew tender',
    'end_tender': 'closed tender',
    'new_bid': 'created a new bid',
    'change_bid': 'changed bid',
    'withdraw_bid': 'withdrew bid',
    'invite_to_tender': 'invited to tender',
    'cancel_invite': 'canceled invite to tender'
}


class NotificationManager(models.Manager):
    def unread(self):
        return self.filter(unread=True)

    def mark_all_as_read(self, recipient=None):
        """Marks all unread notifications as read

        :param recipient: user object
        :return: result of method QS 'update'
        """
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        return qs.update(unread=False)


class NotificationAbstract(TimeStampedModel):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='%(class)ss',
                                  blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    actor_content_type = models.ForeignKey(ContentType,
                                           related_name='%(class)s_actor')
    actor_object_id = models.CharField(max_length=255)
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    target_content_type = models.ForeignKey(ContentType,
                                            related_name='%(class)s_target',
                                            blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type',
                                       'target_object_id')

    action_object_content_type = models.ForeignKey(
        ContentType, related_name='%(class)s_action_object', blank=True,
        null=True
    )
    action_object_object_id = models.CharField(max_length=255, blank=True,
                                               null=True)
    action_object = generic.GenericForeignKey('action_object_content_type',
                                              'action_object_object_id')

    public = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Notification(NotificationAbstract):
    unread = models.BooleanField(default=True, blank=False)
    deleted = models.BooleanField(default=False)

    def timesince(self):
        from django.utils.timesince import timesince as ts
        from django.utils.timezone import now

        return ts(self.created, now())

    objects = NotificationManager()

    class Meta:
        ordering = ('-created', )


class MailNotification(NotificationAbstract):
    pass


class EmployerSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    change_bid = models.BooleanField(_('Change bid'), default=True)
    new_bid = models.BooleanField(_('New bid'), default=True)
    withdraw_bid = models.BooleanField(_('Withdraw bid'), default=True)
    end_tender = models.BooleanField(_('End of Tender'), default=True)

    class Meta:
        abstract = True


class ProviderSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    change_tender = models.BooleanField(_('Change in Tender'), default=True)
    withdraw_tender = models.BooleanField(_('Withdraw of Tender'), default=True)
    end_tender = models.BooleanField(_('End of Tender'), default=True)

    class Meta:
        abstract = True


class NotificationEmployerSettings(EmployerSettings):
    pass


class NotificationProviderSettings(ProviderSettings):
    invite_to_tender = models.BooleanField(_('Invite to Tender'), default=True)
    cancel_invite = models.BooleanField(_('Cancel invite to Tender'),
                                        default=True)


class MailEmployerSettings(EmployerSettings):
    pass


class MailProviderSettings(ProviderSettings):
    pass


SETTING_MODELS_MAP = {
    'notification': {
        'employer': NotificationEmployerSettings,
        'provider': NotificationProviderSettings,
    },
    'mail': {
        'employer': MailEmployerSettings,
        'provider': MailProviderSettings,
    }
}


def notification_model_by_user(user, prefix='notification'):
    if user.is_employer():
        model = SETTING_MODELS_MAP[prefix]['employer']
    elif user.is_provider():
        model = SETTING_MODELS_MAP[prefix]['provider']
    else:
        raise SuspiciousOperation
    return model


def check_recipient_settings(user, verb, prefix='notification'):
    cache_name = getattr(user, 'get_' + prefix + '_cache_name')
    notify_settings = (cache.get(cache_name) or
                       user.get_notification_settings(prefix))
    field = None
    for key, val in NOTIFICATION_MAP_FIELDS.iteritems():
        if val == verb:
            field = key
            break
    return field and getattr(notify_settings, field, False)


@receiver(notify, dispatch_uid='handle_notify')
def handle_notify(verb, **kwargs):
    from accounts.models import User
    if 'recipients' in kwargs:
        recipients = list(kwargs.pop('recipients'))
    else:
        recipients = []

    email_list = kwargs.get('email_list', [])
    if email_list == None:
        recipients_mail = []
    else:
        recipients_mail = recipients[:]
    recipients_obj = User.objects.filter(pk__in=recipients)
    for recipient in recipients_obj:
        if not check_recipient_settings(recipient, verb):
            recipients.remove(recipient.pk)
        if not check_recipient_settings(recipient, verb, 'mail'):
            recipients_mail.remove(recipient.pk)

    if recipients or recipients_mail or email_list:
        actor = kwargs.pop('sender')
        notify_kwargs = {
            'actor': actor,
            'actor_content_type': ContentType.objects.get_for_model(actor),
            'verb': verb,
            'public': bool(kwargs.pop('public', True)),
            'description': kwargs.pop('description', '')
        }

        for opt in ('target', 'action_object'):
            obj = kwargs.pop(opt, None)
            if obj:
                notify_kwargs.update({
                    '{0}_object_id'.format(opt): obj.pk,
                    '{0}_content_type'.format(opt):
                        ContentType.objects.get_for_model(obj),
                })
    if recipients:
        Notification.objects.bulk_create([
            Notification(recipient_id=recipient, **notify_kwargs)
            for recipient in set(recipients)
        ])
    if recipients_mail:
        MailNotification.objects.bulk_create([
            MailNotification(recipient_id=recipient, **notify_kwargs)
            for recipient in set(recipients_mail)
        ])
    if email_list:
        # MailNotification.objects.bulk_create([
        #     MailNotification(email=email, **notify_kwargs)
        #     for email in set(email_list)
        # ])
        Notification.objects.bulk_create([
            Notification(email=email, **notify_kwargs)
            for email in set(email_list)
        ])
