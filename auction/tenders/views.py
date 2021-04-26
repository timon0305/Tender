# encoding: utf-8
from __future__ import unicode_literals

import json
import time

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.views.generic import (ListView, CreateView, UpdateView, DetailView,
                                  View, TemplateView, DeleteView)
from django.views.generic.detail import SingleObjectMixin

from notifications.signals import notify
from notifications.tasks import (send_emails, get_rendered_notification)
from common.view_mixin import (
    AuthenticatedMixinView, AuthenticatedEmployerMixinView,
    ObjectOwnerPermMixin,
    ActiveTabMixin, AttachmentDeleteMixin
)

from .models import Tenders, TendersAttachments, InvitedProvider
from tenders.forms import (TendersModelForm, TendersAttachmentForm,
                           InviteProviderForm,)
from .templatetags.invited_provider import (
    get_email_list, get_invited_providers, get_provider_list,
    get_invited_search)


class EmployerTendersListView(ActiveTabMixin, AuthenticatedEmployerMixinView,
                              ListView):
    template_name = 'employer/employer_tenders.html'
    model = Tenders
    context_object_name = 'obj'
    active_tab = 'my_tenders'

    def get_queryset(self):
        qs = super(EmployerTendersListView, self).get_queryset()
        return (qs.filter(
            is_active=True, user=self.request.user, is_withdraw=False,
            deadline__gt=now()).order_by('-created'))

    def get_context_data(self, **kwargs):
        context = super(EmployerTendersListView, self).get_context_data(**kwargs)
        context['experied'] = Tenders.objects.filter(
            is_active=True, user=self.request.user).filter(
            Q(is_withdraw=True) | Q(deadline__lt=now())
        ).order_by('-created')
        context['active_tenders_tab'] = 'experied' \
            if self.request.COOKIES.get('page_click') == 'exp' else 'active'
        return context


class EmployerTenderDetailView(AuthenticatedMixinView, DetailView):
    queryset = Tenders.objects.filter(is_active=True)
    context_object_name = 'obj'
    template_name = 'tender/detail_tender.html'

    def render_to_response(self, context, **response_kwargs):
        if self.object.type_public == 2 and self.request.user.role:
            ids_provider = InvitedProvider.objects.filter(
                tender=self.object).values_list('provider', flat=True)
            if self.request.user.pk not in ids_provider:
                return HttpResponseRedirect(reverse_lazy('home'))
        return super(EmployerTenderDetailView, self).render_to_response(
            context, **response_kwargs)


class EmployerTendersCreateView(ActiveTabMixin, AuthenticatedEmployerMixinView,
                                CreateView):
    form_class = TendersModelForm
    model = Tenders
    template_name = 'employer/create_tender.html'
    active_tab = 'create_new_tender'
    initial = {}

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        tender_ident = self.request.POST.get('tender_ident', None)

        if tender_ident:
            lookup = {
                'tender_ident': self.request.user.username + tender_ident,
                'user': self.request.user
            }

            TendersAttachments.objects.filter(**lookup).\
                update(tender=self.object)
        return HttpResponseRedirect(
            reverse_lazy('invite_provider', kwargs={'pk': self.object.pk}))

    def get_context_data(self, **kwargs):
        ctx = super(EmployerTendersCreateView, self).get_context_data(**kwargs)
        tender_ident = (self.request.POST.get('tender_ident') or
                        self.initial.get('tender_ident'))
        attach_list = []

        if tender_ident:
            lookup = {
                'tender_ident': self.request.user.username + str(tender_ident),
                'user': self.request.user
            }
            attach_list = TendersAttachments.objects.filter(**lookup)

        ctx.update({
            'tender_ident': tender_ident,
            'attach_list': attach_list
        })
        return ctx

    def get_initial(self):
        self.initial.update({'tender_ident': int(time.time() * 100)})
        try:
            experied_tender_id = self.request.GET.get('reinvite')
            experied_tender = Tenders.objects.get(
                pk=experied_tender_id)
        except Tenders.DoesNotExist:
            pass
        else:
            self.initial.update({
                'title': experied_tender.title,
                'type': experied_tender.type,
                'type_public': experied_tender.type_public,
                'industry': experied_tender.industry,
                'description': experied_tender.description
            })
            session_id = (self.request.user.username +
                          str(self.initial['tender_ident']))
            TendersAttachments.objects.bulk_create(
                TendersAttachments(
                    file=obj.file, tender_ident=session_id,
                    user_id=self.request.user.pk)
                for obj in TendersAttachments.objects.filter(
                    tender_id=experied_tender_id)
            )
        return self.initial.copy()


class TenderNotificationMixin(object):
    def send_notification(self, verb):
        user_ids = self.object.tender_bids.values_list('user', flat=True)

        if user_ids:
            notify.send(self.object.user, recipients=user_ids,
                        verb=verb, target=self.object)


class EmployerTendersEditView(AuthenticatedEmployerMixinView,
                              TenderNotificationMixin,
                              ObjectOwnerPermMixin,
                              UpdateView):
    form_class = TendersModelForm
    queryset = Tenders.objects.filter(is_active=True)
    template_name = 'employer/edit_tender.html'

    def form_valid(self, form):
        obj = super(EmployerTendersEditView, self).form_valid(form)
        self.send_notification('changed in tender')
        return obj

    def get_context_data(self, **kwargs):
        kwargs = super(EmployerTendersEditView, self).get_context_data(**kwargs)
        kwargs.update({'attach_list': TendersAttachments.objects.filter(
            tender=self.object, user=self.request.user)})
        return kwargs


