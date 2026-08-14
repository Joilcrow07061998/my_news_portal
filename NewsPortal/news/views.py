from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from .filters import PostFilter
from django.shortcuts import reverse


class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formatted_news = []
        for post in context['news']:
            post.formatted_date = post.created_at.strftime('%m/%d/%Y')
            formatted_news.append(post)
        context['formatted_news'] = formatted_news
        return context

    def get_queryset(self):
        return Post.objects.filter(post_type='NW').order_by('-created_at')


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'].formatted_date = context['post'].created_at.strftime("%d.%m.%Y")
        return context


class SearchView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class NewsUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class NewsDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post_delete.html'


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class ArticleDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post_delete.html'