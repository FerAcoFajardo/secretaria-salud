from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randrange
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    image = models.ImageField(upload_to='profiles/', max_length=255, blank=True, null=True, default='profiles/generic/blank-profile-pic.png')
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    dark_mode = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']