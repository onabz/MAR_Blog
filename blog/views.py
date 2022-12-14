from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Article
from .forms import CommentForm


class ArticleView(ListView):
    model = Article
    template_name = 'index.html'
    queryset = Article.objects.filter(status=1).order_by('-date_created')
    paginate_by = 4


class AboutView(CreateView):
    model = Article
    template_name = 'about.html'
    fields = '__all__'


class ArticleDetailView(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(
            approved=True).order_by('date_created')
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "article.html",
            {
                "article": article,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.filter(
            approved=True).order_by('date_created')
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "article.html",
            {
                "article": article,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class ArticleLike(View):

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        if article.likes.filter(id=self.request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)

        return HttpResponseRedirect(reverse('article_detail', args=[slug]))


class AddArticleView(CreateView):
    model = Article
    template_name = 'add_article.html'
    fields = (
        'title', 'slug', 'excerpt', 'body',
        'featured_image', 'status')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        return redirect(reverse('home'))


class UpdateArticleView(UpdateView):
    model = Article
    template_name = 'update_article.html'
    fields = (
        'title', 'slug', 'excerpt', 'body',
        'featured_image', 'status')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        return redirect(reverse('home'))


class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'delete_article.html'
    success_url = reverse_lazy('home')
