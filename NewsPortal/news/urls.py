from django.urls import path, include
from .views import PostList, PostDetail, SearchView, PostCreate, PostUpdate, PostDelete, CategoryList, subscribe_category
from .views import become_author

app_name = 'news'


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', SearchView.as_view(), name='search'),

    path('create/', PostCreate.as_view(), {'post_type': 'NW'}, name='news_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('articles/create/', PostCreate.as_view(), {'post_type': 'AR'}, name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('become-author/', become_author, name='become_author'),
    path('categories/', CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/subscribe/',subscribe_category,name='subscribe_category'),
]
