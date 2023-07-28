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


class AuthorsPage(ListView):
    model = Author
    context_object_name = "Authors"
    template_name = 'news/authors.html'


class PostDetail(View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "news/posts.html", {'ps':ps})


class PostList(ListView):
    model = Post
    ordering = 'id'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"

    def form_valid(self, form):
        post_n = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post_n.categoryType = 'NW'
            elif path_info == '/article/create/':
                post_n.categoryType = 'AR'
            post_n.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news.html')


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context
