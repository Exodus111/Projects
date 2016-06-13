from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^all/$', 'articles.views.articles'),
    url(r'^get/(?P<article_id>\d+)/$', 'articles.views.article'),
    url(r'^language/(?P<language>[a-z\-]+)/$', 'articles.views.language'),
]
