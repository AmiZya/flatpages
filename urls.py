# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import PageView, HomeView

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^p/pages(?P<url>.*)$', PageView.as_view(), name='flatpages-view'),
                       url(r'^p/static/why-us/$', TemplateView.as_view(template_name='flatpages/why-us.html'),
                           name='flatpages-why-us'),
)
