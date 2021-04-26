# encoding: utf-8
from __future__ import unicode_literals

from django.forms import ModelForm

from django import forms
from .models import Tenders, TendersAttachments, InvitedProvider
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from django.conf import settings


class TendersModelForm(ModelForm):
    deadline = forms.SplitDateTimeField()
    edit_tender_id = forms.CharField(required=False,
                                     widget=forms.HiddenInput())
    tender_ident = forms.CharField(required=False,
                                     widget=forms.HiddenInput())

    class Meta:
        attachment_model = TendersAttachments
        model = Tenders
        fields = ('title', 'type_public', 'deadline', 'type', 'industry', 'description')

    def clean(self):
        super(TendersModelForm, self).clean()
        if 'deadline' in self.cleaned_data:
            if self.cleaned_data['deadline'] < timezone.now():
                self._errors["deadline"] = self.error_class(
                    ['Deadline should not be in the past'])
                del self.cleaned_data["deadline"]
        return self.cleaned_data


class TendersAttachmentForm(ModelForm):
    class Meta:
        model = TendersAttachments
        fields = ('file', 'tender_ident', 'tender')


class InviteProviderForm(forms.ModelForm):

    class Meta:
        model = InvitedProvider
        fields = ('provider_email',)

    def __init__(self, tender=None, *args, **kwargs):
        self.tender = tender
        super(InviteProviderForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(InviteProviderForm, self).clean()
        if 'provider_email' in self.cleaned_data:
            if InvitedProvider.objects.filter(
                    provider_email=self.cleaned_data['provider_email'],
                    tender=self.tender):
                self.add_error('provider_email', _('Provider already invited'))
            else:
                try:
                    user = User.objects.get(email=self.cleaned_data['provider_email'])
                except User.DoesNotExist:
                    pass
                else:
                    if not user.role:
                        self.add_error('provider_email', _(
                            'He isn\'t provider'))
                    else:
                        self.instance.provider = user


