# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import loader, RequestContext
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView

from constance import config
from models import Page


class HomeView(TemplateView):
    """
    HomeView(TemplateView)
    """
    template_name = "flatpages/home.html"

    def get(self, request, *args, **kwargs):
        """ landing page / home page """

        if config.BETA_MODE:
            if request.user.is_anonymous() or not request.user.eligible_for_beta():
                return redirect(reverse('beta-view'))

        return super(HomeView, self).get(request, *args, **kwargs)


class PageView(View):
    """
    Public interface to the flat page view.

    Models: `flatpages.page`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.page` object

    This class is called from FlatpageFallbackMiddleware.process_response
    when a 404 is raised, which often means CsrfViewMiddleware.process_view
    has not been called even if CsrfViewMiddleware is installed. So we need
    to use @csrf_protect, in case the template needs {% csrf_token %}.
    However, we can't just wrap this view; if no matching flatpage exists,
    or a redirect is required for authentication, the 404 needs to be returned
    without any CSRF checks. Therefore, we only
    CSRF protect the internal implementation.

    """
    DEFAULT_TEMPLATE = 'flatpages/default.html'

    def get(self, request, url):
        if not url.startswith('/'):
            url = '/' + url

        filter_kwargs = {'status': Page.PUBLISHED_STATUS, 'url__exact': url}

        try:
            if request.user.is_superuser and request.user.is_staff:
                filter_kwargs.pop('status')

            f = get_object_or_404(Page, **filter_kwargs)
        except Http404:
            if not url.endswith('/') and settings.APPEND_SLASH:
                return HttpResponsePermanentRedirect('%s/' % request.path)
            else:
                raise
        return self.render_flatpage(request, f)

    @method_decorator(csrf_protect)
    def render_flatpage(self, request, f):
        """
        Internal interface to the flat page view.
        """
        # If registration is required for accessing this page, and the user isn't
        # logged in, redirect to the login page.
        if f.registration_required and not request.user.is_authenticated():
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.path)
        if f.template_name:
            t = loader.select_template((f.template_name, self.DEFAULT_TEMPLATE))
        else:
            t = loader.get_template(self.DEFAULT_TEMPLATE)

        # To avoid having to always use the "|safe" filter in flatpage templates,
        # mark the title and content as already safe (since they are raw HTML
        # content in the first place).
        f.title = mark_safe(f.title)
        f.content = mark_safe(f.content)

        c = RequestContext(request, {
            'flatpage': f,
        })
        response = HttpResponse(t.render(c))
        return response