class AttachmentsMixin(ObjectOwnerPermMixin,
                       SingleObjectMixin,
                       View):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(_('Ok'))


class TendersAttachmentsDeleteView(AuthenticatedEmployerMixinView,
                                   AttachmentDeleteMixin):
    model = TendersAttachments


class TendersAttachmentsAddView(AuthenticatedEmployerMixinView,
                                CreateView):
    form_class = TendersAttachmentForm
    template_name = 'employer/includes/attach_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        kwargs = {'user': self.object.user}

        if not form.cleaned_data['tender']:
            session_id = (self.request.user.username +
                          form.cleaned_data['tender_ident'])
            self.object.tender_ident = session_id
            kwargs['tender_ident'] = self.object.tender_ident
        else:
            kwargs['tender'] = self.object.tender

        self.object.save()

        res = {
            'pk': self.object.pk,
            'file': self.object.file.name.encode('utf-8').split('/')[-1],
            'quan': TendersAttachments.objects.filter(**kwargs).count()
        }
        return HttpResponse(json.dumps(res), status=200)


class WithdrawView(AuthenticatedEmployerMixinView,
                   TenderNotificationMixin,
                   ObjectOwnerPermMixin,
                   UpdateView):
    http_method_names = ('post', )
    fields = []
    model = Tenders
    template_name = 'tender/withdrawview.html'

    def form_valid(self, form):
        if not form.instance.is_withdraw:
            form.instance.is_withdraw = True
            self.send_notification('withdrew tender')
        return super(WithdrawView, self).form_valid(form)


class InviteProviderView(AuthenticatedEmployerMixinView, TemplateView):
    template_name = 'tenders/invite_provider.html'

    def get_context_data(self, **kwargs):
        ctx = super(InviteProviderView, self).get_context_data(**kwargs)
        tender = get_object_or_404(Tenders, pk=self.kwargs['pk'])
        ctx.update({
            'tender': tender,
            'form': InviteProviderForm(),
        })
        return ctx


class InvitedProviderRenderMixin(object):

    def all_renders(self):
        search = self.request.POST.get('search', '')
        html_providers_list = render_to_string(
            'tenders/invited_providers_tags/provider_list.html',
            get_provider_list(self.tender)
        )
        html_email_list = render_to_string(
            'tenders/invited_providers_tags/email_list.html',
            get_email_list(self.tender)
        )
        html_invited_providers = render_to_string(
            'tenders/invited_providers_tags/invited_providers.html',
            get_invited_providers(self.tender)
        )
        html_invited_search = render_to_string(
            'tenders/invited_providers_tags/invited_providers.html',
            get_invited_search(self.tender.pk, search)
        )
        res = {'provider_list': html_providers_list,
               'email_list': html_email_list,
               'invited_providers': html_invited_providers,
               'invited_search': html_invited_search,
               'valid': True}
        return HttpResponse(json.dumps(res), status=200)


class SendInviteNotificationMixin(object):

    def send_message(self, verb):
        kwargs = {
            'verb': verb,
            'target': self.tender
        }
        if self.object.provider:
            kwargs['recipients'] = [self.object.provider.pk, ]
        else:
            kwargs['email_list'] = [self.object.provider_email, ]
        notify.send(self.tender.user, **kwargs)
        if self.object.provider:
            kwargs['recipient'] = self.object.provider
        kwargs['actor'] = self.tender.user
        text = get_rendered_notification(kwargs)
        html_content = get_rendered_notification(
            kwargs, 'notifications/email.html')
        messages = [
            ['Notification', text,
             settings.DEFAULT_FROM_EMAIL,
             [self.object.provider.email, ]
             if self.object.provider else [self.object.provider_email, ],
             html_content,
             ],
        ]
        send_emails.delay(messages)


class InviteAddView(SendInviteNotificationMixin, InvitedProviderRenderMixin,
                    AuthenticatedEmployerMixinView, CreateView):
    http_method_names = ['post']
    form_class = InviteProviderForm
    tender = None

    def get_form_kwargs(self):
        self.tender = get_object_or_404(Tenders, pk=self.request.POST.get('tender'))
        kwargs = super(InviteAddView, self).get_form_kwargs()
        kwargs['tender'] = self.tender
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        html = render_to_string('tenders/invited_providers_tags/invite_form.html', context)
        res = {'html': html, 'valid': False}
        return HttpResponse(json.dumps(res), status=200)

    def form_valid(self, form):
        form.instance.user = self.tender.user
        form.instance.tender = self.tender
        self.object = form.save()
        self.send_message('invited to tender')
        return self.all_renders()


class InviteDeleteView(SendInviteNotificationMixin, InvitedProviderRenderMixin,
                       ObjectOwnerPermMixin, DeleteView):
    model = InvitedProvider

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.tender = self.object.tender
        self.send_message('canceled invite to tender')
        self.object.delete()
        return self.all_renders()


class InviteSearchView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search', '')
        tender_pk = request.POST.get('tender', '')
        html_invited_search = render_to_string(
            'tenders/invited_providers_tags/invited_providers.html',
            get_invited_search(tender_pk, search=search)
        )
        res = {'invited_search': html_invited_search,}
        return HttpResponse(json.dumps(res), status=200)


def modal_content(request):
    data = json.loads(request.POST.get('data', None))
    template = request.POST.get('template', False)

    if template:
        return HttpResponse(render_to_string(template, {'context': data}),
                            status=200)
    else:
        return HttpResponse('Template error', status=404)
