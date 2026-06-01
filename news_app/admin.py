from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created', 'date_updated']
    list_filter = ['author', 'date_created']
    search_fields = ['title', 'content']
    readonly_fields = ['date_created', 'date_updated']