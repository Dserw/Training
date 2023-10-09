from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.urls import reverse

from .models import Post, Subscriber, Category, Author


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        categories = Category.objects.all()
        print('for', categories)
        for category in categories:
            subscribers = Subscriber.objects.filter(category=category)
            emails = [subscriber.user.email for subscriber in subscribers]

            subject = f'Новый пост в категории {instance.category}'

            text_content = (
                f'Заголовок: {instance.head}\n'
                f'Краткое содержание: {" ".join(instance.text.split()[:10])}\n\n'
                f'Ссылка на пост: {reverse("news_detail", args=[instance.pk])}'
            )
            html_content = (
                f'Заголовок: {instance.head}<br>'
                f'Краткое содержание: {" ".join(instance.text.split()[:10])}<br><br>'
                f'Ссылка на пост: {reverse("news_detail", args=[instance.pk])}'
                f'Ссылка на пост</a>'
            )
            for email in emails:
                msg = EmailMultiAlternatives(subject, text_content, None, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()


