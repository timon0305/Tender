# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from employer.views import (
    EmployerProfileView, EmployerEditProfileView, EmployerSearchProvider
)
from tenders.views import (
    EmployerTendersListView, EmployerTenderDetailView, WithdrawView,
    EmployerTendersCreateView, EmployerTendersEditView,
    TendersAttachmentsDeleteView, TendersAttachmentsAddView, InviteProviderView,
    InviteAddView, InviteDeleteView, InviteSearchView)


urlpatterns = patterns('',
                       url(r'^tenders/$',
                           EmployerTendersListView.as_view(),
                           name='employer_tenders'),
                       url(r'^tender/(?P<pk>\d+)/$',
                           EmployerTenderDetailView.as_view(),
                           name='employer-tender-detail'),
                       url(r'^tender/create/$',
                           EmployerTendersCreateView.as_view(),
                           name='employer-tender-create'),
                       url(r'^tender/(?P<pk>\d+)/invite/$',
                           InviteProviderView.as_view(),
                           name='invite_provider'),
                       url(r'^tender/invite/search/$',
                           InviteSearchView.as_view(),
                           name='invite_search'),
                       url(r'^tender/(?P<pk>\d+)/edit/$',
                           EmployerTendersEditView.as_view(),
                           name='employer-tender-edit'),
                       url(r'^tender/(?P<pk>\d+)/withdraw/$',
                           WithdrawView.as_view(), name='withdraw-tender'),
                       url(r'^tender/attach/delete/(?P<pk>\d+)/$',
                           TendersAttachmentsDeleteView.as_view(),
                           name='tender_attachment'),
                       url(r'^tender/attach/add/$',
                           TendersAttachmentsAddView.as_view(),
                           name='tender_attachment_add'),
                       url(r'^tender/invite/delete/(?P<pk>\d+)/$',
                           InviteDeleteView.as_view(),
                           name='invite_delete'),
                       url(r'^tender/invite/add/$',
                           InviteAddView.as_view(),
                           name='invite_add'),
                       url(r'^profile/(?P<pk>\d+)/$',
                           EmployerProfileView.as_view(),
                           name='employer_profile'),
                       url(r'^change-profile/$',
                           EmployerEditProfileView.as_view(),
                           name='employer_change_profile'),
                       url(r'^search-providers/$',
                           EmployerSearchProvider.as_view(),
                           name='search_providers'),

)