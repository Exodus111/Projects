from django.shortcuts import render_to_response
from .models import Category, SubCategory, Article

def index(request):
    return render_to_response('articles/index.html', {'categories':Category.objects.all(),
                                                      'subcategories':SubCategory.objects.all()})

def sub(request, subcategory_id=1):
    subcategory = SubCategory.objects.get(id=subcategory_id)
    selected_articles = Article.objects.filter(category_id=subcategory.id)

    return render_to_response('articles/temp.html', {'articles':selected_articles,
                                                     'categories':Category.objects.all(),
                                                     'subcategories':SubCategory.objects.all(),
                                                     'sub':subcategory})

def article(request, slug):
    article = Article.objects.get(slug=slug)
    return render_to_response('articles/article.html', {'article':article, 'categories':Category.objects.all(), 'subcategories':SubCategory.objects.all()})
