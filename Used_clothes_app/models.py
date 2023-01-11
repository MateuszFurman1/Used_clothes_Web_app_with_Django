from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    father_name = models.CharField(max_length=128, null=True)
    mother_name = models.CharField(max_length=128, null=True)
