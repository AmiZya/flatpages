# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template

from apps.flatpages.models import Page


register = template.Library()


class PageNode(template.Node):
    def __init__(self, context_name, starts_with=None, user=None, nav=None):
        self.context_name = context_name
        if starts_with:
            self.starts_with = template.Variable(starts_with)
        else:
            self.starts_with = None
        if user:
            self.user = template.Variable(user)
        else:
            self.user = None
        if nav:
            self.nav = template.Variable(nav)
        else:
            self.nav = None

    def render(self, context):
        pages = Page.objects.filter(status=Page.PUBLISHED_STATUS)
        # If a prefix was specified, add a filter
        if self.starts_with:
            pages = pages.filter(
                url__startswith=self.starts_with.resolve(context))

        # If the provided user is not authenticated, or no user
        # was provided, filter the list to only public flatpages.
        if not context['user'].is_authenticated():
            pages = pages.filter(registration_required=False)

        if self.nav:
            pages = pages.filter(navigation_placement=self.nav.resolve(context).upper())

        context[self.context_name] = pages
        return ''


@register.tag
def get_flatpages(parser, token):
    """

    Syntax::

        {% get_flatpages ['url_starts_with'] [for user] as context_name %}

    Example usage::

        {% get_flatpages as flatpages %}
        {% get_flatpages nav 'top' as flatpages %}

        -- below syntax not applicable
        {% get_flatpages for someuser as flatpages %}
        {% get_flatpages '/about/' as about_pages %}
        {% get_flatpages prefix as about_pages %}
        {% get_flatpages '/about/' for someuser as about_pages %}
    """
    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['url_starts_with'] [for user] as context_name" %
                      dict(tag_name=bits[0]))
    # Must have at 3-6 bits in the tag
    if len(bits) >= 3 and len(bits) <= 6:

        # If there's an even number of bits, there's no prefix
        if len(bits) % 2 == 0:
            prefix = bits[1]
        else:
            prefix = None

        # The very last bit must be the context name
        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[-1]

        # If there are 5 or 6 bits, there is a user defined
        user = None
        nav = None
        if len(bits) >= 5:
            if bits[-4] == 'for':
                user = bits[-3]
            if bits[1] == 'nav':
                nav = bits[2]

        return PageNode(context_name, starts_with=prefix, user=user, nav=nav)
    else:
        raise template.TemplateSyntaxError(syntax_message)
