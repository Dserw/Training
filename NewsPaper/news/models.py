from django.contrib.auth.models import User, AbstractUser
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse



class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_au = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.author.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.rating_au = pRat*3 + cRat
        self.save()

    def __str__(self):
        return self.author.username


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


    def __str__(self):
        return self.category


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    head = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=CHOICES, default=ARTICLE)
    date_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.head.title()} - {self.text[:32]}'

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        max_length = 124
        if len(self.text) <= max_length:
            return self.text
        else:
            return self.text[:max_length] + '...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    def get_absolute_url(self):
        return reverse('news', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
