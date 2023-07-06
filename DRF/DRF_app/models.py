from django.db import models
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import AbstractBaseUser
class Role(models.Model):
    name=models.CharField()
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        *args,
        **kwargs,
    ):
        if not email:
            raise ValueError("User must have an email address")
        if super().get_queryset().filter(email=self.normalize_email(email)):
            raise ValueError("User with this email address already exists")
        user = self.model(
            email=self.normalize_email(email)
,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password=None,
    ):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, **kwargs):
        return self.model.objects.create_user(**kwargs)

class User(AbstractBaseUser):
    """
    User model
    """

    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, verbose_name=("Role"), on_delete=models.CASCADE,null=True,blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =  ["password"]
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return self.is_superuser

class Task(models.Model):    
    task = models.CharField(max_length=10000, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=2,default=0)
    def __str__(self):
        return self.task
