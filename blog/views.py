from django.shortcuts import render
from django.views import generic
from .models import Article


class ArticleView(generic.ListView):
    model = Article
    template_name = 'index.html'
    queryset = Article.objects.filter(status=1).order_by('-date_created')
    paginate_by = 4


class AboutView(generic.CreateView):
    model = Article
    template_name = 'about.html'
    fields = '__all__'

