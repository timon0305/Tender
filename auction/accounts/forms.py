# encoding: utf-8
from __future__ import unicode_literals


from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth import get_user_model, authenticate
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from unidecode import unidecode

UserModel = get_user_model()


class SwapUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data['username']
        try:
            UserModel._default_manager.get(username=username)
        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class SwapUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class CustomerForm(object):
    def __init__(self, request=None, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = {
                'class': 'input-xlarge',
                'placeholder': self.fields[field_name].label
            }


class AuthenticationForm(CustomerForm, forms.ModelForm):
    email = forms.EmailField(label=_("Email"), required=True)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive.")
    }

    class Meta:
        model = UserModel
        fields = ('email',)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = UserModel._default_manager.get(
                    email=self.cleaned_data['email'])
            except UserModel.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.user_cache = authenticate(username=user.username,
                                               password=password)
                if self.user_cache is None:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                    )
                elif not self.user_cache.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class PasswordResetCustomerForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetCustomerForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = {
                'class': 'span12',
            }

    def clean(self):
        super(PasswordResetCustomerForm, self).clean()
        if 'email' in self.cleaned_data:
            if not UserModel.objects.filter(
                    email=self.cleaned_data['email']).extra():
                raise forms.ValidationError(
                    _('This email address is absent in database'))
        return self.cleaned_data


class SetPasswordCustomerForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordCustomerForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = {
                'class': 'span12',
            }


class RegistrationUserForm(CustomerForm, forms.ModelForm):
    error_messages = {
        'duplicate_email': _('A user with that email already exists.'),
        'password_mismatch': _("The two password fields didn't match."),
    }

    company_name = forms.CharField(label=_('Name'), max_length=70,
                                 required=True)
    email = forms.EmailField(label=_('E-mail'), required=True, max_length=75)
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            UserModel._default_manager.get(email=email)
        except UserModel.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        self.username = self.make_username(
            slugify(unidecode(unicode(company_name)))[:29])
        return company_name

    def make_username(self, username):
        if username:
            try:
                UserModel._default_manager.get(username=username)
            except UserModel.DoesNotExist:
                return username
        return self.make_username(
            '{}{}'.format(username[:25], get_random_string(length=4))
        )

    def get_username(self):
        return self.username

    class Meta:
        model = UserModel
        fields = ('company_name', 'email')
