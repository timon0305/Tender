# encoding: utf-8
from __future__ import unicode_literals

from multiupload.fields import MultiFileField
from django.forms import ModelForm
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode

from accounts.models import User

MAX_NUM_FILES = 5
MAX_FILE_SIZE = 1024 * 1024 * 5


class AttachmentFormMixin(ModelForm):
    attachments = MultiFileField(max_num=MAX_NUM_FILES,
                                 max_file_size=MAX_FILE_SIZE,
                                 required=False)

    def save(self, commit=True):
        super(AttachmentFormMixin, self).save(commit=commit)

        attach_model = getattr(self.Meta, 'attachment_model')

        for each in self.cleaned_data['attachments']:
            attach_model.objects.create(
                tender=self.instance, user=self.instance.user, file=each
            )
        return self.instance


class CompanyNameFormMixin(object):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(CompanyNameFormMixin, self).__init__(*args, **kwargs)

    def clean(self):
        super(CompanyNameFormMixin, self).clean()
        if 'company_name' in self.cleaned_data:
            company_name = self.cleaned_data['company_name']
            self.username = slugify(unidecode(unicode(company_name)))[:29]
            if ((User.objects.filter(company_name=company_name).exists() and
                    company_name != self.user.company_name)
                or
                (User.objects.filter(
                    username=self.username).exists()
                 and self.username != self.user.username)):
                self.add_error(
                    'company_name',
                    _('Unique field')
                )
