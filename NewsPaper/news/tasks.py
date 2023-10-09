from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from news.models import Post, Subscriber, Category
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_notification(post_id, instance):
    post = Post.objects.get(pk=post_id)
    categories = Category.category.all()

    for category in categories:
        subscribers = Subscriber.objects.filter(category=category)
        emails = [subscriber.user.email for subscriber in subscribers]

        subject = f'Новый пост в категории {category}'

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

@shared_task
def send_weekly_newsletter():
    one_week_ago = timezone.now() - timedelta(weeks=1)
    latest_posts = Post.objects.filter(date_create__gte=one_week_ago)

    newsletter_subject = 'Еженедельная рассылка новостей'
    newsletter_message = 'Последние новости:\n\n'

    for post in latest_posts:
        newsletter_message += f'{post.head}\n'
        newsletter_message += f'Ссылка на пост: {reverse("news_detail", args=[post.pk])}\n\n'

    subscribers = Subscriber.objects.all()
    emails = [subscriber.user.email for subscriber in subscribers]

    send_mail(newsletter_subject, newsletter_message, 'ewanliw@yandex.ru', emails, fail_silently=False)