# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MongoData(models.Model):
    text = models.TextField()
    
class Employee(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)
