from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Comment


@receiver(pre_save, sender=Comment)
def my_handler(sender, instance, **kwards):
    if instance.status:
        print("Signal triggered")
        mail = instance.author.email
        send_mail(
            'Your comment',
            'Added by the author of the post',
            from_email='ewanliw@yandex.ru',
            recipient_list=[mail],
            fail_silently=False
        )
    mail = instance.author.email
    print("фаSignal triggered")
    send_mail(
        'You have received a comment',
        'View & Add',
        from_email='ewanliw@yandex.ru',
        recipient_list=[mail],
        fail_silently=False
    )



