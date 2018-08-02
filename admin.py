from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mptt.admin import MPTTModelAdmin
import reversion
from suit.admin import SortableModelAdmin
from models import Page
from forms import PageForm


class PageAdmin(MPTTModelAdmin, SortableModelAdmin, reversion.VersionAdmin):
    form = PageForm
    mptt_level_indent = 20
    fieldsets = (
        (None, {'fields': ('url', 'title', 'parent', 'content', )}),
        (_('Advanced options'),
         {'classes': ('collapse',),
          'fields': ('enable_comments', 'navigation_placement', 'registration_required', 'template_name')}),
    )
    list_display = ('title', 'parent', 'url', 'registration_required', 'status', 'navigation_placement')
    list_filter = ('enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    list_editable = ('status', 'navigation_placement')
    sortable = 'ordering'


admin.site.register(Page, PageAdmin)
