from django.db import models
from django_markdown.models import MarkdownField

class Article(models.Model):
    title = models.CharField(max_length=200)
    body = MarkdownField()
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, default=title)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
