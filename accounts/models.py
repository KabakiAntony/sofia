from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class AccountsUserManager(BaseUserManager):
    """"
    This is a custom user model manager where email is the 
    unique identifier for authentication instead of a username
    """
    def create_user(self, email, password=None, **kwargs):
        """ create a user with the given email password and other info"""
        if not email:
            raise ValueError("A User must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """ create a super user with the given email, password
        and other info. 
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    """ Using the email as the unique identifier instead of the username """
    username = None
    email = models.EmailField(unique=True, max_length=255)
    email_confirmed = models.BooleanField(default=False)
    reset_password = models.BooleanField(default=False)

    objects = AccountsUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
  

class Customer(models.Model):
    """ this holds customer information """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, max_length=255, null=True)

    def __str__(self):
        return self.email






