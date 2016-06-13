from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin

from .models import Category, SubCategory, Article

class ArticleAdmin(MarkdownModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Article, ArticleAdmin)
