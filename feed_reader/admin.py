from django.contrib import admin
from django.utils.html import format_html

from feed_reader.models import Entry, Category

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'category', 'hidden', 'show_article_link')
    list_filter = ('category', 'hidden')
    fields=('title', 'summary', 'category', 'hidden', 'link', 'updated')
    readonly_fields=['title', 'summary', 'category', 'link']
    search_fields = ('title', 'summary')

    def show_article_link(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)

    show_article_link.short_description = "article link"

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
