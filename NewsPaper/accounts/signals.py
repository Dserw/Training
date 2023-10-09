from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from NewsPaper.news.models import Author


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='author').exists():
        author = Author.objects.create(author=instance)
        author.rating_au = 0  # Установите начальное значение рейтинга для созданного автора
        author.save()

@receiver(post_save, sender=User)
def save_author(sender, instance, **kwargs):
    if instance.groups.filter(name='author').exists():
        instance.author.save()
# from django.contrib.auth.models import User, Group
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from NewsPaper.news.models import Author
#
# @receiver(m2m_changed, sender=User.groups.through)
# def create_author(sender, instance, action, reverse, model, pk_set, **kwargs):
#     if action == 'post_add' and not reverse:
#         author_group = Group.objects.get(name='author')
#         if author_group in instance.groups.all():
#             Author.objects.get_or_create(author=instance)
