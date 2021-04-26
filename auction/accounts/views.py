# encoding: utf-8
from __future__ import unicode_literals
import json

from django.core.context_processors import csrf
from django.db.transaction import atomic
from django.template.loader import render_to_string
from django.views.generic.base import View, TemplateResponseMixin
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import get_user_model, login, authenticate
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormMixin

from accounts.models import USER_ROLE_MAP, User
from accounts.forms import CustomerForm, RegistrationUserForm
from provider.forms import ProviderIndividualForm, ProviderCompanyForm
from notifications.models import Notification
from tenders.models import InvitedProvider


UserModel = get_user_model()


USER_MAP_FORMS = {
    User.Roles.PROVIDER_COMPANY: ProviderCompanyForm,
    User.Roles.PROVIDER_INDIVIDUAL: ProviderIndividualForm
}

class RegistrationFormMixin(FormMixin):
    def get_user_form_class(self):
        """
        Returns User form class for registration and validating
        """
        return self.user_form_class

    def get_secondary_form_class(self):
        """
        Returns secondary form class for additional data while registration
        """
        if self.reg_type_id:
            return USER_MAP_FORMS[self.reg_type_id]
        else:
            meta_attr = {'model': self.REG_TYPE['model'], 'exclude': ('user', )}
            form_attr = {
                'Meta': type(str('Meta'), (), meta_attr),
            }
            return type(str('Form'), (CustomerForm, forms.ModelForm), form_attr)

    def form_invalid(self, user_form, secondary_form):
        ctx_dict = {
            'user_form': user_form,
            'secondary_form': secondary_form
        }
        return self.render_to_response(self.get_context_data(**ctx_dict))

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {}

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs


class RegistrationView(RegistrationFormMixin, TemplateResponseMixin, View):
    user_form_class = RegistrationUserForm
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        try:
            self.reg_type_id = int(request.GET.get('type', 0))
            self.REG_TYPE = USER_ROLE_MAP[self.reg_type_id]
        except (ValueError, KeyError):
            raise Http404

        self.template_name = self.REG_TYPE['reg_tpl']
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    @property
    def get_success_url(self):
        return reverse_lazy(self.REG_TYPE['base_url'])

    def get(self, request, *args, **kwargs):
        ctx_dict = {
            'user_form': self.get_user_form_class(),
            'secondary_form': self.get_secondary_form_class()
        }
        return self.render_to_response(self.get_context_data(**ctx_dict))

    def post(self, request, *args, **kwargs):
        self.initial = self.request.POST

        user_form = self.get_form(self.get_user_form_class())
        secondary_form = self.get_form(self.get_secondary_form_class())

        if user_form.is_valid() and secondary_form.is_valid():
            return self.form_valid(request, user_form, secondary_form)
        else:
            return self.form_invalid(user_form, secondary_form)

    def form_valid(self, request, user_form, secondary_form):
        username = user_form.get_username()
        email = user_form.cleaned_data['email']
        password = user_form.cleaned_data['password1']
        company_name = user_form.cleaned_data['company_name']

        self.register(username, email, password, company_name, secondary_form)
        user = self.login(request, username, password)
        if user.role:
            Notification.objects.filter(email=user.email).update(
                recipient=user.pk)
            InvitedProvider.objects.filter(provider_email=user.email).update(
                provider=user
            )

        return HttpResponseRedirect(self.get_success_url)

    @method_decorator(atomic)
    def register(self, username, email, password, company_name, secondary):
        new_user = UserModel.objects.create_user(username, email, password,
                                                 role=self.reg_type_id,
                                                 company_name=company_name)
        new_secondary = secondary.save(commit=False)
        new_secondary.user = new_user
        new_secondary.save()
        secondary.save_m2m()

    def login(self, request, username, password):
        user = authenticate(username=username, password=password)
        login(request, user)
        return user

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            tpl = self.REG_TYPE['reg_tpl'].split('/')
            tpl[-1] = 'form_{}'.format(tpl[-1])
            context['request'] = self.request
            context.update(csrf(self.request))
            html = render_to_string('/'.join(tpl), context)
            json_dump = json.dumps({'html': html})
            return HttpResponse(json_dump, content_type='application/json')

        return super(RegistrationView, self).render_to_response(context,
                                                                **response_kwargs)
