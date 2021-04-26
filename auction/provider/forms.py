# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import ProviderIndividual, Expertise, ProviderCompany
from common.forms import CompanyNameFormMixin
from tenders.models import Industry, Bids, BidsAttachments


class SearchProviderForm(forms.Form):
    industry = forms.ModelChoiceField(
        queryset=Industry.objects.filter(is_active=True), required=False)
    #deadline = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M'], required=False)
    deadline = forms.DateField(required=False)
    is_open = forms.BooleanField(required=False)
    is_employer = forms.BooleanField(required=False)
    is_close = forms.BooleanField(required=False)


class ProviderAbstractForm(forms.ModelForm):
    expertise = forms.ModelMultipleChoiceField(
        queryset=Expertise.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        exclude = ('user', )


class ProviderIndividualForm(ProviderAbstractForm):
    class Meta(ProviderAbstractForm.Meta):
        model = ProviderIndividual


class ProviderIndividualFormEdit(CompanyNameFormMixin, ProviderAbstractForm):
    company_name = forms.CharField(label=_('Name'), required=True)

    class Meta(ProviderAbstractForm.Meta):
        model = ProviderIndividual
        fields = ['company_name', 'logo', 'description', 'facebook', 'twitter',
                  'google', 'linkedin', 'year', 'expertise', ]
        

class ProviderCompanyForm(ProviderAbstractForm):
    class Meta(ProviderAbstractForm.Meta):
        model = ProviderCompany


class ProviderCompanyFormEdit(CompanyNameFormMixin, ProviderAbstractForm):
    company_name = forms.CharField(label=_('Company name'), required=True)

    class Meta(ProviderAbstractForm.Meta):
        model = ProviderCompany
        fields = ['company_name', 'logo', 'description', 'facebook', 'twitter',
                  'google', 'linkedin', 'business_type', 'turnover',
                  'number_of_emloyees', 'year', 'expertise', ]


class BidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ('price',)


class BidsAttachmentForm(forms.ModelForm):
    class Meta:
        model = BidsAttachments
        fields = ('file', 'tender_ident', 'tender')
