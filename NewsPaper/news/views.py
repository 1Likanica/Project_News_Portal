from django.shortcuts import render, redirect
from django.views.generic import *
from django.views.generic.base import View
from .models import *
from .filters import PostFilter
from datetime import datetime
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "post_edit.html"
    permission_required = ('news.add_post',)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post', )


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


@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(authorUser=user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    return redirect('/news/')


# def error_404(request, exception):
#     return render(request, 'errors/404.html')


def error_403(request, exception):
    return render(request, 'errors/403.html')
