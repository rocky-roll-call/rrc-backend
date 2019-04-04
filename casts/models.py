"""
Models to build and manage User profiles and settings
"""

# stdlib
from datetime import date

# django
from django.db import models
from django.utils import text, timezone
from sorl.thumbnail import ImageField


def cast_logo(instance, filename: str) -> str:
    """
    Generate cast logo filename from cast slug
    """
    return f"casts/{instance.slug}/logo.{filename.split('.')[-1]}"


def cast_photo(instance, filename: str) -> str:
    """
    Generate cast photo filename from cast slug
    """
    return f"casts/{instance.cast.slug}/photos/{filename}"


class Cast(models.Model):
    """
    Basic Rocky Horror cast info
    """

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    logo = ImageField(blank=True, upload_to=cast_logo)
    email = models.EmailField(max_length=128)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    modified_date = models.DateTimeField(default=timezone.now)

    managers = models.ManyToManyField("users.Profile", related_name="managed_casts")
    members = models.ManyToManyField("users.Profile", related_name="member_casts")
    member_requests = models.ManyToManyField(
        "users.Profile", related_name="requested_casts"
    )
    blocked = models.ManyToManyField("users.Profile", related_name="blocked_casts")

    # Social Links
    external_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_user = models.CharField(max_length=15, blank=True)
    instagram_user = models.CharField(max_length=30, blank=True)

    def save(self, *args, **kwargs):
        """
        Add computed values and save model
        """
        # Always make the slug match the name
        self.slug = text.slugify(self.name)
        self.modified_date = timezone.now()
        super(Cast, self).save(*args, **kwargs)

    def add_manager(self, profile: "users.Profile"):
        """
        Adds a new profile to managers or raises an error
        """
        if self.managers.filter(pk=profile.pk):
            raise ValueError(f"{profile} is already a manager of {self}")
        if not self.members.filter(pk=profile.pk):
            raise ValueError(f"{profile} is not a member of {self}")
        self.managers.add(profile)

    def remove_manager(self, profile: "users.Profile"):
        """
        Remove a profile from managers
        """
        if not self.managers.filter(pk=profile.pk):
            raise ValueError(f"{profile} is not a manager or {self}")
        self.managers.remove(profile)  # pylint: disable=E1101

    def is_manager(self, profile: "users.Profile") -> bool:
        """
        Returns True if a profile is a cast manager
        """
        return bool(self.managers.filter(pk=profile.pk))

    def add_member(self, profile: "users.Profile"):
        """
        Adds a new profile to members or raises an error
        """
        if self.members.filter(pk=profile.pk):
            raise ValueError(f"{profile} is already a member of {self}")
        self.members.add(profile)

    def remove_member(self, profile: "users.Profile"):
        """
        Remove a profile from members
        """
        if self.managers.filter(pk=profile.pk):
            raise ValueError(
                f"{profile} cannot be removed because they are a manager of {self}"
            )
        if not self.members.filter(pk=profile.pk):
            raise ValueError(f"{profile} is not a member or {self}")
        self.members.remove(profile)  # pylint: disable=E1101

    def is_member(self, profile: "users.Profile") -> bool:
        """
        Returns True if a profile is a member of the cast
        """
        return bool(self.members.filter(pk=profile.pk))

    def add_member_request(self, profile: "users.Profile"):
        """
        Adds a new profile to membership requests or raises an error
        """
        if self.members.filter(pk=profile.pk):
            raise ValueError(f"{profile} is already a member of {self}")
        if self.member_requests.filter(pk=profile.pk):
            raise ValueError(f"{profile} has already requested to join {self}")
        if self.blocked.filter(pk=profile.pk):
            raise ValueError(f"{profile} is blocked from joining {self}")
        self.member_requests.add(profile)

    def remove_member_request(self, profile: "users.Profile"):
        """
        Removes a profile from membership requests
        """
        if not self.member_requests.filter(pk=profile.pk):
            raise ValueError(f"{profile} has not requested to join {self}")
        self.member_requests.remove(profile)  # pylint: disable=E1101

    def has_requested_membership(self, profile: "users.Profile") -> bool:
        """
        Returns True if a profile has requested cast membership
        """
        return bool(self.member_requests.filter(pk=profile.pk))

    def block_user(self, profile: "users.Profile"):
        """
        Adds a new profile to blocked users or raises an error
        """
        if self.managers.filter(pk=profile.pk):
            raise ValueError(
                f"{profile} cannot be blocked because they are a manager of {self}"
            )
        if self.blocked.filter(pk=profile.pk):
            raise ValueError(f"{profile} is already blocked from {self}")
        self.blocked.add(profile)

    def unblock_user(self, profile: "users.Profile"):
        """
        Remove a profile from blocked users
        """
        if not self.blocked.filter(pk=profile.pk):
            raise ValueError(f"{profile} is not blocked from {self}")
        self.blocked.remove(profile)  # pylint: disable=E1101

    def is_blocked(self, profile: "users.Profile") -> bool:
        """
        Returns True if a profile is blocked from the cast
        """
        return bool(self.blocked.filter(pk=profile.pk))

    @property
    def future_events(self) -> ["Event"]:
        """
        Returns cast events happening today or later
        """
        return self.events.filter(cast=self, date__gte=date.today())

    @property
    def upcoming_events(self) -> ["Event"]:
        """
        Returns the first few future events
        """
        return self.future_events[:3]

    def __str__(self) -> str:
        return self.name


class PageSection(models.Model):
    """
    Additional content sections beyond the built-ins
    """

    cast = models.ForeignKey(
        Cast, on_delete=models.CASCADE, related_name="page_sections"
    )
    title = models.CharField(max_length=128)
    text = models.TextField()
    order = models.PositiveSmallIntegerField(default=1)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.cast.name} | {self.title}"


class CastPhoto(models.Model):
    """
    Photos associated with a cast profile
    """

    cast = models.ForeignKey(Cast, on_delete=models.CASCADE, related_name="photos")
    image = ImageField(upload_to=cast_photo)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-pk"]
