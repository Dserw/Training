import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from news.models import Post, Subscriber, Category

logger = logging.getLogger(__name__)


def my_job():
    last_week = datetime.now() - timedelta(days=7)
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        user = subscriber.user
        category = subscriber.category
        new_posts = Post.objects.filter(
            category=category,
            date_create__gte=last_week
        )
        if new_posts:
            subject = f'Новости в категории {category}'
            text_content = f'Подписанные вами новости в категории {category}:\n\n'
            html_content = f'<p>Подписанные вами новости в категории {category}:</p>'

            for post in new_posts:
                text_content += f'{post.head}\n'
                html_content += f'<p><a href="http://127.0.0.1:8000/{post.get_absolute_url()}">{post.head}</a></p>'


            send_mail(subject, text_content, 'ewanliw@yandex.ru', [user.email], html_message=html_content)



@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="20", hour="10"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="fri",  # Каждую пятницу
                hour="18",  # В 18:00
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")