# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import Http404, HttpResponse
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import (ListView, DetailView, FormView, UpdateView,
                                  CreateView, DeleteView)
from dateutil import parser
from django.template.loader import render_to_string

from notifications.signals import notify
from accounts.models import User, ProviderIndividual, ProviderCompany
from common.view_mixin import (
    AuthenticatedProviderMixinView,
    ObjectOwnerPermMixin, ActiveTabMixin, AttachmentDeleteMixin)
from tenders.models import Tenders, Bids, BidsAttachments, InvitedProvider
from .forms import (
    SearchProviderForm, ProviderIndividualFormEdit, ProviderCompanyFormEdit,
    BidsForm, BidsAttachmentForm)
from .permissions import (
    AuthenticatedPermission, ProviderPermission, ProviderIndividualPermission,
    ProviderCompanyPermission
)
from django.utils import timezone
from django.conf import settings
from common.mixin import datetime_convert
from common.views import ChangeProfileMixinView


class MyBidsTendersView(ActiveTabMixin, AuthenticatedPermission,
                        ProviderPermission, ListView):
    template_name = 'provider/bids.html'
    context_object_name = 'tender_list'
    queryset = Tenders.objects.all()
    active_tab = 'my_bids'

    def get_queryset(self):
        qs = super(MyBidsTendersView, self).get_queryset()
        lookup = {'tender_bids__user': self.request.user,
                  'is_withdraw': False,
                  'deadline__gt': now()}
        return qs.filter(**lookup).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(MyBidsTendersView, self).get_context_data(**kwargs)
        context['experied'] = Tenders.objects.filter(
            is_active=True, tender_bids__user=self.request.user).filter(
            Q(is_withdraw=True) | Q(deadline__lt=now())
        ).order_by('-created')
        context['active_tenders_tab'] = 'experied' \
            if self.request.COOKIES.get('page_click') == 'exp' else 'active'
        return context


class MyProfileView(ActiveTabMixin, AuthenticatedPermission, DetailView):
    template_name = 'provider/provider_profile.html'
    queryset = User.objects.all()
    active_tab = 'my_profile'


