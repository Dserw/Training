from celery import shared_task
from django.core.mail import send_mail
from portapp.models import Post


@shared_task
def new_post():
    for users in Post.objects.all():
        send_mail(
            subject='Новости портала',
            message='На портале создано новое объявление',
            from_email='ewanliw@yandex.ru',
            recipient_list=[users.email],
        )
