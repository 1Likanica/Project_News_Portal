from django.urls import path
from .views import *

urlpatterns = [
    path('', news_page_list, name = 'news.html'),
    path('authors/', AuthorsPage.as_view()),

    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]

