import allauth
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from allauth.account.models import EmailAddress as AllAuthEmailAddress


# Create your models here.
class Post(models.Model):
    CHOICES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=64)
    text = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=32, choices=CHOICES)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    upload = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.text[:32]}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:16]
