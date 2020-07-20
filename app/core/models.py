import uuid
import os

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                        PermissionsMixin
from django.conf import settings


def image_path(instance, filename):
    """ generate filepath for images """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/images/', filename)


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
    image = models.ImageField(null=True, upload_to=image_path)
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
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feed


class FeedImage(models.Model):
    """ feed image """
    feed = models.ForeignKey(
        Feed,
        related_name='image_feed',
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, upload_to=image_path)


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


class Community(models.Model):
    """ community model """
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=10, decimal_places=2)
    long = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=image_path)

    def __str__(self):
        return self.name


class CommunityMember(models.Model):
    """ community member model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    is_joined = models.BooleanField(default=False)

    def __str__(self):
        return self.community.name


class CommunityDiscussion(models.Model):
    """ community discussion model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class DiscussionImage(models.Model):
    """ discussion image """
    discussion = models.ForeignKey(
        CommunityDiscussion,
        related_name='discussion_image',
        on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, upload_to=image_path)


class DiscussionComment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    discussion = models.ForeignKey(
        CommunityDiscussion,
        on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class DiscussionLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    discussion = models.ForeignKey(
        CommunityDiscussion,
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
