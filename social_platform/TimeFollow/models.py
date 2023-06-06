from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    postContent = models.CharField(max_length=200, null=False)
    timeStamp = models.DateTimeField(null=False, default=datetime.now())