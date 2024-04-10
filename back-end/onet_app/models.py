from django.db import models
from openai_app.models import Occupation

# Create your models here.
class Details(models.Model):
    onet_name = models.CharField(blank=False, null=False, max_length=150)
    description = models.CharField(blank=False, null=False)
    tasks = models.JSONField(default=dict)
    alt_names = models.JSONField(default=dict)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, related_name="details")
