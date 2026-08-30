from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Author, Category
from .forms import PostForm
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string







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
        form.save_m2m()  # Сохранить связи many-to-many (категории)
        
        # Отправить уведомления подписчикам
        notify_subscribers(post)
        
        return redirect('news:post_detail', pk=post.pk)

class PostUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'



    def form_valid(self, form):
        post = form.save()
        return redirect('news:post_detail', pk=post.pk)

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

    return redirect('news:post_list')

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


@login_required
def subscribe_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.subscribers.add(request.user)

    return redirect('news:categories')

def notify_subscribers(post):
    categories = post.categories.all()

    for category in categories:
        subscribers = category.subscribers.all()

        for subscriber in subscribers:
            html_message = render_to_string(
                'email_notification.html',
                {
                    'post': post,
                    'subscriber': subscriber,
                }
            )

            send_mail(
                subject=post.headline,
                message=strip_tags(html_message),
                from_email='denisboreicko@yandex.by',
                recipient_list=[subscriber.email],
                html_message=html_message,
                fail_silently=False,
            )





