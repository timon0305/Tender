# encoding: utf-8
from __future__ import unicode_literals

from decimal import Decimal
from django.db import models


class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, verbose_name=None, name=None, **kwargs):
        decimal_places = kwargs.pop('decimal_places', 2)
        max_digits = kwargs.pop('max_digits', 15)

        super(CurrencyField, self).__init__(
            verbose_name=verbose_name, name=name, max_digits=max_digits,
            decimal_places=decimal_places, **kwargs)

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(
                Decimal('0.01'))
        except AttributeError:
            return None