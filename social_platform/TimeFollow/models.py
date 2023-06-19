from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
User=settings.AUTH_USER_MODEL

# Create your models here.

# Model for posts created by the user.
class Post(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    postContent = models.CharField(max_length=200, null=False)
    timeStamp = models.DateTimeField(null=False, default=datetime.now())

# Custom user model.
class CustomUser(AbstractUser):
    phone_num = PhoneNumberField(null=True)