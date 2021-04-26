# -*- coding: utf-8 -*-
import datetime

from django import template

register = template.Library()


@register.simple_tag()
def search_form(data_finish):
    try:
        d = data_finish.replace(tzinfo=None) - datetime.datetime.now()
        return d.days if d.days >= 0 else 0
    except:
        return 0


@register.simple_tag()
def days_delay(data_finish):
    try:
        d = datetime.datetime.now() - data_finish.replace(tzinfo=None)
        return d.days if d.days >= 0 else 0
    except:
        return 0