from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formatted_news= []
        for post in context['news']:
            post.formatted_date = post.created_at.strftime('%m/%d/%Y')
            formatted_news.append(post)

        context['formatted_news'] = formatted_news
        return context

    # Переопределяем метод get_queryset. Это самый надежный способ.
    def get_queryset(self):
        # Берем все посты, фильтруем только те, у которых post_type = 'NW'
        # и сортируем по дате создания (от новых к старым)
        return Post.objects.filter(post_type='NW').order_by('-created_at')


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # То же самое форматирование для детальной страницы
        context['post'].formatted_date = context['post'].created_at.strftime("%d.%m.%Y")
        return context
