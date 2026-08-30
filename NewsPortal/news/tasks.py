# from datetime import timedelta
#
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils import timezone
# from django.utils.html import strip_tags
#
# from .models import Post
#
#
# def get_weekly_posts():
#     week_ago = timezone.now() - timedelta(days=7)
#
#     return Post.objects.filter(
#         created_at__gte=week_ago
#     ).order_by('-created_at')
#
#
# def send_weekly_newsletter():
#     posts = get_weekly_posts()
#
#     if not posts.exists():
#         return
#
#     users = User.objects.filter(
#         sub_categories__isnull=False
#     ).distinct()
#
#     for user in users:
#         categories = user.sub_categories.all()
#
#         user_posts = posts.filter(
#             categories__in=categories
#         ).distinct()
#
#         if not user_posts.exists():
#             continue
#
#         html_message = render_to_string(
#             'weekly_newsletter.html',
#             {
#                 'subscriber': user,
#                 'posts': user_posts,
#             }
#         )
#
#         send_mail(
#             subject='Новые статьи за неделю',
#             message=strip_tags(html_message),
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[user.email],
#             html_message=html_message,
#             fail_silently=False,
#         )
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from .models import Post


def get_weekly_posts():
    week_ago = timezone.now() - timedelta(days=7)

    return Post.objects.filter(
        created_at__gte=week_ago
    ).order_by('-created_at')


def send_weekly_newsletter():
    print('=== START NEWSLETTER ===')

    posts = get_weekly_posts()

    print('Статей за неделю:', posts.count())

    if not posts.exists():
        print('Нет статей за неделю')
        return

    users = User.objects.filter(
        sub_categories__isnull=False
    ).distinct()

    print('Пользователей найдено:', users.count())

    for user in users:
        print('Пользователь:', user.username)
        print('Email:', user.email)

        categories = user.sub_categories.all()

        print(
            'Категории:',
            list(categories.values_list('name', flat=True))
        )

        user_posts = posts.filter(
            categories__in=categories
        ).distinct()

        print('Статей для пользователя:', user_posts.count())

        if not user_posts.exists():
            print('Нет подходящих статей')
            continue

        html_message = render_to_string(
            'weekly_newsletter.html',
            {
                'subscriber': user,
                'posts': user_posts,
            }
        )

        print('Шаблон письма сформирован')

        send_mail(
            subject='Новые статьи за неделю',
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        print('ПИСЬМО ОТПРАВЛЕНО:', user.email)

    print('=== END NEWSLETTER ===')