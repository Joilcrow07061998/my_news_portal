import django_filters
from django import forms
from .models import Post

class PostFilter(django_filters.FilterSet):
    headline = django_filters.CharFilter(
        field_name='headline',
        lookup_expr='icontains',
        label='По названию'
    )
    author__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='По имени автора'
    )

    created_at__gte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),  # <-- Это магия!
        label='Позже даты'
    )

    class Meta:
        model = Post
        fields = ['headline', 'author__username', 'created_at__gte']