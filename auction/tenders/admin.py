# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.mixin import AccountMixinAdmin
from .models import Tenders, Industry, Bids, InvitedProvider


class TendersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'created', 'deadline', 'type',
        'industry', 'is_active'
    )
    list_filter = ('is_active',)
    search_fields = ('=id', 'title')


class BidsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'tender', 'price'
    )


admin.site.register(Bids, BidsAdmin)
admin.site.register(InvitedProvider)
admin.site.register(Tenders, TendersAdmin)
admin.site.register(Industry, AccountMixinAdmin)
