# from django.contrib.auth.models import User
# from news.models import Author, Category, Post, Comment
# -------------1--------------------
# user1 = User.objects.create_user(username='john_doe')
# user2 = User.objects.create_user(username='jane_smith')
# -------------2--------------------
# author1 = Author.objects.create(user=user1, rating=0)
# author2 = Author.objects.create(user=user2, rating=0)
# -------------3--------------------
# cat1 = Category.objects.create(name='Спорт')
# cat2 = Category.objects.create(name='Политика')
# cat3 = Category.objects.create(name='Образование')
# cat4 = Category.objects.create(name='Культура')
#
# -------------4--------------------
# post1 = Post.objects.create(
#     author=author1,
#     post_type='AR',
#     headline='Первая статья',
#     body='Это текст первой статьи о спорте и здоровье.'
# )
# post2 = Post.objects.create(
#     author=author2,
#     post_type='NW',
#     headline='Новость дня',
#     body='Это текст новости о новых технологиях.'
# )
# post3 = Post.objects.create(
#     author=author1,
#     post_type='AR',
#     headline='Вторая статья',
#     body='Это текст второй статьи об образовании и науке.'
# )
# -------------5--------------------
# post1.categories.add(cat1, cat2)
# post2.categories.add(cat3)
# post3.categories.add(cat4)
#
# -------------6--------------------
# comment1 = Comment.objects.create(
#     post=post1,
#     user=user2,
#     text='Отличная статья!'
# )
# comment2 = Comment.objects.create(
#     post=post1,
#     user=user1,
#     text='Спасибо, приятно слышать!'
# )
# comment3 = Comment.objects.create(
#     post=post2,
#     user=user1,
#     text='Интересная новость!'
# )
# comment4 = Comment.objects.create(
#     post=post3,
#     user=user2,
#     text='Очень познавательно!'
# )
#
# -------------7--------------------
#
# post1.like()   # +1
# post1.like()   # +2
# post1.dislike() # -1
#
# post2.like()    # +1
# post2.like()    # +2
# post2.like()    # +3
#
# post3.dislike() # -1
#
# comment1.like()   # +1
# comment1.like()   # +2
#
# comment2.like()   # +1
#
# comment3.dislike() # -1
#
# comment4.like()    # +1
# comment4.like()    # +1
#
# -------------8--------------------
# author1.update_rating()
# author2.update_rating()
# -------------9--------------------
# best_author = Author.objects.order_by('-rating').first()
# print(best_author.user.username, best_author.rating)
#
# -------------10--------------------
# best_post = Post.objects.order_by('-rating').first()
# print(
#     best_post.created_at,
#     best_post.author.user.username,
#     best_post.rating,
#     best_post.headline,
#     best_post.preview()
# )
# -------------11--------------------
# for comment in best_post.comment_set.all():
#     print(
#         comment.created_at,
#         comment.user.username,
#         comment.rating,
#         comment.text
#     )
#