class SearchTendersView(ActiveTabMixin, AuthenticatedPermission,
                        ProviderPermission, FormView):
    http_method_names = ('get', )
    template_name = 'provider/search_tender.html'
    form_class = SearchProviderForm
    success_url = '/'
    active_tab = 'search_for_tenders'

    def get_context_data(self, **kwargs):
        context = super(SearchTendersView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        invited_tenders = InvitedProvider.objects.filter(
            provider=self.request.user).values_list('tender', flat=True)
        qs = Tenders.objects.filter(is_active=True, is_withdraw=False,
                                    deadline__gt=now()).filter(
            Q(type_public=1) | Q(type_public=2, pk__in=invited_tenders)
        )
        kwargs = {}
        get_request = self.request.GET
        industry = get_request.get('industry', None)
        if industry:
            kwargs['industry'] = industry
        deadline = get_request.get('deadline', None)
        if deadline:
            deadline_left = datetime_convert(
                parser.parse(deadline + ' 00:00'),
                'UTC',
                settings.TIME_ZONE
            )
            deadline_right = datetime_convert(
                parser.parse(deadline + ' 23:59'),
                'UTC',
                settings.TIME_ZONE
            )
            qs = qs.filter(deadline__lte=deadline_right,
                           deadline__gte=deadline_left)
        else:
            qs = qs.filter(deadline__gte=timezone.now())
        list_status = []
        is_open = get_request.get('is_open', None)
        if is_open == 'on':
            list_status.append(0)
        is_employer = get_request.get('is_employer', None)
        if is_employer == 'on':
            list_status.append(1)
        is_close = get_request.get('is_close', None)
        if is_close == 'on':
            list_status.append(2)
        if list_status:
            kwargs['type__in'] = list_status
        context['tender_list'] = qs.filter(**kwargs).select_related().order_by(
            '-created')
        return context


class ChangeProviderView(ChangeProfileMixinView,
                         AuthenticatedPermission,
                         ProviderIndividualPermission,
                         UpdateView):
    form_class = ProviderIndividualFormEdit
    model = ProviderIndividual


class ChangeProviderCompanyView(ChangeProfileMixinView,
                                AuthenticatedPermission,
                                ProviderCompanyPermission,
                                UpdateView):
    form_class = ProviderCompanyFormEdit
    model = ProviderCompany


class PermissionPrivateTender(object):

    def check_permission_to_private(self, tender=None):
        if tender:
            if tender.type_public == 2 and self.request.user.role:
                ids_provider = InvitedProvider.objects.filter(
                    tender=tender).values_list('provider', flat=True)
                if self.request.user.pk not in ids_provider:
                    raise PermissionDenied


class BidsCreateView(AuthenticatedProviderMixinView, PermissionPrivateTender,
                     CreateView):
    http_method_names = ('get', 'post', )
    model = Bids
    form_class = BidsForm
    tender = None

    def check_request(self):
        if not self.request.is_ajax():
            raise PermissionDenied

        user = self.request.user
        roles = [user.Roles.PROVIDER_COMPANY, user.Roles.PROVIDER_INDIVIDUAL]
        if user.role not in roles:
            raise PermissionDenied

        try:
            self.tender_id = int(self.request.GET.get('tender_id', 0))
        except ValueError:
            raise Http404

        self.tender = get_object_or_404(Tenders, **{'id': self.tender_id})

        self.check_permission_to_private(self.tender)

    def dispatch(self, request, *args, **kwargs):
        self.check_request()
        if Bids.objects.is_able_bid(user=request.user, tender_id=self.tender_id):
            html = render_to_string('provider/bid_done.html')
            return HttpResponse(html, status=200)
        elif self.tender.is_withdraw or self.tender.is_expired:
            raise PermissionDenied
        else:
            return super(BidsCreateView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        tender_ident = self.request.POST.get('tender_ident', None)
        attach_list = None

        if tender_ident:
            lookup = {
                'tender_ident': self.request.user.username + tender_ident,
                'user': self.request.user
            }
            attach_list = BidsAttachments.objects.filter(**lookup)

        context.update({'tender_ident': tender_ident,
                        'attach_list': attach_list})
        html = render_to_string('tenders/bids_form.html', context)
        return HttpResponse(json.dumps({'html': html, 'formshow': 'yes'}),
                            status=200)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tender_id = self.tender_id
        self.object = form.save()
        tender_ident = self.request.POST.get('tender_ident', None)

        if tender_ident:
            lookup = {
                'tender_ident': self.request.user.username + tender_ident,
                'user': self.request.user
            }
            BidsAttachments.objects.filter(**lookup).update(tender=self.object)

        notify.send(self.request.user, recipients=[self.object.tender.user.id],
                    verb='created a new bid', target=self.object.tender)

        html = render_to_string(
            'tenders/bids_list.html',
            {'bids': [self.object, ], 'user': self.request.user,
             'tender': self.tender}
        )
        return HttpResponse(json.dumps({'html': html, 'formshow': 'no'}),
                            status=200)


class BidsMixin(object):
    def get_success_url(self):
        return reverse_lazy('employer-tender-detail',
                            kwargs={'pk': self.object.tender.id})

    def send_notification(self):
        notify.send(self.request.user, recipients=[self.object.tender.user.id],
                    verb=self.verb_msg, target=self.object.tender)


class BidsEditView(AuthenticatedProviderMixinView,
                   ObjectOwnerPermMixin,
                   PermissionPrivateTender,
                   BidsMixin,
                   UpdateView):
    http_method_names = ('get', 'post', )
    model = Bids
    form_class = BidsForm
    template_name_suffix = '_edit'
    verb_msg = 'changed bid'

    def get_object(self, queryset=None):
        obj = super(BidsEditView, self).get_object(queryset)
        self.check_permission_to_private(obj.tender)
        # check for withdrawal
        if obj.tender.is_withdraw:
            raise PermissionDenied
        return obj

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        html = render_to_string('tenders/modal_edit_bid.html',
                                {'form': context['form'],
                                 'attach_list': BidsAttachments.objects.filter(
                                     tender=self.object,
                                     user=self.request.user),
                                 'bid_id': self.kwargs['pk']})

        json_dump = json.dumps({'html': html, 'formshow': 'yes'})
        return HttpResponse(json_dump)

    def form_valid(self, form):
        self.object = form.save()
        self.send_notification()

        html = render_to_string(
            'tenders/bids_list.html',
            {'bids': [self.object, ], 'user': self.request.user,
             'tender': {'is_withdraw': False}}
        )

        json_dump = json.dumps({'html': html, 'formshow': 'no'})
        return HttpResponse(json_dump)


class BidDeleteView(AuthenticatedProviderMixinView,
                    ObjectOwnerPermMixin,
                    PermissionPrivateTender,
                    BidsMixin,
                    DeleteView):
    model = Bids
    verb_msg = 'withdrew bid'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.check_permission_to_private(self.object.tender)
        self.object.delete()
        self.send_notification()
        return HttpResponse(_('Ok'))


class AttachmentDeleteView(AuthenticatedProviderMixinView,
                           AttachmentDeleteMixin):
    model = BidsAttachments


class BidAttachmentsAddView(AuthenticatedProviderMixinView,
                            CreateView):
    form_class = BidsAttachmentForm
    template_name = 'provider/attach_form.html'
    bid = None

    def dispatch(self, request, *args, **kwargs):
        tender_id = request.POST.get('tender_id', None)
        if tender_id:
            try:
                self.bid = Bids.objects.get(user=request.user, tender=tender_id)
            except ObjectDoesNotExist:
                pass
        return super(BidAttachmentsAddView, self).dispatch(request,
                                                           *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        kwargs = {'user': self.object.user}
        if self.bid:
            self.object.tender = self.bid
            kwargs['tender'] = self.bid.pk
        else:
            session_id = (self.request.user.username +
                          form.cleaned_data['tender_ident'])
            self.object.tender_ident = session_id
            kwargs['tender_ident'] = self.object.tender_ident
        self.object.save()
        qs = len(BidsAttachments.objects.filter(**kwargs))
        return HttpResponse(json.dumps({'pk': self.object.pk,
                                        'file': self.object.file.name.
                                            encode('utf-8').split('/')[-1],
                                        'quan': qs}), status=200)