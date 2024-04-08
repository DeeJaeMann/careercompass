from django.db import models
from django.utils import timezone
from user_app.models import CCUser
from .validators import validate_onet_code

# Create your models here.
class Occupation(models.Model):
    name= models.CharField(blank=False, null=False, max_length=150)
    onet_code = models.CharField(blank=False, null=False, max_length=10, validators=[validate_onet_code])
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CCUser, on_delete=models.CASCADE, related_name="occupations")

    class Meta:
        unique_together = ('onet_code','user')