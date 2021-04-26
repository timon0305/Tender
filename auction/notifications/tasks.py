# encoding: utf-8
from __future__ import unicode_literals, absolute_import

import traceback

from celery.task.base import task
from django.contrib.sites.models import Site
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from notifications.models import (MailNotification)
from notifications.signals import notify
from tenders.models import Tenders


def send_mail_to_developers(subject, message):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              settings.DEVELOPERS_EMAIL)


@task
def send_emails(messages):
    connection = get_connection()
    connection.open()
    try:
        for message in messages:
            msg = EmailMultiAlternatives(*message[0:4], connection=connection)
            if len(message) >= 5:
                msg.attach_alternative(message[4], "text/html")
            msg.send()
    except:
        send_mail_to_developers('Send mass mail', traceback.format_exc())       
    connection.close()


def get_rendered_notification(instance, template_name='notifications/email'):
    ctx = {'notice': instance, }
    if Site._meta.installed:
        ctx['domain'] = 'http://{}'.format(Site.objects.get_current().domain)
    return render_to_string(template_name, ctx)


@task
def send_notifications():
    try:
        qs = MailNotification.objects.all().select_related()
        ids = set(qs.values_list('id', flat=True))
        qs = MailNotification.objects.filter(id__in=ids).order_by('created')
        if ids:
            messages = [
                ['Notification', get_rendered_notification(notification),
                 settings.DEFAULT_FROM_EMAIL,
                 [notification.recipient.email, ]
                 if notification.recipient else [notification.email, ],
                 get_rendered_notification(notification,
                                           'notifications/email.html'),
                 ]
                for notification in qs
            ]
            if messages:
                send_emails.delay(messages)
            qs.delete()
    except:
        send_mail_to_developers('Send notifications', traceback.format_exc())


@task
def close_tenders():
    try:
        qs = Tenders.objects.filter(deadline__lt=timezone.now(),
                                    is_withdraw=False)

        tender_ids = set(qs.values_list('id', flat=True))

        if tender_ids and qs.update(is_withdraw=True):
            tenders = Tenders.objects.filter(id__in=tender_ids).select_related()

            for tender in tenders:
                user_ids = list(tender.tender_bids.values_list('user', flat=True))
                user_ids.append(tender.user_id)
                notify.send(tender.user, recipients=user_ids,
                            verb='closed tender', target=tender)
    except:
        send_mail_to_developers('Close tenders', traceback.format_exc())
