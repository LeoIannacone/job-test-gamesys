from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uid = models.CharField(max_length=120, primary_key=True)
    friends = models.ManyToManyField('self')
