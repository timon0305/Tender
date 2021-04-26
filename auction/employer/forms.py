# encoding: utf-8
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User, Experience, Expertise, Employer
from common.forms import CompanyNameFormMixin


class SearchEmployerForm(forms.Form):
    type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=User.Roles.CHOICES[1:],
        required=False)
    expertise = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Expertise.objects.filter(is_active=True),
        required=False
    )
    experience = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Experience.objects.filter(is_active=True),
        required=False
    )


class EmployerFormEdit(CompanyNameFormMixin, forms.ModelForm):
    company_name = forms.CharField(label=_('Company name'), required=True)

    class Meta:
        model = Employer
        fields = ['company_name', 'logo', 'description', 'facebook', 'twitter',
                  'google', 'linkedin', 'business_type', 'turnover',
                  'number_of_emloyees', ]