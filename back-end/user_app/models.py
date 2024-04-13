from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators as v
from .validators import validate_email

# Create your models here.


class CCUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
