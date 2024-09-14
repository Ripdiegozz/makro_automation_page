from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class ProcessingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_file_path = models.CharField(max_length=255)
