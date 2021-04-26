from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from notifications.views import (
    NotificationListView, MarkNotificationsView, EditNotificationSettings,
    EditMailSettings
)
from tenders.views import modal_content
from common.views import HomeView


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^modal-content/$', modal_content,
                           name='modal_content'),

                       url(r'^notifications/$', NotificationListView.as_view(),
                           name='notifications'),
                       url(r'^mark_notifications/$',
                           MarkNotificationsView.as_view(),
                           name='mark_notifications'),
                       url(r'^notification_settings/$',
                           EditNotificationSettings.as_view(),
                           name='notification_settings'),
                       url(r'mail_settings/$',
                           EditMailSettings.as_view(),
                           name='mail_settings'),
                       url(r'^employer/', include('employer.urls')),
                       url(r'^messages/', include('django_messages.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^provider/', include('provider.urls')),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),

                       url(r'^admin/', include(admin.site.urls)))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)))
