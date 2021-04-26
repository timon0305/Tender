# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy


class AuthenticatedPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('home'))
        return super(AuthenticatedPermission, self).dispatch(request, *args,
                                                             **kwargs)


class ProviderIndividualPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 1:
            raise Http404
        return super(ProviderIndividualPermission, self).dispatch(request,
                                                                  *args,
                                                                  **kwargs)


class ProviderCompanyPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role == 2:
            raise Http404
        return super(ProviderCompanyPermission, self).dispatch(request, *args,
                                                               **kwargs)


class ProviderPermission(object):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.role == 1 or request.user.role == 2):
            raise Http404
        return super(ProviderPermission, self).dispatch(request, *args,
                                                        **kwargs)