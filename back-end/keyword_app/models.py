from django.db import models
from django.utils import timezone
from user_app.models import CCUser
from .validators import validate_category, validate_name

# Create your models here.
class Keyword(models.Model):
    category = models.CharField(max_length=10, validators=[validate_category])
    name = models.CharField(max_length=30, validators=[validate_name])
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CCUser, on_delete=models.CASCADE, related_name='keywords')

    # Ensure duplicate keywords don't exist for user
    class Meta:
        unique_together = {'name', 'user',}