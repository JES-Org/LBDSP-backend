from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("admin", "admin"), 
        ("pharmacist", "pharmacist"),
        ("user", "user"),
    ]

    email = models.EmailField(unique=True,null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email if self.email else self.phone_number 

    def clean(self):
        if not self.email and not self.phone_number:
            raise ValueError("Either email or phone number must be provided")