from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin

from .models import Article

class ArticleAdmin(MarkdownModelAdmin):
    pass

admin.site.register(Article)
