# encoding: utf-8
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .forms import (AuthenticationForm, PasswordResetCustomerForm,
                    SetPasswordCustomerForm)
from accounts.views import RegistrationView


urlpatterns = patterns('django.contrib.auth.views',
                       url(r'^login/$', 'login',
                           {'template_name': 'accounts/login.html',
                            'authentication_form': AuthenticationForm},
                           name='auth_login'),
                       url(r'^logout/$', 'logout',
                           {'template_name': 'accounts/logged_out.html'},
                           name='auth_logout'),
                       url(r'^password/change/$', 'password_change',
                           {'template_name': 'accounts/password_change.html'},
                           name='auth_password_change'),
                       url(r'^password/change/done/$', 'password_change_done',
                           {
                               'template_name': 'accounts/password_change_done.html'},
                           name='password_change_done'),
                       url(r'^password/reset/$', 'password_reset',
                           {'template_name': 'accounts/password_reset.html',
                            'email_template_name': 'accounts/mails/password_reset_email.html',
                            'password_reset_form': PasswordResetCustomerForm},
                           name='auth_password_reset'),
                       url(
                           r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                           'password_reset_confirm',
                           {
                               'template_name': 'accounts/password_reset_confirm.html',
                               'set_password_form': SetPasswordCustomerForm},
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           'password_reset_complete',
                           {
                               'template_name': 'accounts/password_reset_complete.html'},
                           name='password_reset_complete'),
                       url(r'^password/reset/done/$', 'password_reset_done',
                           {
                               'template_name': 'accounts/password_reset_done.html'
                           },
                           name='password_reset_done'))

urlpatterns += patterns('',
                        url(r'^registration/$', RegistrationView.as_view(),
                            name='registration'),
                        url(r'^employer/profile/$', TemplateView.as_view(
                            template_name='accounts/registration.html'),
                            name='registration_type'),
)
