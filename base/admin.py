from django.contrib import admin
from .models import Tag, News, Comment

# Register your models here.
admin.site.register(Tag)
admin.site.register(Comment)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',) 