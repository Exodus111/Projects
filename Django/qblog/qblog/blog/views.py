from django.views import generic
from . import models

class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "home.html"
    paginate_by = 2



