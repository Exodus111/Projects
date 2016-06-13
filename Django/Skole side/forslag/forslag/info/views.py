from django.shortcuts import render
from django.views import generic

from .models import Entry

class IndexView(generic.ListView):
    #queryset = Entry.objects.published()
    template_name = 'info/index.html'
    context_object_name = 'my_entries'

    def get_queryset(self):
        return Entry.objects.published()
