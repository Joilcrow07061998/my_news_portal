from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post, Author
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group




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
        context['is_not_author'] = not self.request.user.groups.filter(
            name='authors'
        ).exists()
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


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        post = form.save(commit=False)
        post.post_type = self.kwargs.get('post_type', 'NW')
        post.author = author
        post.save()
        return redirect('post_detail', pk=post.pk)

class PostUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'



    def form_valid(self, form):
        post = form.save()
        return redirect('post_detail', pk=post.pk)

class PostDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'post_delete.html'
    permission_required = 'news.delete_post'

@login_required
def become_author(request):
    authors_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(request.user)

    return redirect('post_list')
