from django.contrib.auth.models import User
from django.db import models

from news.models import Category


#  class Subscriber(models.Model):
#     user = models.ForeignKey(
#         to=User,
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#     )
#     category = models.ForeignKey(
#         to=Category,
#         on_delete=models.CASCADE,
#         related_name='subscriptions',
#     )
