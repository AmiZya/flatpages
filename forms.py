# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from mptt.forms import TreeNodeChoiceField
from redactor.widgets import RedactorEditor
from models import Page
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _


class PageForm(forms.ModelForm):
    """
    PageForm

    """
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
                           help_text=_("Example: '/about/contact/'. Make sure to have leading"
                                       " and trailing slashes."),
                           error_message=_("This value must contain only letters, numbers,"
                                           " dots, underscores, dashes, slashes or tildes."))

    class Meta:
        model = Page

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            queryset = Page.tree.all().exclude(pk=self.instance.id)
        else:
            queryset = Page.tree.all()

        self.fields['parent'] = TreeNodeChoiceField(queryset=queryset, level_indicator=u'+--')
        self.fields['parent'].required = False

    #TODO: Add validation to navigation_placement
    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('/'):
            raise forms.ValidationError(ugettext("URL is missing a leading slash."))
        if (settings.APPEND_SLASH and
                    'django.middleware.common.CommonMiddleware' in settings.MIDDLEWARE_CLASSES and
                not url.endswith('/')):
            raise forms.ValidationError(ugettext("URL is missing a trailing slash."))
        return url

    def clean(self):
        url = self.cleaned_data.get('url', None)
        sites = self.cleaned_data.get('sites', None)

        same_url = Page.objects.filter(url=url)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        if sites and same_url.filter(sites__in=sites).exists():
            for site in sites:
                if same_url.filter(sites=site).exists():
                    raise forms.ValidationError(
                        _('Page with url %(url)s already exists for site %(site)s' %
                          {'url': url, 'site': site}))

        return super(PageForm, self).clean()




