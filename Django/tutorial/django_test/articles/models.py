from django.db import models

class Article(models.Model):
    title = models.TextField(max_length=200)
    body = models.TextField()
    likes = models.IntegerField(default=0)


class Comment(models.Model):
    article = models.ForeignKey(Article)
    text = models.TextField()
