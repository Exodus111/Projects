from django.shortcuts import render_to_response
from .models import Article

def home(request):
    return render_to_response('articles/home.html', {'articles':Article.objects.all()})

def article(request, slug):
    article = Article.objects.get(slug=slug)
    return render_to_response('articles/article.html', {'article':article})
