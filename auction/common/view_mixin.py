# encoding: utf-8
from __future__ import unicode_literals

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.http.response import HttpResponse


class AuthenticatedMixinView(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        role_method = getattr(self, 'role_method', None)
        if role_method:
            if not getattr(self.request.user, role_method)():
                raise Http404
        return super(AuthenticatedMixinView, self).dispatch(request, *args,
                                                            **kwargs)


class AuthenticatedEmployerMixinView(AuthenticatedMixinView):
    role_method = 'is_employer'


class AuthenticatedProviderMixinView(AuthenticatedMixinView):
    role_method = 'is_provider'


class ObjectOwnerPermMixin(object):
    def get_object(self, queryset=None):
        obj = super(ObjectOwnerPermMixin, self).get_object(queryset)
        if self.request.user != obj.user:
            raise PermissionDenied
        return obj


class ActiveTabMixin(object):
    """
    Mixin to set active tab menu
    """
    active_tab = None

    def get_active_tab(self):
        if self.active_tab is None:
            raise ImproperlyConfigured(
                "ActiveTabMixin requires either a definition of "
                "'active_tab' or an implementation of 'get_active_tab()'")
        return self.active_tab

    def get_context_data(self, **kwargs):
        context = super(ActiveTabMixin, self).get_context_data(**kwargs)
        context['active_tab'] = self.get_active_tab()
        return context


class AttachmentDeleteMixin(ObjectOwnerPermMixin, SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwset={'user': self.request.user}
        if self.object.tender:
            kwset['tender'] = self.object.tender
        else:
            kwset['tender_ident'] = self.object.tender_ident
        self.object.delete()
        return HttpResponse(len(self.model.objects.filter(**kwset)))