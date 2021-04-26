# encoding: utf-8
from __future__ import unicode_literals

import time

from django.template import Library

from tenders.models import Bids


register = Library()


@register.inclusion_tag('tenders/bids_list.html', takes_context=True)
def bids_list(context, tender):
    user = context['user']
    t_type = tender.type
    types = tender.Types

    if (t_type == types.CLOSED) or (t_type == types.EMPLOYER and user != tender.user):
        qs = Bids.objects.filter(tender=tender, user=user)
    else:
        qs = Bids.objects.prefetch_related('bidsattachments').filter(tender=tender)
    return {'bids': qs, 'user': user, 'tender': tender}


@register.simple_tag()
def get_tender_ident():
    return int(time.time() * 100)