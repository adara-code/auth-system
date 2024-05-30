from django.db import models
from datetime import datetime
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff must value to True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser must value to True")
        
        return self.create_user(self, email, password, **extra_fields)
        


class UserRegistration(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    full_name = models.CharField (max_length=254)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=str(datetime.now()))
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomManager()
    
    def __str__(self):
        return self.full_name
    
    
    