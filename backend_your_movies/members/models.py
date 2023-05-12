from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class UserManager(UserManager):
    def create_user(self, username, email, password=None):
        if email is None:
            raise TypeError('The Email field must be set')
        if username is None:
            raise TypeError('The Username field must be set')
        if password is None:
            raise TypeError('The password field must be set')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password shouldnt be none')
        user=self.create_user(username, email, password)
        user.is_superuser = True
        user.is_active=True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractUser, PermissionsMixin):
    is_active=models.BooleanField(default=False)
    custom=models.CharField(max_length=500, default='')
    email=models.EmailField(unique=True)


    REQUIRED_FIELDS=['username', 'password']
    USERNAME_FIELD='email'
    
    objects=UserManager()
    
    def __str__(self):
        return super().__str__()
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }