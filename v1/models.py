import hashlib

from django.db import models
from django.utils import timezone
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import (BaseUserManager, AbstractUser, PermissionsMixin)
# from django.contrib.auth.backends import ModelBackend

class UserManager(BaseUserManager):
    def _create_user(self, id, username, password=None, **extra_fields):
        if not id:
            raise ValueError('No ID')
        user = self.model(id=id, username=username, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, id, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(id, username, password, **extra_fields)

    def create_superuser(self, id, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Administrator must be 'is_staff' is True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Administrator must be 'is_superuser' is True")

        return self._create_user(id, username, password, **extra_fields)

# class UserAuth(ModelBackend):
#     def authenticate(self, **kwargs):
#         id = kwargs.get('id')
#         password = kwargs.get('password')
#         UserModel = get_user_model()
#         try:
#             user = User.objects.get(id=id)
#         except:
#             return None
#         if user.check_password(password):
#             return user
#         return None

class User(AbstractUser):
    objects = UserManager()
    id = models.CharField(verbose_name='ID', null=False, primary_key=True, max_length=10)
    username = models.CharField(verbose_name='User\'s username', null=False, max_length=10, default='익명')
    password = models.CharField(verbose_name='Username', null=False, max_length=100)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['username']
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    def __str__(self):
        return self.id

    def get_short_name(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class fineDustInfo(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE, null=False, primary_key=True)
    firstCityName = models.CharField(max_length=50, null=True)
    lastCityName = models.CharField(max_length=50, null=True)
    fullCityName = models.CharField(max_length=100, null=True)
    fineDust = models.CharField(null=True, max_length=10, verbose_name='good-bad-worst')
    fineDustValue = models.IntegerField(null=True)

