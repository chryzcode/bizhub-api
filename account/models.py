from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, business_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, business_name, password, **other_fields)

    def create_user(self, email, business_name, password, **other_fields):
        

        if not email:
            raise ValueError(_("The email field is required"))

        email = self.normalize_email(email)
        user = self.model(email=email, business_name=business_name, **other_fields)
        
        # user.set_password(password)
        user.is_active = True
        user.save()
        return user
    
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    business_name = models.CharField(max_length=150, unique=True)
    avatar = models.ImageField(upload_to="user-profile-images/", null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slugified_business_name = models.SlugField(max_length=255, unique=True, blank=True)
    business_description = models.TextField(max_length=500, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["business_name", "first_name", "last_name"]


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        self.slugified_business_name = slugify(self.business_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name+' '+ self.last_name
    


class Bank_Info(models.Model):
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    bank_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Bank Info"
        verbose_name_plural = "Bank Info"

    def __str__(self):
        return self.account_name
    