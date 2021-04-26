# encoding: utf-8
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, UpdateView, View
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy

from common.view_mixin import AuthenticatedEmployerMixinView, ActiveTabMixin,\
    AuthenticatedMixinView
from accounts.models import Employer
from employer.forms import SearchEmployerForm, EmployerFormEdit
from common.views import ChangeProfileMixinView


UserModel = get_user_model()


class EmployerProfileView(ActiveTabMixin, AuthenticatedMixinView,
                          DetailView):
    model = UserModel
    template_name = 'employer/employer_profile.html'
    active_tab = 'my_profile'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])


class EmployerEditProfileView(ChangeProfileMixinView,
                              AuthenticatedEmployerMixinView,
                              UpdateView):
    model = Employer
    form_class = EmployerFormEdit
    template_name = 'accounts/change_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('employer_profile',
                            kwargs={'pk': self.request.user.pk})


class EmployerSearchProvider(ActiveTabMixin, TemplateResponseMixin, View):
    template_name = 'employer/employer_search.html'
    form_class = SearchEmployerForm
    active_tab = 'search_for_service_provider'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        lookup = {}
        ctx = {'form': form}
        if form.is_valid():
            roles = form.cleaned_data.get('type')
            default_roles = UserModel.Roles

            lookup['role__in'] = roles if roles else [
                default_roles.PROVIDER_INDIVIDUAL,
                default_roles.PROVIDER_COMPANY,
            ]

            qs = UserModel.objects.filter(**lookup)

            experience = form.cleaned_data.get('experience')
            if experience:
                qs = qs.filter(
                    Q(user_provider__year__in=experience) |
                    Q(user_provider_company__year__in=experience)
                )

            expertise = form.cleaned_data.get('expertise')
            if expertise:
                qs = qs.filter(
                    Q(user_provider__expertise__in=expertise) |
                    Q(user_provider_company__expertise__in=expertise)
                )

            ctx['object_list'] = qs.select_related().distinct()
            ctx['active_tab'] = self.get_active_tab()
        return self.render_to_response(ctx)
