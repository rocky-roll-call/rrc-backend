"""
Models to manage calendar events
"""

# stdlib
from datetime import timedelta

# django
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# library
from django_enumfield import enum

EXPIRES_AFTER = 365 * 2  # days


class Event(models.Model):
    """
    A calendar event
    """

    name = models.CharField(max_length=128)
    description = models.TextField()
    venue = models.CharField(max_length=256)
    start = models.DateTimeField()

    cast = models.ForeignKey(
        "casts.Cast", on_delete=models.CASCADE, related_name="events"
    )
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["start"]

    @property
    def is_expired(self) -> bool:
        """
        Returns if an event is ready for deletion
        """
        return timezone.now() > self.start + timedelta(days=EXPIRES_AFTER)

    def __str__(self) -> str:
        return f"{self.cast.name} | {self.start}"


def get_upcoming_events(days: int = 14, limit: int = 12, cast: int = None) -> dict:
    """
    Returns upcoming events as a calendar dictionary
    """
    search = {
        "start__gte": timezone.now(),
        "start__lte": timezone.now() + timedelta(days=days),
    }
    if cast:
        search["cast__pk"] = cast
    events = Event.objects.filter(**search)[:limit]
    calendar = {}
    for event in events:
        day = event.start.strftime(r"%Y-%m-%d")
        if day in calendar:
            calendar[day].append(event)
        else:
            calendar[day] = [event]
    return calendar


class Role(enum.Enum):
    """
    Roles performed at an event
    """

    FRANK = 1
    JANET = 2
    BRAD = 3
    RIFF = 4
    MAGENTA = 5
    COLUMBIA = 6
    SCOTT = 7
    ROCKY = 8
    EDDIE = 9
    CRIM = 10
    TRANSY = 11

    EMCEE = 20
    TRIXIE = 21

    TECH = 30
    LIGHTS = 31
    PHOTOS = 32

    labels = {
        FRANK: "Dr. Frank-N-Furter",
        JANET: "Janet Weiss",
        BRAD: "Brad Majors",
        RIFF: "Riff Raff",
        MAGENTA: "Magenta",
        COLUMBIA: "Columbia",
        SCOTT: "Dr. Everett V. Scott",
        ROCKY: "Rocky Horror",
        EDDIE: "Eddie",
        CRIM: "The Criminologist",
        TRANSY: "Transylvanian",
        EMCEE: "Emcee",
        TRIXIE: "Trixie",
        TECH: "Tech",
        LIGHTS: "Lights",
        PHOTOS: "Photographer",
    }


class Casting(models.Model):
    """
    Represents a User being cast in a Role at an Event
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="castings")
    profile = models.ForeignKey(
        "users.Profile",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="castings",
    )
    role = enum.EnumField(Role)
    writein = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["role"]

    @property
    def role_tag(self) -> Role:
        """
        Returns the role as the Role enum
        """
        return Role.get(self.role)

    @property
    def show_picture(self) -> bool:
        """
        Returns True if the casting is a non-tech role with profile
        """
        return self.profile and self.role < 30

    def clean(self):
        """
        Validates that the object has either a profile or write-in value
        """
        if not (self.profile or self.writein):
            raise ValidationError("Casting requires either a profile or write-in value")
        if self.profile and self.writein:
            raise ValidationError(
                "Casting can't have both a profile and a write-in value"
            )
