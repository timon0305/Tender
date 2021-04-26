# encoding: utf-8
from __future__ import unicode_literals

from django.db.models import Q
from django.template import Library

from tenders.models import InvitedProvider
from accounts.models import User


register = Library()


@register.inclusion_tag('tenders/invited_providers_tags/email_list.html')
def get_email_list(tender):
    email_list = InvitedProvider.objects.filter(
        tender=tender, provider__isnull=True
    ).order_by('-id').values('provider_email', 'id')
    return {'items': email_list}


@register.inclusion_tag('tenders/invited_providers_tags/provider_list.html')
def get_provider_list(tender):
    providers_list = InvitedProvider.objects.filter(
        tender=tender, provider__isnull=False).order_by('-id')
    return {'items': providers_list}


@register.inclusion_tag('tenders/invited_providers_tags/invited_providers.html')
def get_invited_providers(tender):
    all_email_list = InvitedProvider.objects.filter(
        tender=tender).values_list('provider_email', flat=True)
    ids_providers = InvitedProvider.objects.filter(
        user=tender.user, provider__isnull=False).exclude(
        provider_email__in=all_email_list).distinct().values_list('provider',
                                                                  flat=True)
    invited_providers = User.objects.filter(pk__in=ids_providers)
    return {'items': invited_providers, 'tender': tender.pk}


def get_invited_search(tender, search=None):
    if search:
        ids_providers = InvitedProvider.objects.filter(
            tender=tender, provider__isnull=False).values_list(
            'provider', flat=True)
        invited_providers = User.objects.filter(Q(company_name__icontains=search) | Q(email__icontains=search)).exclude(pk__in=ids_providers).exclude(role=0)
    else:
        invited_providers = []
    return {'items': invited_providers, 'tender': tender}
