from django.contrib import admin

# Register your models here.

from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publish', 'category', 'create_dt')

admin.site.register(News, NewsAdmin)