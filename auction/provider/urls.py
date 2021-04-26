# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, patterns

from .views import (
    MyBidsTendersView, MyProfileView, SearchTendersView, ChangeProviderView,
    ChangeProviderCompanyView, BidsCreateView, BidsEditView, BidDeleteView,
    AttachmentDeleteView, BidAttachmentsAddView
)


urlpatterns = patterns('',
                       url(r'^bids/$', MyBidsTendersView.as_view(),
                           name='provider_bids'),
                       url(r'^make_bid/$', BidsCreateView.as_view(),
                           name='make-bid'),
                       url(r'^bid/(?P<pk>\d+)/edit/$',
                           BidsEditView.as_view(), name='bid-edit'),
                       url(r'^bid/attachment_add/$',
                           BidAttachmentsAddView.as_view(), name='bid_attachment_add'),
                       url(r'^bid/(?P<pk>\d+)/attachment_delete/$',
                           AttachmentDeleteView.as_view(), name='attachment-delete'),
                       url(r'^bid/(?P<pk>\d+)/withdraw/$',
                           BidDeleteView.as_view(), name='bid-withdraw'),
                       url(r'^profile/(?P<pk>\d+)/$', MyProfileView.as_view(),
                           name='provider_profile'),
                       url(r'^search-tenders/$', SearchTendersView.as_view(),
                           name='search_tender'),
                       url(r'^change-profile/(?P<pk>\d+)/$',
                           ChangeProviderView.as_view(), name='change_profile'),
                       url(r'^change-profile/(?P<pk>\d+)/company/$',
                           ChangeProviderCompanyView.as_view(),
                           name='change_company_profile'),
)