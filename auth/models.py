from django.db import models
from django.contrib.auth.models import User
import uuid


class Post(models.Model):
    id = models.UUIDField(Primary_key=True, default=uuid.uuid64, help_text='Unique ID for each post')
    body = models.CharField(max_length=512)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
