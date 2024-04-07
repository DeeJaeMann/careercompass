from django.db import models
from django.utils import timezone
from django.core import validators as v
from user_app.models import CCUser

# Create your models here.
class Keyword(models.Model):
    category = models.CharField()
    name = models.CharField()
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CCUser, on_delete=models.CASCADE, related_name='keywords')