from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from DRF.settings import EMAIL_HOST_USER

class Role(models.Model):
    name = models.CharField(max_length=255)

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
        if self.get_queryset().filter(email=self.normalize_email(email)).exists():
            raise ValueError("User with this email address already exists")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        subject = "Change password"
        recipients = (user.email,)
        id = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        link = f"http://127.0.0.1:5500/DRF/DRF_app/password/{id}/{token}/"

        body = f"Click the following link to reset your password: {link}"
        sender_email = EMAIL_HOST_USER
        message = f"Subject: {subject}\n\n{body}  "
    
        try:
            send_mail(subject, message, sender_email,
                      recipients, fail_silently=False)
        except Exception as e:
            print("e: ", e)
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
# class UserManager(BaseUserManager):
#     def create_user(
#         self,
#         email,
#         password=None,
#         *args,
#         **kwargs,
#     ):
#         if not email:
#             raise ValueError("User must have an email address")
#         if self.get_queryset().filter(email=self.normalize_email(email)).exists():
#             raise ValueError("User with this email address already exists")
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save(using=self._db)

#         subject = "Change password"
#         recipients = (user.email,)
#         id = urlsafe_base64_encode(force_bytes(user.id))
#         token = PasswordResetTokenGenerator().make_token(user)
#         # link = f"http://192.168.0.155:3000/change-password?id={id}&token={token}"
#         link = f"http://127.0.0.1:8000/verify_link/{id}/{token}/    "
#         body = f"Click the following link to reset your password: {link}"
#         sender_email = EMAIL_HOST_USER
#         message = f"Subject: {subject}\n\n{body}"

#         try:
#             send_mail(subject, message, sender_email,
#                       recipients, fail_silently=False)
#         except Exception as e:
#             print("e: ", e)
#         return user

#     def create_superuser(
#         self,
#         email,
#         password=None,
#     ):
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

#     def create(self, **kwargs):
#         return self.model.objects.create_user(**kwargs)


class User(AbstractBaseUser):
    """
    User model
    """

    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, verbose_name=(
        "Role"), on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    is_verify = models.BooleanField(("Is Verify"), default=False)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Task(models.Model):
    task = models.CharField(max_length=10000, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=2, default=0)

    def __str__(self):
        return self.task

