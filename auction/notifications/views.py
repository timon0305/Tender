# encoding: utf-8
from __future__ import unicode_literals

from django.utils.functional import cached_property

from django.views.generic import ListView, View, UpdateView
from django.forms import models as model_forms
from django.http import HttpResponse, Http404
from django.contrib.auth import get_user_model

from .models import (Notification, SETTING_MODELS_MAP)
from common.view_mixin import AuthenticatedMixinView
from django.http import HttpResponseRedirect
from django.core.cache import cache


UserModel = get_user_model()


class NotificationListView(AuthenticatedMixinView, ListView):
    model = Notification
    context_object_name = 'notifications'

    def get_queryset(self):
        qs = super(NotificationListView, self).get_queryset()
        return qs.filter(recipient=self.request.user)


class MarkNotificationsView(AuthenticatedMixinView, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.notifications.mark_all_as_read()
        return HttpResponse()


class EditNotificationSettings(AuthenticatedMixinView, UpdateView):
    exclude = ('user', )
    success_url = '/'
    setting_prefix = 'notification'

    @cached_property
    def get_model_class(self):
        user = self.request.user
        if user.is_employer():
            return SETTING_MODELS_MAP[self.setting_prefix]['employer']
        elif user.is_provider():
            return SETTING_MODELS_MAP[self.setting_prefix]['provider']
        else:
            raise Http404

    def get_form_class(self):
        return model_forms.modelform_factory(self.get_model_class,
                                             exclude=self.exclude)

    def get_object(self, queryset=None):
        return self.get_model_class.objects.get(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        cache_name = getattr(self.request.user,
                             'get_' + self.setting_prefix + '_cache_name')
        cache.set(cache_name, self.object)
        return HttpResponseRedirect(self.get_success_url())


class EditMailSettings(EditNotificationSettings):
    setting_prefix = 'mail'
