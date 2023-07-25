from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, username, fname, lname, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            fname = fname,
            lname = lname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fname, lname, password):
        user = self.create_user(
            email,
            password=password,
            username=username,
            fname=fname,
            lname=lname,
        )
        user.is_admin = True
        user.is_staff= True
        user.is_supperuser=True

        user.save(using=self._db)
        return user
    
class MyUser(AbstractUser):

    email = models.EmailField(verbose_name='eamil', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    fname = models.CharField(max_length=60)
    lname = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email", "fname", "lname"]
    
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username} - {self.email}"    
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True