"""
Models to build and manage User profiles and settings
"""

# stdlib
from datetime import date

# django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from sorl.thumbnail import ImageField


def profile_image(instance, filename: str) -> str:
    """
    Generate user profile photo filename from username
    """
    return f"users/{instance.user.username}/profile_image.{filename.split('.')[-1]}"


def user_photo(instance, filename: str) -> str:
    """
    Generate user photo filename from username
    """
    return f"users/{instance.profile.user.username}/photos/{filename}"


def age(born: date) -> int:
    """
    Returns how old a given date is as year int
    """
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Profile(models.Model):
    """
    Profile info to add on top of the auth.User model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Login IDs
    # facebook_id = models.CharField(max_length=200, blank=True, unique=True)

    # Public Profile
    image = ImageField(blank=True, upload_to=profile_image)
    name = models.CharField(max_length=128, blank=True)
    alt = models.CharField(max_length=128, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=64, blank=True)

    # Social Buttons
    external_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_user = models.CharField(max_length=15, blank=True)
    instagram_user = models.CharField(max_length=30, blank=True)

    # Visibility Flags
    show_email = models.BooleanField(default=False)
    searchable = models.BooleanField(default=True)

    # Config
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def display_name(self) -> str:
        """
        Returns the desired display name for the user
        """
        return self.alt or self.name

    @property
    def age(self) -> int:
        """
        Returns the user's age as an int
        """
        return age(self.birth_date)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Profile {self.name} - {self.user.username}>"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a profile for a new User model
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class UserPhoto(models.Model):
    """
    Photos associated with a user profile
    """

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="photos"
    )
    image = ImageField(upload_to=user_photo)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-pk"]
