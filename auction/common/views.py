# encoding: utf-8
from __future__ import unicode_literals

from django.views.generic import View
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy

from accounts.models import USER_ROLE_MAP


UserModel = get_user_model()


class HomeView(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user_role = request.user.role
            url = USER_ROLE_MAP.get(user_role).get('base_url')
        else:
            url = 'auth_login'
        return HttpResponseRedirect(reverse_lazy(url))


class ChangeProfileMixinView(object):
    template_name = 'accounts/change_profile.html'

    def get_success_url(self):
        return reverse_lazy('provider_profile',
                            kwargs={'pk': self.request.user.pk})

    def get_form_kwargs(self):
        kwargs = super(ChangeProfileMixinView, self).get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({'company_name': self.object.user.company_name})
        return initial

    def form_valid(self, form):
        self.object.user.company_name = form.cleaned_data['company_name']
        self.object.user.username = form.username
        self.object.user.save()
        return super(ChangeProfileMixinView, self).form_valid(form)
