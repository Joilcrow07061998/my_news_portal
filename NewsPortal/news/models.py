
from django.db import models
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username



    def update_rating(self):
        post_rating = sum(post.rating for post in self.post_set.all()) * 3

        comment_rating = sum(comment.rating for comment in self.user.comment_set.all())

        posts_of_author = self.post_set.all()
        comment_to_posts_rating = 0
        for post in posts_of_author:
            comment_to_posts_rating += sum(comment.rating for comment in post.comment_set.all())

        self.rating = post_rating + comment_rating + comment_to_posts_rating
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    subscribers = models.ManyToManyField(User,
    blank=True,
    related_name='sub_categories'
    )

    def __str__(self):
        return self.name





class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Cтатья'),
        (NEWS, 'Новость'),
    ]

    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)


    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    headline = models.CharField(max_length=200)
    body = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.body[:125] + '...'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user



