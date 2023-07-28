from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# simple
# class User(AbstractUser):
#     last_login_ip = models.GenericIPAddressField(null=True, blank=True)


# flexible
class LoginIPAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
