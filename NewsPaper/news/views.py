from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
# from django.views.generic.edit import FormView
from django.views.generic.base import View
from .models import *
from django import template
from .filters import PostFilter
from datetime import datetime
from .forms import PostForm
from django.urls import reverse_lazy

register = template.Library()


@register.filter()
def censor(value):
    bad_words = ['Идиот', 'Дурак', 'Дебил', 'Гад']

    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

    for word in value.split():
        if word.lower() in bad_words:
            value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
    return value


class AuthorsPage(ListView):
    model = Author  # queryset = Author.objects.all()
    context_object_name = "Authors"
    template_name = 'news/authors.html'


class PostDetail(View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "news/posts.html", {'ps':ps})


def news_page_list(request):
    """ Представление для вывода страницы с новостями по заданию D3.6 """

    newslist = Post.objects.all().order_by('-rating')[:6]

    return render(request, 'news/news.html', {'newslist': newslist})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
# Create your views here.


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news.html')