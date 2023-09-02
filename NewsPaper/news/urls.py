from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

handler403 = 'news.views.error_403'

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name = 'news.html'),
    path('authors/', AuthorsPage.as_view()),

    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),

    path('search/', PostSearch.as_view(), name='search'),

    path('news/upgrade/', upgrade_me, name='upgrade'),
    path('upgrade/', upgrade_me, name='upgrade'),

    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]

