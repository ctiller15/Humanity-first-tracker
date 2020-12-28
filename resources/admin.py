from django.contrib import admin

from django.utils.html import format_html
from resources.models import Resource

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'link', 'order', 'hidden')
    fields = ('title', 'summary', 'link', 'order', 'hidden')

admin.site.register(Resource, ResourceAdmin)
