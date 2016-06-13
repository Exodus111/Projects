from django.http import HttpResponse
from django.shortcuts import render_to_response

from articles.models import Article

def articles(request):
    language = 'en'
    session_language = 'en'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    return render_to_response('articles/articles.html', {
                            'articles':Article.objects.all(),
                            'language':language,
                            'session_language':session_language})

def article(request, article_id=1):
    return render_to_response('articles/article.html', {'article':Article.objects.get(id=article_id)})

def language(request, language='en'):
    response = HttpResponse("Setting language to {}".format(language))
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response
