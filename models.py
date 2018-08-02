# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urlparse
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from managers import PageTreeObjects


class Page(MPTTModel):
    """
    Page inspired by django's flatpages at django.contrib.flatpages.models.flatpages with several customization

    Customization scope:
        - Ability to use django disqus comments for newly created articles (roadmap)
        - Use MPTT-Django to manage parent child relations to create and generate nested pages
          this can be used for nested navigation and creating neat breadcrumbs in the html layout
        - ordering: used to define the order of pages to appear in the navbar's

    """
    NAVIGATION_PLACEMENTS = (
        (u'TOP', _('Top navbar')),
        (u'FOOTER', _('Footer navbar')),
    )
    DRAFT_STATUS = 0
    PUBLISHED_STATUS = 1
    STATUSES = (
        (DRAFT_STATUS, _('Draft')),
        (PUBLISHED_STATUS, _('Published')),
    )

    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    status = models.PositiveIntegerField(_('Page status'), choices=STATUSES, default=PUBLISHED_STATUS)
    content = models.TextField(_('content'), blank=True)
    enable_comments = models.BooleanField(_('enable disqus comment'), default=False, help_text=_(
        'Disqus comments is not implemented yet, flag is kept for future potential use'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True)
    registration_required = models.BooleanField(_('registration required'), help_text=_(
        "If this is checked, only logged-in users will be able to view the page."))
    # ordering will be used by mptt and AdminSortable
    ordering = models.PositiveIntegerField(default=0)
    navigation_placement = models.CharField(max_length=20, choices=NAVIGATION_PLACEMENTS, null=True, blank=True,
                                            help_text=_('Navigation placement when chosen will determine where to '
                                                        'show the page link, if left blank it will not appear anywhere'
                                            ))
    tree = PageTreeObjects()

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    class MPTTMeta:
        order_insertion_by = ['ordering']

    def __str__(self):
        # Use django.utils.encoding.force_bytes() because value returned is unicode
        return force_bytes('%s -- %s' % (self.url, self.title))

    def __unicode__(self):
        return u'%s -- %s' % (self.url, self.title)

    def get_absolute_url(self):
        return reverse('flatpages-view', args=[self.url, ])

    def get_url(self):
        if bool(urlparse.urlparse(self.url).scheme):
            return self.url
        return self.get_absolute_url()

    # It is required to rebuild tree after save, when using order for mptt-tree
    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        Page.tree.rebuild()
