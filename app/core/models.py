from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """ provide helpers for creating user / superuser """

    def create_user(self, email, password=None, **extra_fields):
        """ creating new user """
        if not email:
            raise ValueError('Email is required for creating user')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ create new superuser """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ custom user model that use email instead of username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    exp = models.IntegerField(default=0)
    about = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ tag model """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    """ category model """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Feed(models.Model):
    """ feed model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    feed = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=10, decimal_places=2)
    long = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    location_lat = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2
    )
    location_long = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2
    )
    location_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.feed


class Like(models.Model):
    """ like model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feed.feed


class Comment(models.Model):
    """ comment model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
