from django.db import models
from django_markdown.models import MarkdownField

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Sub-Categories'



class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(default=None)
    body = MarkdownField()
    teaser = models.CharField(max_length=500, default=None)
    category = models.ForeignKey(SubCategory)
    slug = models.SlugField(unique=True, default=None)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
