# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from common.mixin import AccountMixinAdmin

from .forms import SwapUserChangeForm, SwapUserCreationForm
from .models import (User, Experience, BusinessType, NumberOfEmloyees, Turnover,
                     Expertise, ProviderCompany, ProviderIndividual, Employer)


class ExtUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Extra'), {'fields': ('role','company_name')}),
    )
    form = SwapUserChangeForm
    add_form = SwapUserCreationForm


admin.site.register(User, ExtUserAdmin)
admin.site.register(Employer)
admin.site.register(ProviderIndividual)
admin.site.register(ProviderCompany)
admin.site.register(BusinessType, AccountMixinAdmin)
admin.site.register(Expertise, AccountMixinAdmin)
admin.site.register(Turnover, AccountMixinAdmin)
admin.site.register(NumberOfEmloyees, AccountMixinAdmin)
admin.site.register(Experience, AccountMixinAdmin)